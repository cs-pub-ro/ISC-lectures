## [Introduction to Computer Security Lecture Slides](https://ocw.cs.pub.ro/courses/isc)

© 2024 by Mihai Chiroiu &amp; Florin Stancu

is licensed under Attribution-NonCommercial-ShareAlike 4.0 International

<!-- image -->

## Application Security

<!-- image -->

- 'My software never has bugs. It just develops random features.'
- 'You're holding it wrong!'
- 'Only one more bug left'

<!-- image -->

## Contents

- Software Vulnerabilities
- Cause &amp; classification
- Memory safety bugs + examples
- Defenses &amp; mitigations

<!-- image -->

## Software - the final frontier

- Access control and crypto are the bricks for building secure blocks
- Protocols/algorithms used to design useful blocks
- Software &amp; hardware implements all of the above
- Vulnerabilities - flaws allowing unintended access in a system

<!-- image -->

## Properties of a vulnerability

- Target application / system component
- Cause
- Severity
- Effect: Remote vs Local, e.g.:
- Remote Code Execution (RCE): enter system via network;
- Local Privilege Escalation: become root!
- Discovery/exploitation timeline (previously disclosed vs 0-day )

<!-- image -->

## Vulnerability causes

- Access control / business logic bugs
- Code injection
- Input validation (format string attacks, path traversal … )
- Memory safety : buffer overflow, dangling pointer, race condition, information leak, use after free etc.
- Weak crypto, side channel attacks …
- UI confusion
- And many more!

<!-- image -->

## Real World Examples

- EternalBlue - SMB Protocol Vulnerability (CVE-2017-0144) https://research.checkpoint.com/2017/eternalblue-everything-know
- Microsoft Exchange RCE Vulnerability (CVE-2021-26857) https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers
- Flash Player (CVE-2018-15982) https://securityaffairs.co/wordpress/78712/hacking/cve-2018-15982-flash-zero-day.html
- Log4J (CVE-2021-44228):

[https://blog.cloudflare.com/inside-the-log4j2-vulnerability-cve-2021-44228/](https://blog.cloudflare.com/inside-the-log4j2-vulnerability-cve-2021-44228/)

<!-- image -->

## Memory safety

- Microsoft: 70% of all high severity security bugs are memory safety issues [1]

<!-- image -->

<!-- image -->

## Intro: address space

- Userspace processes have virtual memory
- Compiler (linker) / OS decide where each segment goes.
- Address space layout has impact on application's security

<!-- image -->

<!-- image -->

## Intro: stack frame

- Stack: function arguments, saves CPU state (saved program counter, prev. frame, registers) and local variables:

```
int f(int x) { int n; int buf[10]; // ... } int main() { f(); // asm call f() <-- saves PC }
```

<!-- image -->

<!-- image -->

## Stack buffer overflow [2]

- Happens when a buffer's is written after its allocated size.

```
char buf[10]; char *input = 'This text is larger than expected'; strcpy(buf, input);
```

<!-- image -->

<!-- image -->

## Stack overflow (2)

<!-- image -->

<!-- image -->

<!-- image -->

## Stack overflow (3)

- ret instruction will pop the return address from the stack, then jump to it.
- CPU will execute the injected code (shellcode).

<!-- image -->

<!-- image -->

<!-- image -->

## Generic exploit steps [7]

- Find vulnerable input buffer (e.g., stack overflow)
- Find overwritable code pointer offset (e.g., saved EIP)
- Inject/reuse shell code (attacker-defined)
- Corrupt code pointer with attacker value!
- …
- ●
- all your base are belong to us! (CPU executes malicious instructions)

[7] SoK: Eternal War in Memory

<!-- image -->

<!-- image -->

## Stack exploit mitigations

- DEP (data execution prevention) / No-execute (NX) bit
- defeated by ROP (return oriented programming)
- Address space layout randomization
- defeated by memory leaks
- Stack Canaries
- defeated by memory leaks, side channels, data overwrites
- Shadow Stack

<!-- image -->

## Address Space Layout Randomization (ASLR)

- Implemented by most OSes
- Requires programs be compiled as Position-Independent Code
- Segments can only be randomized at startup!
- KASLR: randomize kernel-space!

## Address Space Layout Randomization example

<!-- image -->

<!-- image -->

## Stack Canaries

- Store random value between Saved EBP + Saved EIP
- Before ret, check this random value
- If modified, show error &amp; exit
- Weaknesses:
- memory leaks / side channels
- canary guessing

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Return to LibC

- Non-executable buffers? no problem!
- reuse existing functions
- Example: jump to execve() / system() etc.
- Reminder: call args from % EBP - 0x08 !

<!-- image -->

EBP -&gt;

<!-- image -->

4

buffer overflow write direction

## Return oriented programming

<!-- image -->

<!-- image -->

## What about exploiting .data ?

```
struct msg_funcs { (void)(*init)( struct message *msg); (void)(*print)( struct message *msg); (void)(*clear)( struct message *msg); } struct message { const struct msg_funcs *funcs; int len; char text[255]; };
```

```
struct message all_messages[10]; // ... int main() { // initialize modules … for (i=0; i<n; i++) { struct message *msg = &all_messages[i]; msg->funcs.init(msg); gets(msg->text); } }
```

<!-- image -->

## Object Oriented Security

- C++ (and other OOP languages) use virtual method tables for implementing polymorphism
- Attacker replaces VTable pointers to controlled memory
- When an object method is called, the function pointer is loaded from the attacker's VTable

<!-- image -->

<!-- image -->

## The Heap

- Dynamic Memory Allocation
- malloc / new
- GLibC: one master arena, multiple heaps, connected by linked lists
- Virtual memory allocated by OS (mmap or sbrk)
- malloc() =&gt; returns a free chunk of contiguous memory, fills metadata
- free() =&gt; clears/resets chunk + metadata

<!-- image -->

Thread Arena

<!-- image -->

## Dangling Pointer

- Return  /  store  a  pointer  to  an  object that  will  become  invalid  after  a  while (e.g., after free)
- Pointer still points to valid memory!
- Example:  returning  stack-local  pointers (function's frame becomes invalid after return)
- Dangerous, especially in OOP languages (e.g.: C++) =&gt; attacker can override objects' VTable!

```
char *parse_name(char *input) { char buf[100]; // process username return buf; } int main(...) { char *name = parse_name(argv[1]); process_more_data(argv[2]); if (strcmp(name, "admin") == 0) printf("Welcome master! \n "); }
```

<!-- image -->

## Use After Free

- Free the memory of an object (not needed anymore)
- Next, application allocates new object with attacker-controlled data
- Another  section  of  the  application uses  the  released  object  (still  has an old pointer stored in a variable)
- Are scripting languages safe?
- nope! -&gt;

```
// Adobe Flash exploit (ActionScript) ps = PSDK.pSDK; ps.release(); ms = new MediaResource("jack", 0x54336677, null ); try { ps.createDefaultContentFactory(); } catch (e:Error) { }
```

<!-- image -->

## Size checks vs integer overflows

```
#define HEADER_SIZE 128 uint16_t payload_len = user_payload_size(); uint8_t *buffer = malloc((uint16_t)(payload_len + HEADER_SIZE)); // user gives a valid payload len: 65534 // 65534 + 128 overflows! // => malloc allocates just 126 bytes... … read_input_into_buffer(buffer, len);
```

<!-- image -->

## Format string attacks

- printf("x=%d, y=%d, z=%d", x, y, z)
- What if the user controls format string?
- printf( user\_input )
- "%s" : read string from address arg.
- "%X %X %X … " : print args as hex
- Read-only vulnerability? Nope …
- "%n" :  consume  next  argument  as  address (pointer)  and  store  the  number  of  bytes written so far into it.

<!-- image -->

z y x 'fmt string' [ call printf ] saves EIP saved EBP [printf frame below]

## Just in Time + scripting =&gt; bytecode injection!

- Defeats W ⊕ X
- JIT Spraying:

```
VAL = (VAL + 0xA8909090)|0; VAL = (VAL + 0xA8909090)|0; => just in time compiles it into: 00: 05909090A8    ADD EAX, 0xA8909090 05: 05909090A8    ADD EAX, 0xA8909090 offset pointer with +1 byte: 03: 90    NOP 04: A805  TEST AL, 05
```

<!-- image -->

## Microsoft: BlueHatIL - Trends, challenge, and shifts in software vulnerability mitigation

## Drilling down into root causes

<!-- image -->

Top root causes since 2016:

#1: heap out-of-bounds

#2: use after free

Note: CVEs may have multiple root causes, so they can be counted in multiple categories

ISC

security crunch Stack corruptions are essentially dead Use after free spiked in 2013-2015 due to web browser UAF, but was mitigated by Mem GC

<!-- image -->

Heap out-of-bounds read, type confusion, &amp; uninitialized use have generally increased

Spatial safety remains the most common vuínerability category (heap out-of-bounds read/write)

#3: type confusion

#4: uninitialized use

11

## Control Flow Integrity

```
bool lt(int x, int y) { return x < y; { bool gt(int x, int y){ return x > y; { sort2(int a[], int b[], int len) { sort( a, len, lt ); sort( b, len, gt); }
```

<!-- image -->

<!-- image -->

## Data oriented attacks

- ●
- Memory overflows …
- non-control flow exploit?

```
int authenticated = 0; struct user_info *user_ptr = auth_users[last_idx]; int username[100]; gets(username); // meanwhile: check name & password if (authenticated) { user_ptr->valid = 1; strcpy(user_ptr->name, username); last_idx++; }
```

<!-- image -->

## Data oriented attacks (2)

- Memory overflows =&gt; non-control exploit
- Defeat W ⊕ X, stack canaries, CFI etc. (we don't alter code execution)!
- Data Oriented Programming Gadgets
- Pointer write access =&gt; write to ANY program variable!

```
int authenticated = 0; struct user_info *user_ptr = auth_users[last_idx]; int username[100]; gets(username); // meanwhile: check name & password if (authenticated) { user_ptr->valid = 1; strcpy(user_ptr->name, username); last_idx++; }
```

<!-- image -->

## Data integrity

- Easy: check bounds after each read / write of any variable!
- Softbounds + CETS
- compile-time transformations for enforcing spatial safety and temporal safety for C
- Huge overhead!
- Write Integrity Tracking / Data Flow Integrity / Data Space Randomization

<!-- image -->

## Protection mechanism summary

|                    | Policy              | Technique     | Weakness         | Perf.   | Comp.     |
|--------------------|---------------------|---------------|------------------|---------|-----------|
| protection Hijack  | W⊕R                 | Page flags    | JIT              | 1x      | pood      |
| protection Hijack  | Return integrity    | Stack cookies | Direct overwrite | 1x      | pood      |
| protection Hijack  | Address space rand. | ASLR          | Info-leak.       | 1.1x    | Good      |
| protection Hijack  | Control-flow integ. | CFI           | Over-approx.     | 1.4x    | Libraries |
| protection Generic | Memory safety       | SB+CETS       | None             | 2-4x    | pood      |
| protection Generic | Data integrity      | WIT           | Over-approx....  | 1.2x    | Libraries |
| protection Generic | Data space rand.    | DSR           | Over-approx....  | 1.3x    | Libraries |
| protection Generic | Data-flow integrity | DFI           | Over-approx.     | 2-3x    | Libraries |

<!-- image -->

## Is zero-vulnerabilities software possible?

## ● Yep! qmail [6]

- Mail Transfer Agent by David Bernstein , 1995 (last version: 1.03, 1998)
- Zero security vulnerabilities so far!

## ● Security practices:

- Keep It Simple Stupid (KISS)
- Unix Philosophy (modular development, each component KISS)
- ■ Separate functions into multiple unprivileged binaries
- Don't parse! Pass uniform/binary messages between programs!
- Write careful code, avoid libc (gets, printf, malloc/free etc.)!

<!-- image -->

## Memory safety defense?

- Scripting (Python, JS etc.) / Java / C#?
- not if you need performace (e.g., games, system level stuff) …
- Rust / GoLang / Zig (etc.)
- still able to write 'unsafe' code (e.g.,  syscalls / hardware interfaces / code optimizations)
- Stronger typing systems:
- Pure-functional programming (e.g., Haskell)
- ATS (write both code + mathematical proofs!) =&gt; HARDEST
- Backwards compatibility …
- no money to rewrite everything from scratch
- use secure coding practices, static analysis tools etc.
- hardware pointer/boundary checks (Intel MPX, ARM PAC)

<!-- image -->

## References

- [1] [https://www.zdnet.com/article/microsoft-70-percent-of-all-security-bugs-are-memory-safety-issues/](https://www.zdnet.com/article/microsoft-70-percent-of-all-security-bugs-are-memory-safety-issues/)
- [2] [https://security-summer-school.github.io/binary/](https://security-summer-school.github.io/binary/)
- [3] [https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf](https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf)
- [4] [https://sourceware.org/glibc/wiki/MallocInternals](https://sourceware.org/glibc/wiki/MallocInternals)
- [5] [https://infosecwriteups.com/use-after-free-13544be5a921](https://infosecwriteups.com/use-after-free-13544be5a921)
- [6] [https://blog.acolyer.org/2018/01/17/some-thoughts-on-security-after-ten-years-of-qmail-1-0/](https://blog.acolyer.org/2018/01/17/some-thoughts-on-security-after-ten-years-of-qmail-1-0/)
- [7] [SoK: Eternal War in Memory https://www.ieee-security.org/TC/SP2013/papers/4977a048.pdf](https://www.ieee-security.org/TC/SP2013/papers/4977a048.pdf)
- [8] [https://people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)

<!-- image -->