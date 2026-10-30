#!/usr/bin/env python3
"""make_shots.py -- capture the lab sessions used in buffovf-demo.md.

Every screenshot is a real terminal session recorded from a pty (term_shot.py)
and rendered to PNG with Playwright (shoot.mjs).

Setup (once):
    python3 -m venv .venv && .venv/bin/pip install ansi2html
    npm install playwright-chromium && npx playwright install chromium

Run from a directory that contains the compiled vuln32 / vuln64 binaries plus
the exploit_*.py scripts (i.e. the lab directory):

    ../buffovf-scripts/make_shots.py            # writes ./shots/*.png
    ../buffovf-scripts/make_shots.py checksec   # only matching shots

Environment knobs:
    PYTHON     python that has ansi2html        (default: ./.venv/bin/python)
    LAB_DIR    directory with the binaries      (default: current directory)
    OUT_DIR    where the PNGs go                (default: ../images)
"""
import os
import pwd
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.environ.get("LAB_DIR", os.getcwd())
OUT = os.environ.get("OUT_DIR", os.path.join(HERE, "..", "images"))
WORK = os.path.join(LAB, "_html")  # intermediate cards, safe to delete
PY = os.environ.get("PYTHON", os.path.join(LAB, ".venv", "bin", "python"))
NODE = os.environ.get("NODE", "node")

sys.path.insert(0, HERE)
import term_shot  # noqa: E402

CYCLIC = "python3 -c 'from pwn import *; print(cyclic(80).decode())' > /tmp/{f}"

# Lines that only add noise to a slide (gdb banner, ASLR warning, thread info).
NOISE = [
    r"pwndbg: ",
    r"warning: Error disabling address space randomization",
    r"\[Thread debugging using libthread_db enabled\]",
    r"Using host libthread_db library",
    r"^pwndbg> quit",
    r"^quit$",
    r"Reading symbols from",
    r"^Temporary breakpoint 1 at",
    r"Sections set to be empty",
    r"Set which context sections are displayed",
    r"nal, expressions, heap_tracker",
    r"^30\t\}",
]

SESSIONS = [
    dict(
        name="checksec_x86_64",
        title="pwndbg checksec — ./vuln64",
        cmds=["gdb -q ./vuln64", "checksec", "quit"],
    ),
    dict(
        name="checksec_x86",
        title="pwndbg checksec — ./vuln32",
        cmds=["gdb -q ./vuln32", "checksec", "quit"],
    ),
    dict(
        name="offset_x86_64",
        title="find the offset — x86_64",
        cols=100,
        cmds=[
            CYCLIC.format(f="cyclic64"),
            "gdb -q ./vuln64",
            "set context-sections ''",
            "run < /tmp/cyclic64",
            "info registers rip rbp rsp",
            "x/2gx $rsp",
            "cyclic -l $rbp",
            "quit",
        ],
    ),
    dict(
        name="offset_x86",
        title="find the offset — x86",
        cols=100,
        cmds=[
            CYCLIC.format(f="cyclic32"),
            "gdb -q ./vuln32",
            "set context-sections ''",
            "run < /tmp/cyclic32",
            "info registers eip esp ebp",
            "x/2wx $esp",
            "cyclic -l $eip",
            "quit",
        ],
    ),
    dict(
        name="ret2win_x86_64",
        title="ret2win — ./vuln64",
        idle=2.5,
        cmds=["./exploit_ret2win.py ./vuln64"],
    ),
    dict(
        name="ret2win_x86",
        title="ret2win — ./vuln32",
        idle=2.5,
        cmds=["./exploit_ret2win.py ./vuln32"],
    ),
    dict(
        name="got",
        title="the GOT of ./vuln64",
        cols=118,
        cmds=["gdb -q ./vuln64", "set context-sections ''", "start", "got", "plt", "quit"],
    ),
    dict(
        name="libc",
        title="libc is mapped — where is system()?",
        cols=122,
        cmds=[
            "gdb -q ./vuln64",
            "set context-sections ''",
            "start",
            "vmmap libc",
            "p/x (void *)system",
            "p/x (void *)gets",
            "quit",
        ],
    ),
    dict(
        name="gadget",
        title="looking for a 'pop rdi ; ret' gadget in libc",
        cols=100,
        idle=4.0,
        cmds=[
            'ROPgadget --binary /lib/x86_64-linux-gnu/libc.so.6 --only "pop|ret" '
            '| grep -m1 "pop rdi ; ret"',
        ],
    ),
    dict(
        name="ret2libc_x86_64",
        title="ret2libc — ./vuln64 (pwntools)",
        idle=3.0,
        cmds=["./exploit_ret2libc_x86_64.py"],
    ),
    dict(
        name="ret2libc_x86",
        title="ret2libc — ./vuln32 (pwntools)",
        idle=3.0,
        cmds=["./exploit_ret2libc_x86.py"],
    ),
]


def tidy(html_path):
    """Replace long absolute paths so the cards fit on a slide.

    SUBS="from=to,from2=to2" in the environment adds more substitutions
    (handy when the target links against a libc outside /lib).
    """
    subs = [(LAB, "~/lab")]
    for pair in filter(None, os.environ.get("SUBS", "").split(",")):
        src, _, dst = pair.partition("=")
        subs.append((src, dst))
    with open(html_path) as f:
        html = f.read()
    for src, dst in subs:
        html = html.replace(src, dst)
    with open(html_path, "w") as f:
        f.write(html)


def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(WORK, exist_ok=True)
    for s in SESSIONS:
        if only and only not in s["name"]:
            continue
        html = os.path.join(WORK, s["name"] + ".html")
        png = os.path.join(OUT, "buf_" + s["name"] + ".png")
        print(f"== {s['name']}")
        term_shot.session(
            s["cmds"], s["title"], html,
            cols=s.get("cols", 96), cwd=LAB, idle=s.get("idle", 0.8),
            drop=NOISE if not s.get("noisy") else None,
        )
        tidy(html)
        env = dict(os.environ)
        # HOME may be a throw-away dir (see term_shot); Playwright needs the real one
        cache = os.path.join(pwd.getpwuid(os.getuid()).pw_dir, ".cache", "ms-playwright")
        if os.path.isdir(cache):
            env.setdefault("PLAYWRIGHT_BROWSERS_PATH", cache)
        subprocess.run([NODE, os.path.join(HERE, "shoot.mjs"), html, png, "2"],
                       check=True, env=env)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
