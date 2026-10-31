#!/usr/bin/env python3
"""Generate the step-by-step x86 call-flow stack diagrams used by the
"Intro: stack frame" slide (``<v-switch>`` frames 0..6).

Run it after editing a step's stack state, highlight or note::

    python3 scripts/gen_call_flow.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")

W, H = 880, 322

# ---- geometry -------------------------------------------------------------
ASM_X, ASM_W = 14, 412
ASM_Y, LINE_H, LINE_Y0 = 38, 28, 56
COL_X, COL_W = 500, 240
MK_X, MK_W, MK_H = 770, 100, 30
CELLS = {
    "caller": (52, 40),
    "x":      (92, 36),
    "ret":    (128, 36),
    "saved":  (164, 36),
    "locals": (200, 60),
}
BOT = {k: y + h for k, (y, h) in CELLS.items()}   # bottom line = address of the slot

ASM = [
    ("  push  0x1c",        "   ; argument x"),
    ("  call  f",           ""),
    ("f: push  ebp",        "   ; save the caller's EBP"),
    ("   mov   ebp, esp",   ""),
    ("   sub   esp, 0x20",  "   ; 32 bytes for the locals"),
    ("   ...",              "   ; f() body: n, buf[10]"),
    ("   leave",            "   ; mov esp, ebp ; pop ebp"),
    ("   ret",              "   ; EIP = [ESP] ; ESP += 4"),
]

L_PUSH_X, L_CALL, L_PUSH_EBP = 0, 1, 2
L_MOV, L_SUB, L_LEAVE, L_RET = 3, 4, 6, 7

# ---- per-step state -------------------------------------------------------
# fill[cell] = "full" | "dim" | "empty",  highlight = asm line index
STEPS = [
    dict(name="01_push_arg", esp=BOT["x"], ebp=None, hl=L_PUSH_X,
         fill=dict(x="full"),
         note="push 0x1c &#8594; ESP &#8722;= 4, then [ESP] = x &#8212; the caller pushes arguments right-to-left"),
    dict(name="02_call", esp=BOT["ret"], ebp=None, hl=L_CALL,
         fill=dict(x="full", ret="full"),
         note="call f &#8594; ESP &#8722;= 4, then [ESP] = EIP, the return address"),
    dict(name="03_push_ebp", esp=BOT["saved"], ebp=None, hl=L_PUSH_EBP,
         fill=dict(x="full", ret="full", saved="full"),
         note="push ebp &#8594; ESP &#8722;= 4, then [ESP] = the caller's EBP"),
    dict(name="04_mov_ebp", esp=BOT["saved"], ebp=BOT["saved"], hl=L_MOV,
         fill=dict(x="full", ret="full", saved="full"),
         note="mov ebp, esp &#8594; EBP anchors the frame: [ebp+8] = x, [ebp+4] = return address"),
    dict(name="05_sub_esp", esp=BOT["locals"], ebp=BOT["saved"], hl=L_SUB,
         fill=dict(x="full", ret="full", saved="full", locals="full"),
         note="sub esp, 0x20 &#8594; ESP &#8722;= 32; the locals live at [ebp&#8722;4] &#8230; [ebp&#8722;32]"),
    dict(name="06_leave", esp=BOT["ret"], ebp=70, ebplab="EBP (caller)", hl=L_LEAVE,
         fill=dict(x="full", ret="full", saved="dim", locals="dim"),
         note="leave &#8594; mov esp, ebp ; pop ebp &#8212; locals released, the caller's EBP restored"),
    dict(name="07_ret", esp=BOT["x"], ebp=70, ebplab="EBP (caller)", hl=L_RET,
         fill=dict(x="full", ret="dim", saved="dim", locals="dim"),
         note="ret &#8594; EIP = [ESP] ; ESP += 4 &#8212; execution resumes in the caller at 0x08048a1f"),
]

FILL = {  # cell -> (fill, stroke, textcolour)
    "x":      ("#ffffff", "#9aa6ae", "#1a1a1a"),
    "ret":    ("#fbe6e3", "#b3261e", "#8c1d18"),
    "saved":  ("#e4eff1", "#176b87", "#0f4a5e"),
    "locals": ("url(#hatch)", "#2f6b34", "#245227"),
}
TEXT = {
    "caller": "caller's frame",
    "x":      "x = 0x0000001c",
    "ret":    "return address = 0x08048a1f",
    "saved":  "saved EBP = 0xffffd6f8",
    "locals": "locals: 32 bytes (n, buf[10])",
}

HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="x86 call flow step {{step}} of 7: {{alt}}">
<title>x86 call flow — step {{step}}</title>
<style>
  .panel{{fill:#f6f8fa;stroke:#e2e7ea;stroke-width:1.4}}
  .hl{{fill:#fdf1dc;stroke:#b26b00;stroke-width:1.2}}
  .ln{{font:15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#1a1a1a;dominant-baseline:central}}
  .lnp{{font:15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#3f4b52;dominant-baseline:central}}
  .lnf{{font:15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#b9c2c8;dominant-baseline:central}}
  .lnh{{font:600 15px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#7a4b00;dominant-baseline:central}}
  .cm{{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#8a949b;dominant-baseline:central}}
  .cell{{stroke-width:2;rx:3}}
  .ghost{{fill:#f4f6f7;stroke:#b6c0c6;stroke-width:1.6;stroke-dasharray:6 4}}
  .empty{{fill:#ffffff;stroke:#dfe5e8;stroke-width:1.4;stroke-dasharray:4 4}}
  .ct{{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;dominant-baseline:central}}
  .cap{{font:600 15px Inter,ui-sans-serif,system-ui,sans-serif;fill:#1a1a1a}}
  .sub{{font:13px Inter,ui-sans-serif,system-ui,sans-serif;fill:#8a949b}}
  .mk{{fill:#e4eff1;stroke:#176b87;stroke-width:2;rx:4}}
  .mkt{{font:600 14px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:#0f4a5e;text-anchor:middle;dominant-baseline:central}}
  .ar{{stroke:#176b87;stroke-width:2;fill:none}}
  .note{{font:15px Inter,ui-sans-serif,system-ui,sans-serif;fill:#0f4a5e}}
</style>
<defs>
  <marker id="m" viewBox="0 0 10 10" refX="9.5" refY="5" markerWidth="6.5" markerHeight="6.5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#176b87"/></marker>
  <pattern id="hatch" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
    <rect width="9" height="9" fill="#eaf2ea"/><line x1="0" y1="0" x2="0" y2="9" stroke="#c9dfc9" stroke-width="4"/>
  </pattern>
</defs>
'''


def asm_block(hl):
    out = [f'<text class="cap" x="{ASM_X}" y="26">x86 call convention</text>',
           f'<rect class="panel" x="{ASM_X}" y="{ASM_Y}" width="{ASM_W}" height="{8 * LINE_H + 14}" rx="5"/>']
    for i, (code, cmt) in enumerate(ASM):
        y = LINE_Y0 + i * LINE_H
        if i == hl:
            out.append(f'<rect class="hl" x="{ASM_X + 4}" y="{y - 12}" width="{ASM_W - 8}" height="24" rx="4"/>')
        cls = "lnh" if i == hl else ("lnf" if i > hl else "lnp")
        out.append(f'<text class="{cls}" x="{ASM_X + 14}" y="{y}" xml:space="preserve">{code}</text>')
        if cmt:
            out.append(f'<text class="cm" x="{ASM_X + 14 + 8 * 22}" y="{y}" xml:space="preserve">{cmt}</text>')
    return "\n".join(out)


def cell(key, state):
    y, h = CELLS[key]
    if key == "caller":
        out = [f'<rect class="ghost" x="{COL_X}" y="{y}" width="{COL_W}" height="{h}" rx="3"/>',
               f'<text class="ct" x="{COL_X + 12}" y="{y + h / 2}" fill="#5b6670" style="font-family:Inter,sans-serif;font-weight:400">{TEXT[key]}</text>']
        return "\n".join(out)
    if state == "empty":
        return f'<rect class="empty" x="{COL_X}" y="{y}" width="{COL_W}" height="{h}" rx="3"/>'
    fill, stroke, colour = FILL[key]
    dim = state == "dim"
    op = ' opacity="0.42"' if dim else ""
    dash = ' stroke-dasharray="5 4"' if dim else ""
    out = [f'<rect class="cell" x="{COL_X}" y="{y}" width="{COL_W}" height="{h}" rx="3" fill="{fill}" stroke="{stroke}"{dash}{op}/>']
    if key == "locals":
        out.append(f'<text class="ct" x="{COL_X + 12}" y="{y + h / 2}" fill="{colour}"{op}>{TEXT[key]}</text>')
    else:
        out.append(f'<text class="ct" x="{COL_X + 12}" y="{y + h / 2}" fill="{colour}"{op}>{TEXT[key]}</text>')
    return "\n".join(out)


def markers(esp, ebp, ebplab="EBP"):
    out = []
    if ebp is not None and ebp == esp:
        out.append(f'<rect class="mk" x="{MK_X}" y="{esp - MK_H / 2}" width="{MK_W}" height="{MK_H}"/>')
        out.append(f'<text class="mkt" x="{MK_X + MK_W / 2}" y="{esp}" style="font-size:13px">ESP = EBP</text>')
        out.append(f'<path class="ar" d="M{MK_X},{esp} L{COL_X + COL_W + 3},{esp}" marker-end="url(#m)"/>')
        return "\n".join(out)
    for lab, y in ((ebplab, ebp), ("ESP", esp)):
        if y is None:
            continue
        out.append(f'<rect class="mk" x="{MK_X}" y="{y - MK_H / 2}" width="{MK_W}" height="{MK_H}"/>')
        out.append(f'<text class="mkt" x="{MK_X + MK_W / 2}" y="{y}" style="font-size:{12 if len(lab) > 3 else 14}px">{lab}</text>')
        out.append(f'<path class="ar" d="M{MK_X},{y} L{COL_X + COL_W + 3},{y}" marker-end="url(#m)"/>')
    return "\n".join(out)


for n, st in enumerate(STEPS, 1):
    body = [HEAD.format(W=W, H=H, step=n, alt=st["name"].split("_", 1)[1].replace("_", " ")),
            asm_block(st["hl"]),
            f'<text class="cap" x="{COL_X}" y="26">stack</text>',
            f'<text class="sub" x="{COL_X + COL_W}" y="26" style="text-anchor:end">higher addresses on top</text>']
    for key in ("caller", "x", "ret", "saved", "locals"):
        body.append(cell(key, st["fill"].get(key, "empty")))
    body.append(markers(st["esp"], st["ebp"], st.get("ebplab", "EBP")))
    body.append(f'<text class="note" x="{ASM_X}" y="{H - 16}">{st["note"]}</text>')
    body.append("</svg>")
    path = os.path.join(OUT, f"call_frame_{st['name']}.svg")
    with open(path, "w") as fh:
        fh.write("\n".join(body) + "\n")
    print("wrote", path)
