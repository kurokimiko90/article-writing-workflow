"""warm-paper 変換後の図を仕上げる（灰色の枠と地・文字下の四角・小さい文字・余白・見出しの折り返し）。

使い方: python3 warm-paper-polish.py <file.html>...（warm-paper-convert.py の後に実行。再実行しても結果は変わらない）
"""
import re
import sys
from pathlib import Path

MARK = "/* wp-polish */"
# 図内の最小文字サイズ（SVG 単位≒PNG の CSS px）。記事では約 0.65〜0.8 倍に縮むため、16 で表示 10〜13px を確保
MIN_FONT = 16

POLISH_CSS = MARK + """
.frame h1 { font-family:'Noto Sans SC','PingFang SC',sans-serif !important; font-weight:900 !important; color:#1F2A27 !important; font-size:36px !important; text-wrap:balance; word-break:keep-all; }
.ptag,.tag,.eb,.al,.leg,.legh { font-family:var(--sans) !important; letter-spacing:.04em !important; }
.sub,.tag,.al,.leg,.legh,.eb,.ptag { font-size:%dpx !important; }""" % MIN_FONT + """
.call { fill:var(--accent) !important; font-weight:700 !important; }
.frame h1 mark { background:linear-gradient(transparent 52%, #D9F05B 52%, #D9F05B 92%, transparent 92%) !important; color:inherit; }
body.shot svg .ey, body.shot svg .hd, body.shot svg text.title, body.shot p.sub { display:none; }
"""

# 行間をそろえる：同じ x・同じ揃えで縦に積んだ文字行（字を大きくして詰まった行）を 1.4×字号 の間隔に広げる。
# 行のまとまりの中心は動かさないので、カードの中で上下中央のまま
RELAYOUT_JS = """<script>/* wp-relayout */
(()=>{const LH=1.4,fs=t=>parseFloat(getComputedStyle(t).fontSize),key=t=>t.getAttribute('x')+'|'+getComputedStyle(t).textAnchor;
document.querySelectorAll('svg').forEach(svg=>{const ts=[...svg.querySelectorAll('text[y]')].filter(t=>t.textContent.trim()),groups=[];
ts.forEach(t=>{const g=groups[groups.length-1],p=g&&g[g.length-1];
if(p&&p.parentNode===t.parentNode&&key(p)===key(t)&&+t.getAttribute('y')>+p.getAttribute('y')&&+t.getAttribute('y')-+p.getAttribute('y')<LH*Math.max(fs(p),fs(t)))g.push(t);else groups.push([t])});
groups.filter(g=>g.length>1).forEach(g=>{const y=g.map(t=>+t.getAttribute('y')),c=(y[0]+y[y.length-1])/2,ny=[0];
for(let i=1;i<g.length;i++)ny.push(ny[i-1]+Math.max(y[i]-y[i-1],LH*Math.max(fs(g[i-1]),fs(g[i]))));
const sh=c-(ny[0]+ny[ny.length-1])/2;g.forEach((t,i)=>t.setAttribute('y',Math.round(ny[i]+sh)))});
/* 胶囊（rx≧高さ/2 の rect＋中央揃えの文字）：文字が入らなければ、同じ行の胶囊を左から詰め直して幅を文字に合わせる */
const pills=[...svg.querySelectorAll('rect[rx]')].filter(r=>+r.getAttribute('rx')>=+r.getAttribute('height')/2-1&&+r.getAttribute('height')<=44).map(r=>{const x=+r.getAttribute('x'),w=+r.getAttribute('width'),y=+r.getAttribute('y'),h=+r.getAttribute('height');
const t=[...svg.querySelectorAll('text')].find(t=>getComputedStyle(t).textAnchor==='middle'&&Math.abs(+t.getAttribute('x')-(x+w/2))<2&&+t.getAttribute('y')>y&&+t.getAttribute('y')<y+h);return t&&{r,t,x,w,y}}).filter(Boolean);
/* 同じ親・同じ y で、間隔 30 未満で並ぶものだけを 1 行とみなす */
const rows=[];pills.sort((a,b)=>a.y-b.y||a.x-b.x).forEach(p=>{const row=rows.find(r=>{const q=r[r.length-1];return q.r.parentNode===p.r.parentNode&&q.y===p.y&&p.x-(q.x+q.w)<30});row?row.push(p):rows.push([p])});
rows.forEach(row=>{if(!row.some(p=>p.t.getComputedTextLength()+24>p.w))return;
const gap=row.length>1?Math.max(10,Math.min(...row.slice(1).map((p,i)=>p.x-row[i].x-row[i].w))):0;let x=row[0].x;
row.forEach(p=>{const w=Math.max(p.w,Math.ceil(p.t.getComputedTextLength()+28));p.r.setAttribute('x',x);p.r.setAttribute('width',w);p.t.setAttribute('x',x+w/2);x+=w+gap})});
/* 凡例：「色見本＋文字」を左から実際の文字幅で並べ直す（右へ押すだけ。項目間 28） */
const B=e=>e.getBBox(),lg=[...svg.querySelectorAll('text.lg-item,text.leg')].map(t=>{const b=B(t),cy=b.y+b.height/2;
const m=[...svg.querySelectorAll('rect,line,path,circle')].filter(e=>!e.closest('.wp-badges')&&e.getAttribute('class')!=='lg-rule').map(e=>[e,B(e)]).filter(([e,r])=>r.x+r.width<=b.x+2&&r.x+r.width>=b.x-48&&Math.abs(r.y+r.height/2-cy)<10&&r.width<80).sort((p,q)=>q[1].x-p[1].x)[0];
return{t,b,m,left:m?m[1].x:b.x,cy}}).sort((a,b)=>a.cy-b.cy||a.left-b.left);
let cur=-1e9,cyp=null;lg.forEach(it=>{if(cyp===null||Math.abs(it.cy-cyp)>8)cur=-1e9;cyp=it.cy;const sh=Math.max(0,cur-it.left);
if(sh)[it.t,it.m&&it.m[0]].filter(Boolean).forEach(e=>e.setAttribute('transform',`translate(${sh},0) `+(e.getAttribute('transform')||'')));
cur=it.b.x+it.b.width+sh+28})})})();
</script>"""

# 余白を詰める：SVG の viewBox を中身の bbox に合わせる（#shot 時のみ）
CROP_JS = """<script>/* wp-crop */
if(location.hash==='#shot'){const s=[...document.querySelectorAll('svg[viewBox]')].sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
const b=s.getBBox();const p=20;
s.setAttribute('viewBox',[b.x-p,b.y-p,b.width+2*p,b.height+2*p].map(v=>Math.round(v)).join(' '));
const h=document.querySelector('h1');document.body.dataset.mainH=s.getBoundingClientRect().bottom-(h?h.getBoundingClientRect().top:s.getBoundingClientRect().top);
/* 間隔チェック：文字同士・文字とバッジの重なり、文字が入っている枠からのはみ出しを data-overlap に書く */
/* 字形の範囲＝箱の中心±0.5×字号（Chrome の箱は行の高さを含むため）。行間は 1.25×字号 以上を求める */
const R=e=>e.getBoundingClientRect(),hit=(a,b,g)=>a.left<b.right-g&&b.left<a.right-g&&a.top<b.bottom-g&&b.top<a.bottom-g;
const sc=s.getBoundingClientRect().width/s.viewBox.baseVal.width;
const ink=t=>{const r=R(t),f=parseFloat(getComputedStyle(t).fontSize)*sc,c=(r.top+r.bottom)/2;return{left:r.left,right:r.right,top:c-f/2,bottom:c+f/2,f}};
const ts=[...s.querySelectorAll('text')].filter(t=>t.textContent.trim()&&R(t).width),bs=[...s.querySelectorAll('.wp-badges > *')];
const rs=[...s.querySelectorAll('rect')].map(R).filter(r=>r.width>40&&r.height>24),cs=[...s.querySelectorAll('circle')].map(R),out=[];
/* 凡例の色見本（小さな rect。文字下のマスクは除く） */
const sw=[...s.querySelectorAll('rect')].filter(r=>!r.classList.contains('mask')&&+r.getAttribute('width')<=40&&+r.getAttribute('height')<=20&&(r.getAttribute('stroke')||!/#FFFCF6|#F4EFE6/i.test(r.getAttribute('fill')||''))).map(R),nm=t=>t.textContent.trim().slice(0,14);
ts.forEach((t,i)=>{const a=ink(t);
ts.slice(i+1).forEach(u=>{const b=ink(u),g=Math.max(a.f,b.f)*.25;
if(a.left<b.right+2&&b.left<a.right+2&&a.top<b.bottom+g&&b.top<a.bottom+g)out.push('近すぎ「'+nm(t)+'」×「'+nm(u)+'」')});
bs.forEach(b=>{if(hit(a,R(b),1))out.push('バッジと重なり「'+nm(t)+'」')});
sw.forEach(r=>{if(a.left<r.right+6&&r.left<a.right+6&&a.top<r.bottom&&r.top<a.bottom)out.push('凡例の色と近すぎ「'+nm(t)+'」')});
const cx=(a.left+a.right)/2,cy=(a.top+a.bottom)/2;
if(cs.some(r=>Math.hypot(cx-(r.left+r.right)/2,cy-(r.top+r.bottom)/2)<r.width/2))return; /* 丸の中の文字（G1 など）は枠チェック対象外 */
const box=rs.filter(r=>r.left<cx&&cx<r.right&&r.top<cy&&cy<r.bottom).sort((p,q)=>p.width*p.height-q.width*q.height)[0];
if(box&&(a.left<box.left+4||a.right>box.right-4||a.top<box.top+2||a.bottom>box.bottom-2))out.push('枠からはみ出し「'+nm(t)+'」')});
document.body.dataset.overlap=out.join(' | ');}
</script>"""

FONT_LINK = ('<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700;900'
             '&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">')
# convert で拾えない pdm-flat 系の残り色（rgba のアクセント・寒色グレー）
LATE_MAP = {
    "rgba(49,87,213,": "rgba(17,100,91,", "rgba(42,70,176,": "rgba(14,80,72,",
    "#F0F1F4": "#EFE9DD", "#f0f1f4": "#EFE9DD", "#E3E5EA": "#E6DFD2", "#e3e5ea": "#E6DFD2",
    "#B8C1D1": "#C9C2B4", "#b8c1d1": "#C9C2B4",
}

START_FILL = 'fill="#FCEFE4"'
START_STROKE = 'stroke="rgba(242,169,126,0.55)"'


def floor_fonts(s: str) -> str:
    """MIN_FONT 未満の文字サイズ（font 一括指定・font-size・font-size 属性）を MIN_FONT に引き上げる。"""
    up = lambda m: m.group(1) + str(max(MIN_FONT, round(float(m.group(2))))) + m.group(3)
    s = re.sub(r"(\bfont:\s*(?:[\w-]+\s+)*?)(\d+(?:\.\d+)?)(px)", up, s)
    s = re.sub(r"(\bfont-size:\s*)(\d+(?:\.\d+)?)(px)", up, s)
    return re.sub(r'(\bfont-size=")(\d+(?:\.\d+)?)((?:px)?")', up, s)


CANVAS_MIN_W, CANVAS_MIN_H = 1000, 300  # これ以上の大きさで原点にある rect は全面背景とみなす


def strip_canvas_rects(s: str) -> str:
    """原点（x/y 無し or 0）にある全面 rect を fill に関係なく消す。"""
    def is_canvas(m: re.Match) -> bool:
        a = m.group(1)
        num = lambda k: (re.search(r'\b%s="([\d.]+%%?)"' % k, a) or [None, "0"])[1]
        w, h = num("width"), num("height")
        big = lambda v, lim: v.endswith("%") or float(v) >= lim
        return num("x") in ("0", "0.0") and num("y") in ("0", "0.0") \
            and big(w, CANVAS_MIN_W) and big(h, CANVAS_MIN_H)
    pat = r'[ \t]*<rect\b([^>]*?)\s*(?:/>|>\s*</rect>)\n?'
    return re.sub(pat, lambda m: "" if is_canvas(m) else m.group(0), s)


def polish(s: str) -> str:
    s = floor_fonts(s)
    # 仕上げ CSS は毎回入れ直す（ルール更新を既存ファイルにも反映するため）
    s = re.sub(re.escape(MARK) + r".*?(?=</style>)", "", s, count=1, flags=re.S)
    s = s.replace("</style>", POLISH_CSS + "</style>", 1)
    if "Noto+Sans+SC" not in s:
        s = s.replace("</head>", FONT_LINK + "\n</head>", 1)
    for old, new in LATE_MAP.items():
        s = s.replace(old, new)
    # 全面背景 rect は削除（白・カード色の地が紙の上に浮くのを防ぐ。bbox も広げる）
    s = strip_canvas_rects(s)
    # くすんだ灰色の地（起点・人の入力）→ 杏色の淡い地
    s = re.sub(r'fill="rgba\((?:31,42,39,0\.0[35]|125,133,127,0\.10)\)"', START_FILL, s)
    # 濃い枠線 → 細い線
    s = re.sub(r'(<rect[^>]*?)stroke="(?:#1F2A27|#8E948D|#7D857F|rgba\(31,42,39,0\.3[05]\))"', r'\1stroke="rgba(31,42,39,0.14)"', s)
    # 杏色の地には杏色の線
    s = re.sub(r'(<rect[^>]*' + START_FILL + r'[^>]*?)stroke="rgba\(31,42,39,0\.14\)"', r'\1' + START_STROKE, s)
    s = s.replace("灰框 = ", "杏色框 = ")
    # 文字下のマスク（線のない小さなカード色 rect）→ 紙色に近づけて跡を消す
    s = re.sub(r'<rect([^>]*?)height="(1\d|2[0-4])"([^>]*?)fill="#FFFCF6"/>',
               r'<rect\1height="\2"\3fill="#F4EFE6"/>', s)
    s = re.sub(r"<script>/\* wp-(?:relayout|crop) \*/.*?</script>\n?", "", s, flags=re.S)
    s = s.replace("</body>", RELAYOUT_JS + "\n" + CROP_JS + "\n</body>", 1)
    return s


if __name__ == "__main__":
    for p in map(Path, sys.argv[1:]):
        p.write_text(polish(p.read_text(encoding="utf-8")), encoding="utf-8")
        print("polished", p.name)
