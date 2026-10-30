#!/bin/sh
# cc32.sh -- build 32-bit binaries when the distro has no gcc-multilib.
#
# Point M32_PREFIX at a directory that contains an extracted i386 sysroot
# (crt*.o + libc under usr/lib32, libgcc under usr/lib/gcc/*/32), e.g.
#
#   sudo apt install gcc-multilib        # -- normally all you need
#   make CC32=./cc32.sh M32_PREFIX=...   # -- otherwise this wrapper
set -e
: "${M32_PREFIX:?set M32_PREFIX to the extracted i386 sysroot}"
G="$M32_PREFIX/usr/lib/gcc/x86_64-linux-gnu/14/32"
exec gcc -m32 \
    -I"$M32_PREFIX/usr/include/x86_64-linux-gnu" -I/usr/include/x86_64-linux-gnu \
    -B "$M32_PREFIX/usr/lib32" -B "$G" -L "$G" -L "$M32_PREFIX/usr/lib32" \
    -static-libgcc \
    -Wl,--dynamic-linker="$M32_PREFIX/usr/lib32/ld-linux.so.2" \
    -Wl,-rpath,"$M32_PREFIX/usr/lib32" \
    "$@"
