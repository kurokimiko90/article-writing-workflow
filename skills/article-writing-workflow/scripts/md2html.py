"""article.md を単一の article.html に変換する（図は相対パスのまま、warm-paper 系の読みやすい組版）。
用法: python3 md2html.py article.md article.html
"""
import re,html,sys
CSS = """
:root{--bg:#f5f0e8;--ink:#1f2a27;--muted:#6b6f68;--rule:#e2dacb;--accent:#d7ef5c;--teal:#1f6b5c}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1c1f1d;--ink:#ece6da;--muted:#a8a69c;--rule:#33372f;--teal:#7fc7b4}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.9 "PingFang SC","Hiragino Sans GB","Noto Sans SC",sans-serif}
main{max-width:760px;margin:0 auto;padding:56px 16px 96px}
h1{font-size:32px;line-height:1.35;margin:0 0 40px;letter-spacing:.01em}
h2{font-size:22px;margin:56px 0 16px;padding-left:12px;border-left:5px solid var(--accent)}
p{margin:0 0 1.1em}ol,ul{padding-left:1.4em;margin:0 0 1.2em}li{margin:.3em 0}
figure{margin:32px -8px}img{width:100%;height:auto;display:block;border-radius:10px;border:1px solid var(--rule)}
figcaption{font-size:14px;color:var(--muted);margin-top:10px;line-height:1.7}
@media (min-width:900px){figure{margin:36px -60px}}
@media (min-width:1180px){figure{margin:40px -156px}}
figure a{display:block;cursor:zoom-in}
@media print{body{background:#fff}figure{break-inside:avoid}}
html{scroll-behavior:smooth}h2,h3{scroll-margin-top:24px}
nav.toc{margin:0 0 40px;padding:18px 22px;border:1px solid var(--rule);border-radius:10px;font-size:15px;line-height:1.7}
nav.toc b{display:block;margin-bottom:6px;color:var(--muted);font-size:13px;letter-spacing:.1em}
nav.toc ol{margin:0;padding-left:1.4em}nav.toc ol ol{padding-left:1.1em;font-size:14px}nav.toc li{margin:.15em 0}
nav.toc a{color:var(--ink);text-decoration:none}nav.toc a:hover{color:var(--teal);text-decoration:underline}
@media print{nav.toc{display:none}}
"""
src,dst=sys.argv[1],sys.argv[2]
md=open(src).read().splitlines(); out=[];inlist=None;para=[];title='';toc=[]
# 見出しに id を振り、h1 の直後に目次（クリックで該当章へ移動）を差し込む
def heading(level,text):
    hid=f'sec-{len(toc)+1}'; toc.append((level,hid,text))
    return f'<h{level} id="{hid}">'+inline(text)+f'</h{level}>'
def toc_html():
    if not toc: return ''
    label='目次' if re.search(r'[぀-ヿ]',title) else '目录'
    items=[];open_sub=False
    for level,hid,text in toc:
        if level==3 and not open_sub: items.append('<ol>'); open_sub=True
        if level==2 and open_sub: items.append('</ol></li>'); open_sub=False
        elif level==2 and items: items.append('</li>')
        items.append(f'<li><a href="#{hid}">{inline(text)}</a>'+('</li>' if level==3 else ''))
    items.append('</ol></li>' if open_sub else '</li>')
    return f'<nav class="toc" aria-label="{label}"><b>{label}</b><ol>'+''.join(items)+'</ol></nav>'
def inline(t): return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',html.escape(t,quote=False))
def flush():
    global para
    if para: out.append('<p>'+inline(''.join(para))+'</p>'); para=[]
def closelist():
    global inlist
    if inlist: out.append('</%s>'%inlist); inlist=None
for l in md:
    if not l.strip(): flush(); closelist(); continue
    m=re.match(r'!\[(.*?)\]\((.*?)\)',l)
    if m: flush();closelist(); out.append(f'<figure><a href="{m[2]}" target="_blank"><img src="{m[2]}" alt="{html.escape(m[1])}" loading="lazy"></a>'); continue
    if re.match(r'^\*[图図圖].*\*$',l): out.append('<figcaption>'+inline(l.strip('*'))+'</figcaption></figure>'); continue
    if l.startswith('# '): title=l[2:]; out.append('<h1>'+inline(title)+'</h1>'); continue
    if l.startswith('### '): flush();closelist(); out.append(heading(3,l[4:])); continue
    if l.startswith('## '): flush();closelist(); out.append(heading(2,l[3:])); continue
    m=re.match(r'^(\d+)\. (.*)',l)
    if m:
        flush()
        if inlist!='ol': closelist(); out.append('<ol>' if m[1]=='1' else f'<ol start="{m[1]}">'); inlist='ol'
        out.append('<li>'+inline(m[2])+'</li>'); continue
    if l.startswith('- '):
        flush()
        if inlist!='ul': closelist(); out.append('<ul>'); inlist='ul'
        out.append('<li>'+inline(l[2:])+'</li>'); continue
    para.append(l)
flush();closelist()
if out and out[0].startswith('<h1>'): out.insert(1,toc_html())
lang='ja' if re.search(r'[぀-ヿ]',title) else 'zh-Hans'
# 配図密度：表示行（中国語 約40字／日本語 約44字）で数え、図のない区間が 10 行を超えたら知らせる
def figure_gaps(lines,cpl,limit=10):
    gaps=[];run=0;start=None
    for i,l in enumerate(lines,1):
        if l.startswith('!['):
            if run>limit: gaps.append((run,start,i))
            run=0;start=None;continue
        if l.strip() and not re.match(r'^(\*[图図圖]|#)',l):
            run+=max(1,-(-len(re.sub(r'\*\*|`','',l))//cpl));start=start or i
    if run>limit: gaps.append((run,start,len(lines)))
    return gaps
for n,s,e in figure_gaps(md,44 if lang=='ja' else 40):
    print(f'  ! 図のない区間が {n} 行（10 行超）: {src} L{s}-L{e}')
open(dst,'w').write(f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><style>{CSS}</style></head><body><main>\n'+'\n'.join(out)+'\n</main></body></html>')
