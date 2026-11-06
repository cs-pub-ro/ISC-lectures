#!/usr/bin/env python3
"""Generate the stacked ret2libc hijack frames used by the
"Return to LibC" slide (``<v-switch>`` frames 0..4).

Left column: the attacker's input string, ordered the way it lands in memory.
Right column: the stack while ``strcpy`` writes it, then ``leave`` / ``ret``.

Same visual style as gen_hijack_frames.py.

    python3 scripts/gen_ret2libc_frames.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")

W, H = 720, 400
RULER_X = 38
PAY_X, PAY_W = 46, 244
STK_X, STK_W = 360, 244
TAG_X = 618
TAG_W, TAG_H = 72, 26

# band -> (top y, height); high addresses at the top, low at the bottom
BANDS = {
    "binsh":  (40,  32),   # "/bin/sh\0" string planted above the args
    "arg0":   (80,  38),   # pointer to "/bin/sh"
    "fakeret":(126, 38),   # fake return address (0xDEADBEEF)
    "ret":    (172, 38),   # overwritten return address -> &system
    "saved":  (218, 34),   # saved EBP
    "buf":    (260, 80),   # buf[16] filled with 'A's
}

OFFSET = {
    "binsh":  0x28,
    "arg0":   0x20,
    "fakeret":0x1c,
    "ret":    0x18,
    "saved":  0x14,
    "buf":    0x00,
}

PAYLOAD_LABEL = {
    "binsh":   '"/bin/sh\\0"',
    "arg0":    "0xffffd6c0",
    "fakeret": "0xDEADBEEF",
    "ret":     "0x0804a011",
    "saved":   '"AAAA"',
    "buf":     '"A" &#215; 16',
}

PAYLOAD_SUBLABEL = {
    "binsh":   "",
    "arg0":    "ptr to string",
    "fakeret": "fake return",
    "ret":     "&amp;system()",
    "saved":   "junk",
    "buf":     "",
}

STACK_LABEL = {
    "binsh":   "",
    "arg0":    "",
    "fakeret": "",
    "ret":     "ret addr = 0x08048a1f",
    "saved":   "saved EBP = 0xffffd6f8",
    "buf":     "buf[16]",
}

HEAD = '''\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="ret2libc hijack, step {step} of 5: {alt}">
<title>ret2libc — step {step}</title>
<style>
  .sr{{font:600 15px Inter,ui-sans-serif,system-ui,sans-serif;fill:#1a1a1a}}
  .sc{{font:14px Inter,ui-sans-serif,system-ui,sans-serif;fill:#5b6670}}
  .off{{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8a949b;text-anchor:end}}
  .pl{{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8c1d18;dominant-baseline:central}}
  .pl2{{font:11px Inter,ui-sans-serif,system-ui,sans-serif;fill:#8c1d18;dominant-baseline:central}}
  .sl{{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#0f4a5e;dominant-baseline:central}}
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
  .libc{{fill:#e4eff1;stroke:#176b87;stroke-width:2}}
  .libct{{font:600 18px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#0f4a5e;text-anchor:middle;dominant-baseline:central}}
  .libcs{{font:11px Inter,ui-sans-serif,system-ui,sans-serif;fill:#5b6670;text-anchor:middle}}
  .note{{font:11px Inter,ui-sans-serif,system-ui,sans-serif;fill:#5b6670}}
  .leg1{{font:600 12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#b3261e}}
  .leg2{{font:600 12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#0f4a5e}}
</style>
<defs>
  <marker id="a" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b3261e"/></marker>
  <marker id="g" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b6c0c6"/></marker>
  <marker id="teal" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#176b87"/></marker>
  <marker id="amber" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#b26b00"/></marker>
</defs>
'''


def band(cls, key, x, w, extra=""):
    y, h = BANDS[key]
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="3"{extra}/>'


def label(cls, key, x, text, dx=12):
    y, h = BANDS[key]
    return f'<text class="{cls}" x="{x + dx}" y="{y + h / 2}">{text}</text>'


def sublabel(key, x, dx=12):
    if not PAYLOAD_SUBLABEL.get(key):
        return ""
    y, h = BANDS[key]
    return f'<text class="pl2" x="{x + dx}" y="{y + h / 2 + 14}">{PAYLOAD_SUBLABEL[key]}</text>'


def tag(text, y):
    return (f'<rect class="tag" x="{TAG_X}" y="{y - TAG_H / 2}" width="{TAG_W}" height="{TAG_H}"/>'
            f'<text class="tagt" x="{TAG_X + TAG_W / 2}" y="{y}">{text}</text>')


def ruler():
    out = []
    for key in ("binsh", "arg0", "fakeret", "ret", "saved", "buf"):
        y = BANDS[key][0] + BANDS[key][1]
        out.append(f'<text class="off" x="{RULER_X}" y="{y + 4}">0x{OFFSET[key]:02x}</text>')
    return "\n".join(out)


def connectors():
    out = []
    for key in ("binsh", "arg0", "fakeret", "ret", "saved", "buf"):
        y, h = BANDS[key]
        mid = y + h / 2
        out.append(f'<path class="conn" d="M{PAY_X + PAY_W},{mid} L{STK_X - 14},{mid}" marker-end="url(#g)"/>')
    return "\n".join(out)


def payload_column():
    out = [f'<text class="cap" x="{PAY_X}" y="30">attacker input (as it lands)</text>']
    for key in ("binsh", "arg0", "fakeret", "ret", "saved", "buf"):
        out.append(band("pay", key, PAY_X, PAY_W))
        out.append(label("pl", key, PAY_X, PAYLOAD_LABEL[key]))
        sub = sublabel(key, PAY_X)
        if sub:
            out.append(sub)
    return "\n".join(out)


def stack_column(frame):
    """frame: 0 = pristine, 1 = overwritten, 2+ = animation steps."""
    out = [f'<text class="cap" x="{STK_X}" y="30">stack</text>',
           f'<text class="sc" x="{STK_X + STK_W}" y="30" style="text-anchor:end">higher addresses on top</text>']
    if frame == 0:
        # binsh, arg0, fakeret zones are the caller's frame (ghost)
        top_y = BANDS["binsh"][0]
        bot_y = BANDS["fakeret"][0] + BANDS["fakeret"][1]
        out.append(f'<rect class="ghost" x="{STK_X}" y="{top_y}" width="{STK_W}" height="{bot_y - top_y}" rx="3"/>')
        out.append(f'<text class="sl" x="{STK_X + 12}" y="{(top_y + bot_y) / 2}">caller\'s frame</text>')
        # ret: original
        out.append(band("orig", "ret", STK_X, STK_W))
        out.append(label("sl", "ret", STK_X, STACK_LABEL["ret"]))
        # saved EBP: original
        out.append(band("orig", "saved", STK_X, STK_W))
        out.append(label("sl", "saved", STK_X, STACK_LABEL["saved"]))
        # buf: neutral
        out.append(band("neutral", "buf", STK_X, STK_W))
        out.append(label("sl", "buf", STK_X, STACK_LABEL["buf"]))
    else:
        # All overwritten
        STACK_OVR = {
            "binsh":   '"/bin/sh\\0"',
            "arg0":    "0xffffd6c0  (arg0)",
            "fakeret": "0xDEADBEEF",
            "ret":     "&amp;system = 0x0804a011",
            "saved":   "saved EBP = 0x41414141",
            "buf":     '"A" &#215; 16  (buf[16])',
        }
        for key in ("binsh", "arg0", "fakeret", "ret", "saved", "buf"):
            cls = "pay" if key in ("ret", "binsh", "arg0") else "pay2"
            out.append(band(cls, key, STK_X, STK_W))
            out.append(label("pl", key, STK_X, STACK_OVR[key]))
    return "\n".join(out)


def libc_box():
    """The libc system() box on the right side."""
    return (
        f'<rect class="libc" x="452" y="158" width="250" height="70" rx="5"/>'
        f'<text class="libct" x="577" y="184">system()</text>'
        f'<text class="libcs" x="577" y="208">in libc · code we reuse</text>'
    )


def jump_arrow(from_key, to_x, to_y, colour="#176b87", marker="teal"):
    """Arrow from a stack band to an external box."""
    ya = BANDS[from_key][0] + BANDS[from_key][1] / 2
    x_start = STK_X + STK_W + 4
    return (f'<path d="M{x_start},{ya} L{to_x},{to_y}" '
            f'stroke="{colour}" stroke-width="2.2" fill="none" marker-end="url(#{marker})"/>')


def internal_arrow(from_key, to_key, colour="#b3261e", marker="a", back=34, r=9):
    """Elbow arrow between two stack bands."""
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


def legend(frame):
    lines = []
    if frame >= 2:
        lines.append(f'<text class="leg1" x="46" y="360">stack · rw-    injected code cannot execute</text>')
        lines.append(f'<text class="leg2" x="452" y="360">libc · r-x    reuse code that is already there</text>')
    if frame >= 3:
        lines.append(f'<text class="note" x="46" y="380">system() reads arg0 from [esp+4] → pointer to "/bin/sh"</text>')
    return "\n".join(lines)


FRAMES = [
    dict(name="0_payload", frame=0,
         alt="the attacker's crafted input: buf padding, address of system, fake ret, pointer to /bin/sh",
         tags=[("ESP", BANDS["buf"][0] + BANDS["buf"][1]),
               ("EBP", BANDS["saved"][0] + BANDS["saved"][1])],
         show_libc=False, show_ret_arrow=False, show_arg_arrow=False,
         hl=None, int_arrows=[]),
    dict(name="1_overwritten", frame=1,
         alt="strcpy overwrites the frame: return address now points to system()",
         tags=[("ESP", BANDS["buf"][0] + BANDS["buf"][1]),
               ("EBP", BANDS["saved"][0] + BANDS["saved"][1])],
         show_libc=True, show_ret_arrow=False, show_arg_arrow=False,
         hl="ret", int_arrows=[]),
    dict(name="2_ret_pops", frame=1,
         alt="ret pops the address of system() into EIP — the CPU jumps into libc, not the stack",
         tags=[("ESP", BANDS["ret"][0] + BANDS["ret"][1])],
         show_libc=True, show_ret_arrow=True, show_arg_arrow=False,
         hl="ret", int_arrows=[]),
    dict(name="3_arg0", frame=1,
         alt="system() reads arg0 from [esp+4] — a pointer to the /bin/sh string",
         tags=[("ESP", BANDS["fakeret"][0])],
         show_libc=True, show_ret_arrow=True, show_arg_arrow=True,
         hl="arg0", int_arrows=[("arg0", "binsh", "#b26b00", "amber")]),
    dict(name="4_shell", frame=1,
         alt="system('/bin/sh') executes — the attacker gets a shell",
         tags=[],
         show_libc=True, show_ret_arrow=True, show_arg_arrow=True,
         hl=None, int_arrows=[("arg0", "binsh", "#b26b00", "amber")]),
]


for n, fr in enumerate(FRAMES):
    body = [HEAD.format(W=W, H=H, step=n, alt=fr["alt"]),
            ruler(), connectors(), payload_column(), stack_column(fr["frame"])]
    if fr["show_libc"]:
        body.append(libc_box())
    if fr["show_ret_arrow"]:
        # arrow from the "ret" band to the libc box
        body.append(jump_arrow("ret", 448, 191))
        body.append(f'<text class="note" x="{STK_X + STK_W + 8}" y="{BANDS["ret"][0] + BANDS["ret"][1] / 2 - 8}">ret → EIP</text>')
    if fr["show_arg_arrow"]:
        # dashed arrow from libc box up to the "/bin/sh" string
        body.append(
            f'<path d="M 577,158 L 577,{BANDS["binsh"][0] + BANDS["binsh"][1] / 2} '
            f'L {STK_X + STK_W + 4},{BANDS["binsh"][0] + BANDS["binsh"][1] / 2}" '
            f'stroke="#b26b00" stroke-width="1.8" fill="none" stroke-dasharray="6 4" marker-end="url(#amber)"/>')
    for a_key, b_key, colour, marker in fr["int_arrows"]:
        body.append(internal_arrow(a_key, b_key, colour, marker))
    if fr["hl"]:
        body.append(highlight(fr["hl"]))
    for text, y in fr["tags"]:
        body.append(tag(text, y))
        body.append(f'<path d="M{TAG_X},{y} L{STK_X + STK_W + 3},{y}" stroke="#b26b00" stroke-width="2" fill="none" marker-end="url(#amber)"/>')
    body.append(legend(fr["frame"]))
    # shell annotation on frame 4
    if fr["name"] == "4_shell":
        body.append(
            f'<text class="libct" x="577" y="260" style="fill:#1a7a3a;font-size:22px">$ /bin/sh 🐚</text>')
        body.append(
            f'<text class="libcs" x="577" y="284">system("/bin/sh") runs — shell!</text>')
    body.append("</svg>")
    path = os.path.join(OUT, f"ret2libc_{fr['name']}.svg")
    with open(path, "w") as fh:
        fh.write("\n".join(body) + "\n")
    print("wrote", os.path.basename(path))

