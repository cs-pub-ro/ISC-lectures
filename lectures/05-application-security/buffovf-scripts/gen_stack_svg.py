#!/usr/bin/env python3
"""gen_stack_svg.py -- generate the animated "stack before/after the overflow"
diagrams used by buffovf-demo.md (one for x86, one for x86_64).

The SVG is self-contained: the three phases (normal frame -> overflow ->
hijacked return) are driven by CSS keyframes, so the animation also plays when
the file is embedded with <img src="..."> (Slidev does that).

    ./gen_stack_svg.py                     # writes ../images/stack_overflow_*.svg
    ./gen_stack_svg.py --outdir /tmp/x     # somewhere else
"""
import argparse
import os

# --- palette ---------------------------------------------------------------
INK = "#141414"
MUTED = "#6b7280"
BLUE = "#1f6feb"
RED = "#c92a2a"
RED_FILL = "#ffe3e0"
GREEN = "#1a7f37"
GREEN_FILL = "#e7f6ec"
GREY_FILL = "#f4f4f4"
WHITE = "#ffffff"
FONT = "ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

CYCLE = 12          # seconds for one full before -> after loop
W, H = 900, 300     # canvas; the slide shows it at ~1:1

ARCH = {
    "x86": dict(
        label="x86 (i386)",
        word=4,
        ret_orig="0x80491db",
        ret_text="0x8049196",
        off=68,
        rbp="ebp",
        pack="p32",
        extra="arguments travel on the stack → ret2libc needs no gadget",
        cells=[("buf[64]", 320), ("saved ebp", 74), ("return addr", 100),
               ("caller frame (main)", 170)],
    ),
    "x86_64": dict(
        label="x86_64 (amd64)",
        word=8,
        ret_orig="0x4011a4",
        ret_text="0x401156",
        off=72,
        rbp="rbp",
        pack="p64",
        extra="the first argument travels in rdi → ret2libc needs a gadget",
        cells=[("buf[64]", 320), ("saved rbp", 86), ("return addr", 100),
               ("caller frame (main)", 170)],
    ),
}


def svg(arch_key):
    a = ARCH[arch_key]
    cells = a["cells"]
    x0, y, h = 36, 76, 100
    xs, x = [], x0
    for _, cw in cells:
        xs.append(x)
        x += cw
    buf_x, buf_w = xs[0], cells[0][1]
    rbp_x, rbp_w = xs[1], cells[1][1]
    ret_x, ret_w = xs[2], cells[2][1]
    bar_rbp = (rbp_x + rbp_w) - buf_x     # bytes written: buffer + saved rbp
    bar_end = (ret_x + ret_w) - buf_x     # ... + the return-address slot

    css = f"""
    @keyframes bar {{
      0%, 33%   {{ width: 0px; }}
      47%       {{ width: {buf_w}px; }}
      55%       {{ width: {buf_w}px; }}
      63%       {{ width: {bar_rbp}px; }}
      71%, 100% {{ width: {bar_end}px; }}
    }}
    @keyframes ptext {{ 0%, 33% {{ opacity: 0; }} 36%, 100% {{ opacity: 1; }} }}
    @keyframes caret {{
      0%, 33%   {{ opacity: 0; transform: translateX(0px); }}
      34%, 70%  {{ opacity: 1; }}
      47%       {{ transform: translateX({buf_w}px); }}
      63%       {{ transform: translateX({bar_rbp}px); }}
      71%       {{ transform: translateX({bar_end}px); }}
      72%, 100% {{ opacity: 0; transform: translateX({bar_end}px); }}
    }}
    @keyframes ret_normal {{ 0%, 68% {{ opacity: 1; }} 72%, 100% {{ opacity: 0; }} }}
    @keyframes ret_pwned  {{ 0%, 68% {{ opacity: 0; }} 72%, 100% {{ opacity: 1; }} }}
    @keyframes ret_fill   {{ 0%, 70% {{ fill: {WHITE}; }} 72%, 100% {{ fill: {RED_FILL}; }} }}
    @keyframes c1 {{ 0%, 32% {{ opacity: 1; }} 34%, 100% {{ opacity: 0; }} }}
    @keyframes c2 {{ 0%, 33% {{ opacity: 0; }} 35%, 65% {{ opacity: 1; }} 67%, 100% {{ opacity: 0; }} }}
    @keyframes c3 {{ 0%, 66% {{ opacity: 0; }} 68%, 96% {{ opacity: 1; }} 99%, 100% {{ opacity: 0; }} }}
    @keyframes arrow {{
      0%, 70% {{ stroke-dashoffset: 240; opacity: 0; }}
      74%     {{ opacity: 1; }}
      88%, 100% {{ stroke-dashoffset: 0; opacity: 1; }}
    }}
    @keyframes target {{ 0%, 71% {{ opacity: 0; }} 76%, 100% {{ opacity: 1; }} }}
    .bar    {{ animation: bar {CYCLE}s linear infinite; }}
    .ptext  {{ animation: ptext {CYCLE}s infinite; }}
    .caret  {{ animation: caret {CYCLE}s infinite; }}
    .retn   {{ animation: ret_normal {CYCLE}s infinite; }}
    .retp   {{ animation: ret_pwned {CYCLE}s infinite; }}
    .retfill{{ animation: ret_fill {CYCLE}s steps(1, end) infinite; }}
    .c1     {{ animation: c1 {CYCLE}s steps(1, end) infinite; }}
    .c2     {{ animation: c2 {CYCLE}s steps(1, end) infinite; }}
    .c3     {{ animation: c3 {CYCLE}s steps(1, end) infinite; }}
    .arrow  {{ animation: arrow {CYCLE}s infinite; }}
    .target {{ animation: target {CYCLE}s steps(1, end) infinite; }}
    """

    p = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="animated {a["label"]} stack frame before and after a buffer overflow">'
    )
    p.append(f"<title>{a['label']}: the frame of greet() before, during and after a buffer overflow</title>")
    p.append(
        f"<style>{css}"
        f"text{{font-family:{FONT};fill:{INK}}}"
        f".hdr{{font-size:15px;font-weight:700}}"
        f".cap{{font-size:14.5px}}"
        f".cell{{font-size:14px;font-weight:600}}"
        f".sm{{font-size:12px;fill:{MUTED}}}"
        f".mono{{font-family:{MONO};font-size:12.5px}}"
        f"</style>"
    )
    p.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{WHITE}"/>')

    # --- header + caption per phase ---------------------------------------
    p.append(f'<text class="hdr" x="{x0}" y="26">{a["label"]} — the frame of greet()</text>')
    p.append(
        f'<text class="cap c1" x="{x0}" y="52">&#9312; untouched: buf[64], then the saved '
        f'{a["rbp"]}, then the saved return address</text>'
    )
    p.append(
        f'<text class="cap c2" x="{x0}" y="52">&#9313; gets(buf) keeps writing: the padding runs over '
        f'<tspan font-weight="700">saved {a["rbp"]}</tspan> and the '
        f'<tspan font-weight="700">return address</tspan></text>'
    )
    p.append(
        f'<text class="cap c3" x="{x0}" y="52">&#9314; ret pops the attacker value: the CPU jumps where we say</text>'
    )

    # --- cells -------------------------------------------------------------
    for i, (name, cw) in enumerate(cells):
        fill = WHITE if i < 3 else GREY_FILL
        extra = ' class="retfill"' if i == 2 else ""
        p.append(
            f'<rect x="{xs[i]}" y="{y}" width="{cw}" height="{h}" fill="{fill}" '
            f'stroke="{INK}" stroke-width="2.5"{extra}/>'
        )
    # payload bar (behind the labels)
    p.append(
        f'<rect class="bar" x="{buf_x}" y="{y}" width="0" height="{h}" fill="{RED_FILL}" '
        f'fill-opacity="0.95" stroke="none"/>'
    )
    p.append(
        f'<rect class="bar" x="{buf_x}" y="{y + h - 26}" width="0" height="26" fill="{RED}" '
        f'fill-opacity="0.9" stroke="none"/>'
    )
    p.append(
        f'<text class="ptext mono" x="{buf_x + 10}" y="{y + h - 8}" fill="{WHITE}" '
        f'font-size="12" font-weight="700">"AAAA…AAAA" + {a["pack"]}(…)</text>'
    )
    p.append(f'<g class="caret"><path d="M {buf_x} {y - 6} l 7 -11 l -14 0 z" fill="{RED}"/></g>')

    # --- labels (on top of the bar) ---------------------------------------
    p.append(f'<text class="cell" x="{buf_x + 10}" y="{y + 22}">buf[64]</text>')
    p.append(
        f'<text class="sm" x="{buf_x + buf_w - 10}" y="{y + 22}" text-anchor="end">'
        f'64 bytes of stack memory</text>'
    )
    p.append(
        f'<text class="cell" x="{rbp_x + rbp_w / 2}" y="{y + 22}" text-anchor="middle">saved</text>'
        f'<text class="cell" x="{rbp_x + rbp_w / 2}" y="{y + 42}" text-anchor="middle">{a["rbp"]}</text>'
    )
    p.append(
        f'<text class="cell" x="{ret_x + ret_w / 2}" y="{y + 22}" text-anchor="middle" '
        f'font-size="13">return addr</text>'
        f'<text class="retn mono" x="{ret_x + ret_w / 2}" y="{y + 50}" text-anchor="middle" '
        f'fill="{MUTED}">{a["ret_orig"]}</text>'
        f'<text class="retp mono" x="{ret_x + ret_w / 2}" y="{y + 50}" text-anchor="middle" '
        f'fill="{RED}" font-weight="700">{a["ret_text"]}</text>'
    )
    p.append(
        f'<text class="cell" x="{xs[3] + 12}" y="{y + 22}">caller frame</text>'
        f'<text class="sm" x="{xs[3] + 12}" y="{y + h - 12}">main()</text>'
    )

    # --- address labels under the cells -----------------------------------
    ly = y + h + 24
    for i in range(4):
        p.append(
            f'<line x1="{xs[i]}" y1="{y + h + 3}" x2="{xs[i]}" y2="{ly - 12}" '
            f'stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="4 3"/>'
        )
    p.append(f'<text class="mono" x="{buf_x}" y="{ly}" fill="{BLUE}">buf = {a["rbp"]} - 0x40</text>')
    p.append(f'<text class="mono" x="{rbp_x + 4}" y="{ly}" fill="{BLUE}">{a["rbp"]}</text>')
    p.append(
        f'<text class="mono" x="{ret_x + 4}" y="{ly}" fill="{BLUE}">{a["rbp"]} + {a["word"]}'
        f' &#8592; offset {a["off"]}</text>'
    )

    # --- phase 3: where the return now points -----------------------------
    tgt_w, tgt_h = 330, 54
    tgt_x, tgt_y = ret_x + ret_w - tgt_w, ly + 16
    p.append(
        f'<g class="target">'
        f'<rect x="{tgt_x}" y="{tgt_y}" width="{tgt_w}" height="{tgt_h}" rx="12" '
        f'fill="{GREEN_FILL}" stroke="{GREEN}" stroke-width="2.5"/>'
        f'<text class="cell" x="{tgt_x + tgt_w / 2}" y="{tgt_y + 23}" text-anchor="middle" '
        f'fill="{GREEN}" font-size="13.5">attacker-chosen target</text>'
        f'<text class="mono" x="{tgt_x + tgt_w / 2}" y="{tgt_y + 42}" text-anchor="middle" '
        f'fill="{GREEN}">win() · system("/bin/sh") · a ROP gadget</text>'
        f"</g>"
    )
    p.append(
        f'<path class="arrow" d="M {ret_x + ret_w - 6} {y + h} '
        f"C {ret_x + ret_w - 6} {ly + 2}, {tgt_x + tgt_w - 60} {tgt_y - 20}, "
        f'{tgt_x + tgt_w - 60} {tgt_y - 3}" '
        f'fill="none" stroke="{GREEN}" stroke-width="3" stroke-dasharray="240" '
        f'stroke-dashoffset="240" marker-end="url(#head)"/>'
        f'<defs><marker id="head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" '
        f'markerHeight="6" orient="auto-start-reverse">'
        f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{GREEN}"/></marker></defs>'
    )

    # --- footer -----------------------------------------------------------
    p.append(
        f'<text class="sm" x="{x0}" y="{H - 10}">offset to the return address = 64 (buffer) + '
        f'{a["word"]} (saved {a["rbp"]}) = <tspan font-weight="700">{a["off"]}</tspan> bytes &#183; '
        f'{a["extra"]}</text>'
    )
    p.append("</svg>")
    return "\n".join(p)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", default=os.path.join(here, "..", "images"))
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    for key in ARCH:
        path = os.path.join(a.outdir, f"stack_overflow_{key}_animated.svg")
        with open(path, "w") as f:
            f.write(svg(key))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
