# Build the two lab targets for buffovf-demo.md.
#
#   make                  # vuln64 + vuln32
#   make vuln64           # only the 64-bit one
#   make CC32=./cc32.sh   # 32-bit build without a system-wide multilib toolchain
CFLAGS   = -g -O0 -fno-stack-protector -no-pie -fno-pie -fno-pic
# -mpreferred-stack-boundary=2 keeps buf[64] at exactly rbp-0x40 (offset 68);
# with gcc's default 16-byte alignment the frame grows 8 bytes and it is 76.
CFLAGS32 = $(CFLAGS) -mpreferred-stack-boundary=2
CC32    ?= gcc -m32

all: vuln64 vuln32

# NX stays on (no -z execstack): we want the "no shellcode" scenario.
vuln64: vuln.c
	$(CC) $(CFLAGS) $< -o $@

vuln32: vuln.c
	$(CC32) $(CFLAGS32) $< -o $@

# Same programs, but with an executable stack (the pre-2004 classic).
execstack: vuln.c
	$(CC) $(CFLAGS) -z execstack $< -o vuln64_exec
	$(CC32) $(CFLAGS32) -z execstack $< -o vuln32_exec

clean:
	rm -f vuln32 vuln64 vuln32_exec vuln64_exec

# Docker lab environment (gcc + multilib + gdb + pwndbg + pwntools + dotfiles)
IMAGE ?= buffovf
TAG   ?= latest

image:
	docker build -t $(IMAGE):$(TAG) .

run: image
	docker run --rm -it -v "$$(pwd):/workspace" $(IMAGE):$(TAG)

clean-image:
	docker rmi $(IMAGE):$(TAG) || true

.PHONY: all execstack clean image run clean-image
