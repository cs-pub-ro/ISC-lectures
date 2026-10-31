#!/usr/bin/env python3
"""Generate the stacked-shellcode hijack frames used by the
"Hijack using shellcode" slide (``<v-switch>`` frames 0..4).

Left column: the attacker's input string, ordered the way it lands in memory.
Right column: the stack while ``strcpy`` writes it, then ``leave`` / ``ret``.

Only labels, offsets and addresses live in the SVG — all prose is markdown.

    python3 scripts/gen_hijack_frames.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")

W, H = 700, 382
RULER_X = 38
PAY_X, PAY_W = 46, 244
STK_X, STK_W = 360, 244
TAG_X = 618
TAG_W, TAG_H = 72, 26

# band -> (top y, height) ; the low-address edge (bottom) carries the offset
BANDS = {
    "shell": (44, 68),
    "sled":  (112, 68),
    "ret":   (180, 32),
    "saved": (212, 32),
    "buf":   (244, 96),
}
OFFSET = {"shell": 0x30, "sled": 0x18, "ret": 0x14, "saved": 0x10, "buf": 0x00}
PAYLOAD_LABEL = {
    "shell": "shellcode",
    "sled":  r"\x90 NOP sled",
    "ret":   "0xffffd6a0",
    "saved": '"AAAA"',
    "buf":   '"A" &#215; 16',
}
STACK_LABEL = {
    "ret":   "ret addr = 0x08048a1f",
    "saved": "saved EBP = 0xffffd6f8",
    "buf":   "buf[16]",
}

HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Stack buffer overflow hijack, step {step} of 5: {alt}">
<title>shellcode hijack — step {step}</title>
<style>
  .sr{{font:600 15px Inter,ui-sans-serif,system-ui,sans-serif;fill:#1a1a1a}}
  .sc{{font:14px Inter,ui-sans-serif,system-ui,sans-serif;fill:#5b6670}}
  .off{{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8a949b;text-anchor:end}}
  .pl{{font:600 15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8c1d18;dominant-baseline:central}}
  .sl{{font:600 15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#0f4a5e;dominant-baseline:central}}
  .pay{{fill:#fbe6e3;stroke:#b3261e;stroke-width:1.8}}
  .pay2{{fill:#fdeeeb;stroke:#d98b84;stroke-width:1.4;stroke-dasharray:5 4}}
  .orig{{fill:#e4eff1;stroke:#176b87;stroke-width:1.8}}
  .neutral{{fill:#ffffff;stroke:#9aa6ae;stroke-width:1.8}}
  .ghost{{fill:#f4f6f7;stroke:#b6c0c6;stroke-width:1.6;stroke-dasharray:6 4}}
  .hi{{stroke:#b26b00;stroke-width:3}}
  .conn{{stroke:#c6cfd4;stroke-width:1.6;fill:none;stroke-dasharray:5 4}}
  .jump{{stroke:#b3261e;stroke-width:2.2;fill:none}}
  .tag{{fill:#fff6e6;stroke:#b26b00;stroke-width:2;rx:4}}
  .tagt{{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#7a4b00;text-anchor:middle;dominant-baseline:central}}
  .cap{{font:600 15px Inter,ui-sans-serif,system-ui,sans-serif;fill:#1a1a1a}}
</style>
<defs>
  <marker id="a" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b3261e"/></marker>
  <marker id="g" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b6c0c6"/></marker>
  <marker id="amber" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b26b00"/></marker>
  <pattern id="hatch" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
    <rect width="9" height="9" fill="#fdeeeb"/><line x1="0" y1="0" x2="0" y2="9" stroke="#f3c9c2" stroke-width="4"/>
  </pattern>
</defs>
'''


def band(cls, key, x, w, extra=""):
    y, h = BANDS[key]
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"{extra}/>'


def label(cls, key, x, text, dx=12):
    y, h = BANDS[key]
    return f'<text class="{cls}" x="{x + dx}" y="{y + h / 2}">{text}</text>'


def tag(text, y):
    return (f'<rect class="tag" x="{TAG_X}" y="{y - TAG_H / 2}" width="{TAG_W}" height="{TAG_H}"/>'
            f'<text class="tagt" x="{TAG_X + TAG_W / 2}" y="{y}">{text}</text>')


def ruler():
    out = []
    for key in ("shell", "sled", "ret", "saved", "buf"):
        y = BANDS[key][0] + BANDS[key][1]
        out.append(f'<text class="off" x="{RULER_X}" y="{y + 4}">0x{OFFSET[key]:02x}</text>')
    return "\n".join(out)


def connectors():
    out = []
    for key in ("shell", "sled", "ret", "saved", "buf"):
        y, h = BANDS[key]
        mid = y + h / 2
        out.append(f'<path class="conn" d="M{PAY_X + PAY_W},{mid} L{STK_X - 14},{mid}" marker-end="url(#g)"/>')
    return "\n".join(out)


def payload_column():
    out = [f'<text class="cap" x="{PAY_X}" y="30">attacker input (as it lands)</text>']
    for key in ("shell", "sled", "ret", "saved", "buf"):
        cls = "pay"
        out.append(band(cls, key, PAY_X, PAY_W))
        out.append(label("pl" if key != "buf" else "sl", key, PAY_X, PAYLOAD_LABEL[key]))
    return "\n".join(out)


def stack_column(frame):
    """frame: 0 = pristine, 1..4 = overwritten."""
    out = [f'<text class="cap" x="{STK_X}" y="30">stack</text>',
           f'<text class="sc" x="{STK_X + STK_W}" y="30" style="text-anchor:end">higher addresses on top</text>']
    if frame == 0:
        out.append('<rect class="ghost" x="%d" y="%d" width="%d" height="%d" rx="3"/>'
                   % (STK_X, BANDS["shell"][0], STK_W, BANDS["sled"][0] + BANDS["sled"][1] - BANDS["shell"][0]))
        out.append(f'<text class="sl" x="{STK_X + 12}" y="{(BANDS["shell"][0] + BANDS["sled"][0] + BANDS["sled"][1]) / 2}">caller\'s frame</text>')
    else:
        for key in ("shell", "sled"):
            out.append(band("pay", key, STK_X, STK_W))
            out.append(label("pl", key, STK_X, "shellcode" if key == "shell" else r"\x90 NOP sled"))
    for key, cls in (("ret", "pay"),
                     ("saved", "orig" if frame == 0 else "pay"),
                     ("buf", "neutral" if frame == 0 else "pay2")):
        out.append(band(cls, key, STK_X, STK_W))
        text = STACK_LABEL[key]
        if frame > 0:
            text = {"ret": "ret addr = 0xffffd6a0",
                    "saved": "saved EBP = 0x41414141",
                    "buf": '"A" &#215; 16  (buf[16])'}[key]
        out.append(label("pl" if frame > 0 else "sl", key, STK_X, text))
    return "\n".join(out)


def jump(from_key, to_key, colour="#b3261e", marker="a", back=34, r=9):
    """Click-to-click redirect arrow: rounded elbow hugging the stack column."""
    ya = BANDS[from_key][0] + BANDS[from_key][1] / 2
    yb = BANDS[to_key][0] + BANDS[to_key][1] / 2
    xm = STK_X - back
    up = yb < ya
    sy = -1 if up else 1
    d = (f"M{STK_X},{ya} L{xm + r},{ya} Q{xm},{ya} {xm},{ya + sy * r} "
         f"L{xm},{yb - sy * r} Q{xm},{yb} {xm + r},{yb} L{STK_X - 2},{yb}")
    return (f'<path d="{d}" stroke="{colour}" stroke-width="2.4" fill="none" '
            f'stroke-linejoin="round" marker-end="url(#{marker})"/>')


def highlight(key):
    y, h = BANDS[key]
    return f'<rect class="hi" x="{STK_X - 2}" y="{y - 2}" width="{STK_W + 4}" height="{h + 4}" rx="5" fill="none"/>'


FRAMES = [
    dict(name="0_payload", frame=0, alt="the attacker's input is copied onto the stack",
         tags=[("ESP", BANDS["buf"][0] + BANDS["buf"][1]), ("EBP", BANDS["saved"][0] + BANDS["saved"][1])],
         arrows=[], hl=None),
    dict(name="1_overwritten", frame=1, alt="the saved EBP and the return address are overwritten",
         tags=[("ESP", BANDS["buf"][0] + BANDS["buf"][1]), ("EBP", BANDS["saved"][0] + BANDS["saved"][1])],
         arrows=[("ret", "sled", "#b3261e", "a")], hl="ret"),
    dict(name="2_ret_pops", frame=1, alt="the return instruction pops the attacker address into EIP",
         tags=[("ESP", BANDS["ret"][0] + BANDS["ret"][1])],
         arrows=[("ret", "sled", "#b3261e", "a")], hl="ret"),
    dict(name="3_sled", frame=1, alt="EIP lands in the NOP sled and slides up into the shellcode",
         tags=[("EIP", BANDS["sled"][0] + BANDS["sled"][1] / 2)],
         arrows=[("sled", "shell", "#b26b00", "amber")], hl="sled"),
    dict(name="4_exec", frame=1, alt="the shellcode executes",
         tags=[("EIP", BANDS["shell"][0] + BANDS["shell"][1] / 2)],
         arrows=[], hl="shell"),
]

for n, fr in enumerate(FRAMES):
    body = [HEAD.format(W=W, H=H, step=n, alt=fr["alt"]),
            ruler(), connectors(), payload_column(), stack_column(fr["frame"])]
    for a_key, b_key, colour, marker in fr["arrows"]:
        body.append(jump(a_key, b_key, colour, marker))
    if fr["hl"]:
        body.append(highlight(fr["hl"]))
    for text, y in fr["tags"]:
        body.append(tag(text, y))
        body.append(f'<path d="M{TAG_X},{y} L{STK_X + STK_W + 3},{y}" stroke="#b26b00" stroke-width="2" fill="none" marker-end="url(#amber)"/>')
    body.append("</svg>")
    path = os.path.join(OUT, f"hijack_{fr['name']}.svg")
    with open(path, "w") as fh:
        fh.write("\n".join(body) + "\n")
    print("wrote", os.path.basename(path))
