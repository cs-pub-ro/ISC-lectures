#!/usr/bin/env python3
"""term_shot.py -- record a real terminal session in a pty and turn it into a
terminal-style HTML card (dark window, rounded corners, traffic lights).

The terminal recording keeps the colours produced by gdb/pwndbg, so the cards
look exactly like the session they were captured from.

Capture:  Term(...).send() a list of commands, get raw ANSI bytes back.
Render:   ansi2html converts the bytes to styled HTML; shoot.mjs screenshots
          the card with Playwright.

Requires: `pip install ansi2html` (see ../README.md).
Usage:    python3 term_shot.py --out /tmp/x.html --title "gdb" --cmd 'gdb -q ./vuln64' ...
"""
import argparse
import os
import pty
import re
import select
import struct
import subprocess
import sys
import fcntl
import termios
import time

CARD_CSS = """
  * { box-sizing: border-box; }
  body { margin: 0; background: transparent; }
  .term {
    display: inline-block; min-width: 620px;
    background: #0b0e14; border-radius: 14px;
    border: 1px solid #2b3240; overflow: hidden;
    box-shadow: 0 18px 40px rgba(0,0,0,.35);
    font-family: "Liberation Mono", "DejaVu Sans Mono", ui-monospace, monospace;
  }
  .bar {
    display: flex; align-items: center; gap: 8px; padding: 9px 14px;
    background: #151a23; border-bottom: 1px solid #2b3240;
  }
  .dot { width: 11px; height: 11px; border-radius: 50%; display: inline-block; }
  .r { background: #ff5f57; } .y { background: #febc2e; } .g { background: #28c840; }
  .title { margin-left: 8px; color: #8b98a9; font-size: 12.5px; letter-spacing: .02em; }
  pre.ansi2html-content {
    margin: 0; padding: 14px 18px; color: #d5dae3; background: #0b0e14;
    font-family: inherit; font-size: 13.5px; line-height: 1.42;
    white-space: pre; tab-size: 8;
  }
  pre.ansi2html-content span { font-family: inherit; }
"""


class Term:
    """A tiny expect-style driver around a pty running an interactive bash."""

    def __init__(self, cols=104, rows=26, cwd=None, env=None):
        self.cols, self.rows, self.buf = cols, rows, b""
        full_env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "TERM": "xterm-256color",
            "HOME": os.environ.get("HOME", "/tmp"),
            "LANG": "C.UTF-8",
            "PS1": "$ ",
            "COLUMNS": str(cols),
            "LINES": str(rows),
        }
        full_env.update(env or {})
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack("HHHH", rows, cols, 0, 0))
        self.proc = subprocess.Popen(
            ["bash", "--noprofile", "--norc", "-i"],
            stdin=slave, stdout=slave, stderr=slave,
            cwd=cwd, env=full_env, start_new_session=True,
        )
        os.close(slave)
        self.master = master
        self._drain(0.4)  # swallow the first prompt

    def _drain(self, idle=0.6, timeout=90.0):
        """Read until the pty has been quiet for `idle` seconds."""
        start = last = time.time()
        while time.time() - start < timeout:
            r, _, _ = select.select([self.master], [], [], 0.05)
            if r:
                try:
                    chunk = os.read(self.master, 65536)
                except OSError:
                    break
                if not chunk:
                    break
                self.buf += chunk
                last = time.time()
            elif time.time() - last > idle:
                break
        return self.buf

    def send(self, cmd, idle=0.6, timeout=90.0):
        os.write(self.master, cmd.encode() + b"\n")
        self._drain(idle, timeout)
        return self

    def close(self):
        try:
            os.write(self.master, b"exit\n")
            self._drain(0.3, 3)
        except OSError:
            pass
        try:
            self.proc.kill()
        except ProcessLookupError:
            pass
        os.close(self.master)
        return self.buf


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def strip_lines(text, patterns):
    """Drop whole lines matching any regex (startup noise, banners, ...)."""
    if not patterns:
        return text
    lines = re.split(r"\r\n|\n", text)
    return "\n".join(ln for ln in lines if not any(re.search(p, ln) for p in patterns))


def wrap(text, cols):
    """Hard-wrap at `cols` *visible* characters, like a terminal would."""
    out = []
    for line in text.split("\n"):
        visible, buf, i = 0, [], 0
        while i < len(line):
            m = ANSI_RE.match(line, i)
            if m:                      # escape sequences take no space
                buf.append(m.group(0))
                i = m.end()
                continue
            buf.append(line[i])
            if line[i] != "\x00":
                visible += 1
            i += 1
            if visible == cols:
                out.append("".join(buf))
                buf, visible = [], 0
        out.append("".join(buf))
    return "\n".join(out)


def to_html(raw: bytes, title: str, cols: int, drop=None) -> str:
    from ansi2html import Ansi2HTMLConverter

    text = raw.decode("utf-8", errors="replace")
    text = strip_lines(text, drop)
    text = text.replace("\r\n", "\n").replace("\r", "")
    text = wrap(text, cols)
    text = re.sub(r"\x1b\[\?[0-9;]*[a-zA-Z]", "", text)  # bracketed paste & friends
    text = re.sub(r"\n?exit\n\Z", "\n", text)  # bash's parting "exit" echo
    # drop trailing blank lines so the card hugs the content
    text = re.sub(r"\n+\Z", "\n", text)
    conv = Ansi2HTMLConverter(dark_bg=True, inline=True, scheme="xterm")
    body = "<pre class='ansi2html-content'>" + conv.convert(text, full=False) + "</pre>"
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{CARD_CSS}</style></head><body>"
        f"<div class='term' data-cols='{cols}'>"
        f"<div class='bar'><span class='dot r'></span><span class='dot y'></span>"
        f"<span class='dot g'></span><span class='title'>{title}</span></div>"
        f"{body}</div></body></html>"
    )


def session(commands, title, out_html, cols=104, rows=26, cwd=None, env=None,
            idle=0.8, drop=None):
    """Run `commands` (list of strings) and write the rendered HTML card."""
    term = Term(cols=cols, rows=rows, cwd=cwd, env=env)
    for cmd in commands:
        term.send(cmd, idle=idle)
    raw = term.close()
    html = to_html(raw, title, cols, drop)
    with open(out_html, "w") as f:
        f.write(html)
    return html


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", default="terminal")
    ap.add_argument("--cols", type=int, default=104)
    ap.add_argument("--cwd", default=".")
    ap.add_argument("--cmd", action="append", default=[])
    a = ap.parse_args()
    session(a.cmd, a.title, a.out, cols=a.cols, cwd=a.cwd)
    print(f"wrote {a.out}")
