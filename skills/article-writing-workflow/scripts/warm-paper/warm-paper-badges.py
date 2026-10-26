"""warm-paper の図に丸いアイコンバッジ（lucide）を入れる。

使い方: python3 warm-paper-badges.py <badges.json>
badges.json: {"<file>.html": [{"anchor":"文言の一部", "icon":"user", "tone":"apricot"}, ...]}
- anchor: そのバッジを付けたいカード内の文字列。ブラウザで文字の範囲を測り、カードの内側で文字と重ならない位置（左中→右上→右中→左上、半径は段階的に縮小）を選ぶ。
  同じ大きさのカードの組は同じ位置・同じ半径にそろえる。組の 1 枚でも置けなければ、組ごと付けずに警告を出す（一部だけ付くと不揃いになるため）。カードのない文字は文字の左に置く
- 位置を固定したいときは anchor の代わりに cx/cy/r を書く
- icon: icons/<icon>.svg（本スクリプトと同じフォルダ）（lucide-static@0.469.0）。null なら丸だけ描く
- under: true なら既存の図形の下（</defs> の直後）に入れる。既存アイコンの背景用
再実行しても同じ結果になる（前回のバッジを消してから入れ直す）。
"""
import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

ICON_DIR = Path(__file__).resolve().parent / "icons"
TONES = {  # (背景, アイコン色)
    "apricot": ("#F8DCCB", "#9A4A22"),
    "teal": ("#D3E7E3", "#11645B"),
    "lime": ("#D9F05B", "#1F2A27"),
    "ink": ("#1F2A27", "#FFFCF6"),
    "neutral": ("#EAE4D8", "#5E6B66"),
}
GROUP_RE = re.compile(r'<g class="wp-badges[^"]*"[^>]*>.*?</g><!--/wp-badges-->\n?', re.S)


def icon_body(name: str) -> str:
    svg = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
    inner = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]
    return re.sub(r"\s+", " ", inner).strip()


def badge(b: dict) -> str:
    bg, fg = TONES[b["tone"]]
    cx, cy, r = b["cx"], b["cy"], b["r"]
    out = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
    if b.get("icon"):
        size = r * 1.1
        k = size / 24
        out += (f'<g transform="translate({cx - size / 2:.2f},{cy - size / 2:.2f}) scale({k:.4f})" fill="none" '
                f'stroke="{fg}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon_body(b["icon"])}</g>')
    return out


def apply(html: str, items: list) -> str:
    html = GROUP_RE.sub("", html)
    over = "".join(badge(b) for b in items if not b.get("under"))
    under = "".join(badge(b) for b in items if b.get("under"))
    if under:
        group = f'<g class="wp-badges under" aria-hidden="true">{under}</g><!--/wp-badges-->\n'
        html = html.replace("</defs>", "</defs>\n" + group, 1)
    if over:
        group = f'<g class="wp-badges" aria-hidden="true">{over}</g><!--/wp-badges-->\n'
        i = html.index("</svg>", html.index("<svg", html.index("<body")))
        html = html[:i] + group + html[i:]
    return html


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SKIPPED: list[str] = []  # 置き場所がなく付けられなかったバッジ（build が失敗扱いにする）

# anchor の文言を含むカードを探し、文字と重ならない位置を選ぶ（ブラウザで実測）
SOLVER_JS = r"""<script id="wp-solver">(function(){
const spec=JSON.parse(document.getElementById('wp-spec').textContent);
const svg=[...document.querySelectorAll('svg[viewBox]')].sort((a,b)=>b.getBoundingClientRect().width-a.getBoundingClientRect().width)[0];
const texts=[...svg.querySelectorAll('text')].filter(t=>!t.matches('.ey,.hd,.title,.eyebrow')).map(t=>({t,b:t.getBBox()}));
const rects=[...svg.querySelectorAll('rect')].map(r=>r.getBBox()).filter(b=>b.width>=60&&b.height>=40);
const hit=(c,r,m)=>texts.some(({b})=>c.x+r+m>b.x&&c.x-r-m<b.x+b.width&&c.y+r+m>b.y&&c.y-r-m<b.y+b.height);
const inside=(c,r,k)=>c.x-r>=k.x+6&&c.x+r<=k.x+k.width-6&&c.y-r>=k.y+6&&c.y+r<=k.y+k.height-6;
// 候補：0=左中 1=右上 2=右中 3=左上（カード内）、4–6=左上の縁にまたがる（上へ 0/3/6px ずらす。内側に余白がない密なカード用の最終手段）
const cand=(k,r)=>[{x:k.x+16+r,y:k.y+k.height/2},{x:k.x+k.width-14-r,y:k.y+14+r},
                   {x:k.x+k.width-16-r,y:k.y+k.height/2},{x:k.x+14+r,y:k.y+14+r},{x:k.x+18+r,y:k.y},{x:k.x+18+r,y:k.y-3},{x:k.x+18+r,y:k.y-6}];
const items=spec.map(s=>{
  const boxOf=tx=>{const cx=tx.b.x+tx.b.width/2, cy=tx.b.y+tx.b.height/2;
    return rects.filter(k=>cx>k.x&&cx<k.x+k.width&&cy>k.y&&cy<k.y+k.height).sort((a,b)=>a.width*a.height-b.width*b.height)[0];};
  const hits=texts.filter(({t})=>t.textContent.includes(s.anchor));
  if(!hits.length) return {s,error:'anchor not found'};
  const tx=hits.find(h=>boxOf(h))||hits[0];
  return {s,tx,box:boxOf(tx)};
});
const radii=k=>{const r0=Math.max(14,Math.min(20,Math.round(k.height*0.22)));return [r0,r0-3,r0-6,12].filter((v,i,a)=>v>=12&&a.indexOf(v)===i);};
const ok=(it,r,i)=>{const p=cand(it.box,r)[i];if(hit(p,r,i<4?4:2))return false;return i<4?inside(p,r,it.box):(p.x-r>=it.box.x+4&&p.x+r<=it.box.x+it.box.width-4);};
const groups={};
items.filter(it=>!it.error&&it.box).forEach(it=>{const g=Math.round(it.box.width)+'x'+Math.round(it.box.height);(groups[g]=groups[g]||[]).push(it);});
Object.values(groups).forEach(g=>{
  let best=null;
  outer: for(const idx of [[0,1,2,3],[4,5,6]]){for(const r of radii(g[0].box)){for(const i of idx){const n=g.filter(it=>ok(it,r,i)).length;
    if(n>0&&(!best||n>best.n))best={r,i,n};if(best&&best.n===g.length)break outer;}}}
  g.forEach(it=>{if(best&&best.n===g.length){const p=cand(it.box,best.r)[best.i];it.res={cx:Math.round(p.x),cy:Math.round(p.y),r:best.r};}
                 else it.error=g.length>1?'group of '+g.length+' has no common spot':'no free spot';});
});
items.filter(it=>!it.error&&!it.box).forEach(it=>{
  const r=it.s.r||16;const p={x:it.tx.b.x-10-r,y:it.tx.b.y+it.tx.b.height/2};
  if(!hit(p,r,6))it.res={cx:Math.round(p.x),cy:Math.round(p.y),r};else it.error='no free spot';
});
document.body.dataset.wpBadges=JSON.stringify(items.map(it=>it.error?{anchor:it.s.anchor,error:it.error}:{anchor:it.s.anchor,...it.res}));
})();</script>"""


def solve(path: Path, items: list) -> list:
    """anchor 指定のバッジを座標に解決する。cx/cy 指定のものはそのまま返す。"""
    todo = [b for b in items if "anchor" in b and "cx" not in b]
    if not todo:
        return items
    html = GROUP_RE.sub("", path.read_text(encoding="utf-8"))
    spec = json.dumps([{"anchor": b["anchor"], "r": b.get("r")} for b in todo], ensure_ascii=False)
    probe = html.replace("</body>", f'<script type="application/json" id="wp-spec">{spec}</script>{SOLVER_JS}</body>', 1)
    tmp = path.with_name(f".wp-solve-{path.name}")
    tmp.write_text(probe, encoding="utf-8")
    try:
        dom = subprocess.run(["perl", "-e", "alarm 60; exec @ARGV", CHROME, "--headless=new", "--disable-gpu",
                              "--window-size=1360,900", "--virtual-time-budget=10000", "--dump-dom",
                              f"file://{tmp.resolve()}"], capture_output=True, text=True).stdout
    finally:
        tmp.unlink(missing_ok=True)
    m = re.search(r'data-wp-badges="([^"]*)"', dom)
    if not m:
        raise SystemExit(f"solver failed: {path.name}")
    solved = {s["anchor"]: s for s in json.loads(unescape(m.group(1)))}
    result = []
    for b in items:
        if b in todo:
            s = solved[b["anchor"]]
            if "error" in s:
                print(f"  ! {path.name}: {s['anchor']} -> {s['error']}（スキップ）")
                SKIPPED.append(f"{path.name}「{s['anchor']}」")
                continue
            b = {**b, "cx": s["cx"], "cy": s["cy"], "r": s["r"]}
        result.append(b)
    return result


def run(spec_path: Path) -> None:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    for name, items in spec.items():
        p = spec_path.parent / name
        resolved = solve(p, items)
        p.write_text(apply(p.read_text(encoding="utf-8"), resolved), encoding="utf-8")
        print("badged", name, len(resolved))


if __name__ == "__main__":
    run(Path(sys.argv[1]))
