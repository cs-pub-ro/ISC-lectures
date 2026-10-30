# buffovf-scripts

Everything behind the bonus lab `../buffovf-demo.md`: the vulnerable
target, the exploits, the screenshot generator and the animation generator.

```
vuln.c                          the target: gets() into a 64-byte stack buffer
Makefile                        builds vuln64 / vuln32 with the "convenient" flags
cc32.sh                         build 32-bit without a system-wide multilib toolchain
exploit_ret2win.py              step 1: overwrite the return address with &win()
exploit_ret2libc_x86.py         step 2 (32-bit): pad | system | junk | &"/bin/sh"
exploit_ret2libc_x86_64.py      step 2 (64-bit): pad | pop rdi | &"/bin/sh" | ret | system
libc_leak.py                    read the libc base out of /proc/<pid>/maps
term_shot.py                    record a real terminal session in a pty -> HTML card
shoot.mjs                       screenshot that card with Playwright (PNG)
make_shots.py                   runs all lab sessions -> ../images/buf_*.png
gen_stack_svg.py                generates ../images/stack_overflow_*_animated.svg
```

## Quick start

```console
$ make                                   # needs gcc; for vuln32: gcc-multilib
$ python3 -m pip install --user pwntools

$ ./exploit_ret2win.py ./vuln64           # [+] win() reached
$ ./exploit_ret2libc_x86_64.py            # uid=1000(you) ... pwned
$ ./exploit_ret2libc_x86_64.py -i         # keep the /bin/sh interactive
```

`vuln32` needs 32-bit development files. On Debian/Ubuntu:

```console
$ sudo apt install gcc-multilib libc6-dbg
```

If you cannot install them (e.g. inside a container), extract the i386 packages
somewhere and use the wrapper:

```console
$ make CC32=./cc32.sh M32_PREFIX=/path/to/sysroot
```

## The lab, step by step

```console
$ gcc -g -O0 -fno-stack-protector -no-pie -fno-pie vuln.c -o vuln64
$ python3 -c 'from pwn import *; print(cyclic(80).decode())' > /tmp/cyclic64
$ gdb -q ./vuln64
pwndbg> set context-sections ''
pwndbg> run < /tmp/cyclic64
pwndbg> info registers rip rbp rsp
pwndbg> x/2gx $rsp
pwndbg> cyclic -l $rbp            # 64 -> the return address is at 64 + 8 = 72
```

32-bit: identical, with `x/2wx $esp` and `cyclic -l $eip` (answer: 68).

## Notes on the environment

- **ASLR is not disabled.** `setarch -R` / `set disable-randomization` fail with
  *Operation not permitted* in many containers, so the exploit scripts "leak"
  the libc base from `/proc/<pid>/maps` — exactly what a real exploit does with
  a memory-disclosure bug. With ASLR off you can skip the leak and hardcode the
  addresses.
- **nx is on** on purpose (`Makefile` does not pass `-z execstack`): the point of
  the last section is reusing libc instead of running injected code.
- The 32-bit cards in the deck were linked against an extracted glibc (see
  `cc32.sh`); on a normal machine the `RUNPATH` line will be empty.

## Regenerating the slide assets

```console
$ python3 -m venv .venv && .venv/bin/pip install ansi2html
$ npm install playwright-chromium && npx playwright install chromium

$ ./gen_stack_svg.py                 # ../images/stack_overflow_{x86,x86_64}_animated.svg
$ PYTHON=.venv/bin/python ./make_shots.py          # ../images/buf_*.png
$ PYTHON=.venv/bin/python ./make_shots.py offset   # only the matching shots
```

`make_shots.py` runs each session in a pty (so colours and wrapping are real),
drops the noisy startup lines (`NOISE`), renders the transcript as a terminal
card and screenshots it with Playwright. Useful env vars: `LAB_DIR` (where the
binaries are, default `.`), `OUT_DIR` (default `../images`), `SUBS`
(`from=to` path rewrites, e.g. to shorten a sysroot path).

The SVG animations are pure CSS keyframes: 12 s per loop, three phases
(normal frame → the write running past the buffer → the hijacked return).
They also animate inside `<img src="...">`, which is how Slidev embeds them;
a PDF export shows a single frozen phase.
