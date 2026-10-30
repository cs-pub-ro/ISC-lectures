#!/usr/bin/env python3
"""leak_libc() -- find where the dynamic loader mapped libc in a live process.

A real exploit needs a *memory disclosure* bug to learn this address.  As the
owner of the process we just started, we can simply read its map file: that is
the "leak" used by the demo scripts here.

Returns (libc_base, path_to_libc).
"""
import time


def leak_libc(pid, timeout=3.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        with open(f"/proc/{pid}/maps") as f:
            for line in f:
                if "libc.so.6" in line:
                    return int(line.split("-")[0], 16), line.split()[-1]
        time.sleep(0.02)  # the process may not have finished exec()'ing yet
    raise RuntimeError(f"pid {pid}: no libc mapping found")
