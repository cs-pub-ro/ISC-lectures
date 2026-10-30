/*
 * vuln.c -- the target used by the buffer-overflow lab (buffovf-demo.md).
 *
 *   gcc -g -O0 -fno-stack-protector -no-pie -fno-pie vuln.c -o vuln64
 *   gcc -g -O0 -fno-stack-protector -no-pie -fno-pie -m32 vuln.c -o vuln32
 *
 * Everything that makes life easy here is switched off on purpose
 * (no stack canary, no PIE/ASLR for the binary itself, writable-but-not-
 * executable stack stays on: NX is enabled so we cannot just run shellcode).
 *
 * The bug: gets() copies an unlimited line of input into a 64-byte buffer.
 * gets() was removed from the C standard in C11 for exactly this reason, so
 * we have to declare it ourselves -- and the linker will warn us about it.
 */
#include <stdio.h>
#include <stdlib.h>

extern char *gets(char *);

/* A convenient "landing pad": jump here instead of shellcode. */
__attribute__((used)) void win(void) {
    puts("[+] win() reached -- the saved return address was overwritten");
    exit(0);
}

void greet(void) {
    char buf[64];         /* <-- the victim buffer */
    gets(buf);            /* <-- the bug: unbounded write */
    printf("Hello, %s!\n", buf);
}

int main(void) {
    greet();
    puts("bye");          /* never printed once the return address is smashed */
    return 0;
}
