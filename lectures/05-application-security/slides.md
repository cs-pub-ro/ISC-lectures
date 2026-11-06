---
routerMode: hash
download: 'slides.pdf'
theme: ../../isc-theme
colorSchema: light
selectable: false
touying:
  preset: isc
title: Lecture 5 — Application Security
info: |
  ## ISC — Lecture 5 · Application Security
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
src: ../_shared/intro.md#1
---
---
layout: cover
title: "Lecture 5: Application Security"
subtitle: "Software vulnerabilities, memory safety bugs, and defenses"
---

::default::

---
layout: quote
class: text-center
---

<br>
<br>
<br>

# Developer optimism

_'My software never has bugs. It just develops random features.'_

_'You're holding it wrong!'_

_'Only one more bug left'_

---

# Contents

<v-clicks>

1. Software Vulnerabilities. Cause & classification.
2. Memory safety: stack overflow
3. Defenses & Mitigations
4. More on attacks: Beyond the stack

</v-clicks>

---
layout: section
---

# Software vulnerabilities

---

# Software — the final frontier

- Access control and crypto are the bricks for building secure blocks
- Protocols/algorithms used to design useful blocks
- Software & hardware implement all of the above
- **Vulnerabilities** — flaws allowing unintended access in a system

---

# Properties of a vulnerability

- Target application / system component
- Cause
- Severity
- Effect: **Remote** vs **Local**, e.g.:
  - **Remote Code Execution (RCE)** — enter system via network
  - **Local Privilege Escalation** — become root!
- Discovery/exploitation timeline: previously disclosed vs **0-day**

---

# Vulnerability causes

<v-clicks>

- Broken authentication/authorization control / business logic bugs
- Cryptography Fails
- Misconfiguration
- Injection (i.e., script / commands / code)
- Input validation (e.g., format string, path traversal)
- Memory safety (buffer overflow, race condition, leaks, use after free etc.)
- UI confusion
- And many more!

</v-clicks>

---

# Real world examples

- **EternalBlue** — SMB protocol vulnerability (CVE-2017-0144)
  [research.checkpoint.com](https://research.checkpoint.com/2017/eternalblue-everything-know)
- **Microsoft Exchange RCE** (CVE-2021-26857)
  [microsoft.com](https://www.microsoft.com/security/blog/2021/03/02/hafnium-targeting-exchange-servers)
- **Flash Player** (CVE-2018-15982)
  [securityaffairs.co](https://securityaffairs.co/wordpress/78712/hacking/cve-2018-15982-flash-zero-day.html)
- **Log4Shell** (CVE-2021-44228)
  [blog.cloudflare.com](https://blog.cloudflare.com/inside-the-log4j2-vulnerability-cve-2021-44228/)

---
layout: two-cols
class: cols-40-60
---

# Memory safety

- Microsoft: **70% of all high severity security bugs are memory safety issues** [1]

[1] [zdnet.com (2019)](https://www.zdnet.com/article/microsoft-70-percent-of-all-security-bugs-are-memory-safety-issues/)
::right::

<div class="img-col">

![](./images/memory_safety_root_causes_pie.svg)
*https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code*

</div>

---
layout: section
---

# Memory safety: stack overflow

---
layout: two-cols
---

# Intro: address space

- Userspace processes use **virtual memory**
- Compiler (linker) / OS decide where each segment goes
- Address space layout has impact on application's security

::right::

<div class="img-col">
<img src="./images/address_space_layout.svg" />
</div>

---
layout: two-cols
---

# The Stack

Stack holds function arguments, saved CPU state (saved program counter, previous frame, registers), and local variables:

ESP Extended Stack Pointer
EBP Extended Base Pointer

```c
int f(int x) {
  char buf[10]; int n; // ...
}

int main() {
  f(10); // asm: call f() <-- saves PC
}
```

::right::

<div style="padding: 1em;">
<img src="./images/stack_frame_layout.svg" />
</div>

---

# Intro: stack frame

The frame is not declared — it is built, one instruction at a time, by the x86 call convention:

<div class="cf-switch">

<v-switch transition="fade" :unmount="true">

<template #0>
<img src="./images/call_frame_01_push_arg.svg" alt="push the argument" />
</template>

<template #1>
<img src="./images/call_frame_02_call.svg" alt="call saves EIP" />
</template>

<template #2>
<img src="./images/call_frame_03_push_ebp.svg" alt="save the old EBP" />
</template>

<template #3>
<img src="./images/call_frame_04_mov_ebp.svg" alt="EBP := ESP" />
</template>

<template #4>
<img src="./images/call_frame_05_sub_esp.svg" alt="allocate the locals" />
</template>

<template #5>
<img src="./images/call_frame_06_leave.svg" alt="leave — tear down" />
</template>

<template #6>
<img src="./images/call_frame_07_ret.svg" alt="ret — back to the caller" />
</template>

</v-switch>

</div>

---
layout: two-cols
---

# Stack buffer overflow [2]

Happens when a buffer is written after its allocated size:

```c
char buf[16];
char *input = "AAAAAAAAAAAAAAAA<many times>";
strcpy(buf, input);
```

[https://security.cs.pub.ro/summer-school](https://security.cs.pub.ro/summer-school)

::right::

<div class="img-col">
<img src="./images/stack_buffer_overflow_direction.svg" />
</div>

---
layout: two-cols
class: cols-50-50
---

# Hijack using shellcode

When **input** can have sufficient size:

<div class="hj-code">

```c
void f(char *in) {
  char buf[16];
  strcpy(buf, in);  // no bounds check
  return;
}
```

</div>

<div v-click="2">

Note: `ret` is the one instruction that turns a data corruption into code execution:

<div class="hj-code">

```asm
    leave    ; esp = ebp ; pop ebp
    ret      ; eip = [esp]
```

</div>

_Spoilers: code injection won't work on a modern system (:_

</div>

::right::

<div class="hj-switch">

<v-switch transition="fade" unmount>
<template #0>
<img src="./images/hijack_0_payload.svg" />
<p class="hj-cap">
  The input overwrites the frame: 16 bytes fill <code>buf</code>, then
  4 bytes replace the saved <code>EBP</code> and 4 more the <b>return
  address</b>; everything after that is the NOP sled and the attacker's
  <b>machine code</b>.
</p>
</template>
<template #1>
<img src="./images/hijack_1_overwritten.svg" />
<p class="hj-cap">
  The return address now says <code>0xffffd6a0</code> — an address
  <b>inside the buffer</b>, where the NOP sled and the shellcode sit.
</p>
</template>
<template #2>
<img src="./images/hijack_2_ret_pops.svg" />
<p class="hj-cap">
  <code>leave</code> brings <code>ESP</code> back to the frame, 
  <code>ret</code> pops our word into <code>EIP</code>:
  the CPU thinks it is a normal return and proceeds to execute 
  the injected code -> PROFIT!
</p>
</template>
<template #3>
<img src="./images/hijack_3_sled.svg" />
<p class="hj-cap">
  The landing address does not have to be exact — 
  <code>0x90</code> is <code>nop</code>, so execution
  slides up into the payload.</p>
</template>
<template #4>
<img src="./images/hijack_4_exec.svg" />
<p class="hj-cap">
  The stack is decoded as code and, for example, 
  <code>execve("/bin/sh")</code> runs.</p>
<p><b>Note: this needs an executable stack!</b></p>
</template>
</v-switch>

</div>

<style>
.slidev-layout .hj-switch img { display: block; width: 100%; max-height: none; }
.hj-switch { position: relative; padding-left: 1.4em; }
.hj-cap { margin-top: 0.4em; min-height: 3.2em; font-size: 0.85em; line-height: 1.35; color: #3f4b52; text-align: left; }
.hj-code { --slidev-code-font-size: 13px; --slidev-code-line-height: 1.4; }
</style>

---

# No-execute (NX) / DEP

- The page-table entry gets an **NX / XD bit**: the stack and the heap are no longer executable
- Policy **W ⊕ X** — a page is either writable or executable, never both
- The shellcode still lands on the stack; the CPU simply faults when `ret` jumps to it
- On by default for stack/heap on x86-64 (AMD NX / Intel XD) and arm64, off for code pages
- Weakness: just wait for it... (ret2libc, ROP)
- Careful: JIT compilers keep their code pages **RWX** (cf. JIT spraying)

---
layout: two-cols
class: cols-45-55
---

# Return to LibC

When the stack is **not executable** (NX/DEP):

<div class="hj-code">

```c
void f(char *in) {
  char buf[16];
  strcpy(buf, in);  // no bounds check
  return;
}
```

</div>

<div v-click="2">

- Non-executable buffers? No problem!
- **Reuse** existing functions (`system()`, `execve()`)
- x86 cdecl: args from `[ESP+4]` = `[EBP+0x08]`
- Need `system()`'s address → a leak, or no-PIE

</div>

::right::

<div class="hj-switch">

<v-switch transition="fade" unmount>
<template #0>
<img src="./images/ret2libc_0_payload.svg" />
<p class="hj-cap">
  The input overwrites the frame: 16 bytes fill <code>buf</code>, then
  4 bytes replace <b>saved EBP</b>; the next 4 become the
  <b>return address</b> (<code>&system</code>), followed by a fake
  return and a pointer to <code>"/bin/sh"</code>.
</p>
</template>
<template #1>
<img src="./images/ret2libc_1_overwritten.svg" />
<p class="hj-cap">
  <code>strcpy</code> writes the entire payload onto the stack.
  The return address now says <code>0x0804a011</code> —
  the address of <b>system()</b> in libc.
</p>
</template>
<template #2>
<img src="./images/ret2libc_2_ret_pops.svg" />
<p class="hj-cap">
  <code>leave</code> restores <code>ESP</code>;
  <code>ret</code> pops <code>&system</code> into <code>EIP</code>.
  The CPU jumps <b>into libc</b> — nothing is executed from the stack.
</p>
</template>
<template #3>
<img src="./images/ret2libc_3_arg0.svg" />
<p class="hj-cap">
  <code>system()</code> reads its first argument from
  <code>[ESP+4]</code>: it finds the pointer to
  <code>"/bin/sh"</code> that the attacker planted.
</p>
</template>
<template #4>
<img src="./images/ret2libc_4_shell.svg" />
<p class="hj-cap">
  <code>system("/bin/sh")</code> runs — <b>the attacker gets a shell</b> 🐚
  <br/>NX is irrelevant: we only reused code that was already mapped <code>r-x</code>.
</p>
</template>
</v-switch>

</div>

<style>
.slidev-layout .hj-switch img { display: block; width: 100%; max-height: none; }
.hj-switch { position: relative; padding-left: 1.4em; }
.hj-cap { margin-top: 0.4em; min-height: 3.2em; font-size: 0.85em; line-height: 1.35; color: #3f4b52; text-align: left; }
.hj-code { --slidev-code-font-size: 13px; --slidev-code-line-height: 1.4; }
</style>

---

# ret2libc: x86 vs x86-64

<v-clicks>

- **x86 (32-bit)** — cdecl: arguments live **on the stack**
  - `ret` pops `&system` → the CPU calls `system()`
  - `system()` reads its argument from `[ESP+4]` — the next slot we control
  - **No gadget needed**: the calling convention does the work

</v-clicks>

<div style="--slidev-code-font-size: 14px;">

```c
payload = "A" × 20 + p32(system) + p32(0xDEADBEEF) + p32(binsh)
//        buf+EBP    ret addr       fake ret           arg0
```

</div>

<v-clicks>

- **x86-64** — System V ABI: first argument travels in **`RDI`**, not on the stack
  - We must load `RDI` with `&"/bin/sh"` **before** calling `system()`
  - Need a **gadget**: `pop rdi ; ret` — pops our value into `RDI`, then continues the chain
  - Extra `ret` gadget may be needed for **16-byte stack alignment** (`movaps` crash)

</v-clicks>

<div style="--slidev-code-font-size: 14px;">

```c
payload = "A" × 72 + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system)
//        buf+RBP    gadget          arg→RDI      alignment   call
```

</div>

---

# Dynamic linking: PLT & GOT

Programs call libc functions (`printf`, `system`, …) without containing their code — the **dynamic linker** resolves them at runtime.

<v-clicks>

- **PLT** — *Procedure Linkage Table*: one tiny stub per imported function, at **fixed addresses inside the binary**
  - `call printf` actually calls `printf@plt` — a trampoline
- **GOT** — *Global Offset Table* (`.got.plt`): one **pointer** per import
  - The PLT stub does `jmp *printf@got` — an indirect jump through the GOT entry
- **Lazy binding** (default): on the **first call**, the GOT entry still points back into the PLT → the dynamic linker resolves the real address and **patches the GOT**; later calls go straight to libc
- **`Partial RELRO`**: GOT stays writable → attacker can overwrite a GOT entry (**GOT hijack**)
- **`Full RELRO`** (`-z now`): all symbols resolved at startup, GOT mapped **read-only**

</v-clicks>

<div style="font-size: 0.82em; margin-top: 0.5em; color: #5b6670;">

The GOT is the bridge between **fixed** addresses (in a non-PIE binary) and **randomised** libc — a perfect leak target and a perfect hijack target.

</div>

---
layout: two-cols
class: cols-35-65
---

# Return oriented programming

- reuse **instructions** from exe/libs' code sections!
- defeats **NX**
- **Gadget**: short instruction sequence that ends in `ret`<br>
  (e.g. `pop rdi ; ret`)
- **Chain**: gadget addresses laid out on the stack<br>
  => each `ret` feeds the next gadget

::right::

<div class="img-col">
<img src="./images/rop_chain_x64.svg" alt="x86-64 ROP chain: return address replaced by a pop rdi ; ret gadget, the slot above it is the pointer to /bin/sh popped into RDI, then the address of libc system(), then the address of exit() as system's return address" />
</div>

---

# Common ROP gadgets (x86-64)

| Gadget | What it buys the attacker |
|--------|---------------------------|
| `ret` | skip a slot: fix 16-byte alignment (the `movaps` crash) |
| `pop rdi ; ret` | 1st argument, e.g. `system("/bin/sh")` |
| `pop rsi ; ret` / `pop rdx ; ret` | 2nd / 3rd argument (`execve`, `write`) |
| `pop rax ; ret` + `syscall ; ret` | ret2syscall - no libc needed |
| `leave ; ret` | stack pivot: `RSP := RBP`, move the chain somewhere else |
| `add rsp, 0x?? ; ret` | jump over slots, dodge bad bytes |
| `mov [rdi], rax ; ret` | write-what-where → overwrite a GOT entry / function pointer |

- Finding them: `ropper`/`ROPgadget` / pwntools `ROP(...)`
- Nothing useful in the binary? Look in **libc** / **ret2csu** (`__libc_csu_init`)

<style>
table { font-size: 0.85em; }
table td, table th { padding: 0.3em 0.6em; }
</style>

---
layout: two-cols
---

# Generalization of memory exploits [3]

[3] SoK: Eternal War in Memory — [ieee-security.org](https://www.ieee-security.org/TC/SP2013/papers/4977a048.pdf)

<v-clicks>

1. Find vulnerable input buffer (e.g., stack / heap / data)
2. Find overwritable code pointer offset (e.g., saved EIP, VTable / GOT / function pointer)
3. Inject/reuse shell code (attacker-defined)
4. Corrupt code pointer with attacker value!
5. … **all your base are belong to us!** (CPU executes malicious instructions)

</v-clicks>

::right::

<div class="img-col">
<img src="./images/sok_stack_smashing.svg" />
</div>

---
layout: section
---

# Defenses & Mitigations

---
layout: two-cols
---

# Memory Attack Mitigations

- **DEP (data execution prevention) / No-execute (NX) bit**
  - defeated by ROP (return oriented programming)
- **Address space layout randomization**
  - defeated by memory leaks
- **Stack Canaries**
  - defeated by memory leaks, side channels, data overwrites
- **Shadow Stack**

::right::

<div class="img-col">
<img src="./images/svg_attack_mitigations.svg" />
</div>


---
layout: two-cols
class: cols-45-55
---

# Address Space Layout Randomization (ASLR)

- Implemented by most OSes
- The OS randomizes the stack, heap, and shared libraries (libc) via ASLR
- Compiling with -fPIE -pie is required to randomize the base address of the main executable itself (.text, .data, .bss). (**Position-Independent Code**)
- Segments can only be randomized at startup!
- **KASLR** — randomize kernel-space!

::right::

<div class="img-col">
<img src="./images/aslr_rerandomization.svg" class="img-tall" />
</div>

---
layout: two-cols
class: cols-50-50
---

# Stack Canaries

- Store random value between locals and saved EBP/EIP
- Before returning, compiler inserts a check — if the canary changed → `__stack_chk_fail` → **abort**
- **Null-byte prefix**: the canary's LSB is `\x00` — designed to stop `strcpy`/`gets` from copying past it (the `\x00` terminates the string)

<v-clicks>

- Weaknesses:
  - **Format string leaks**: `%p` / `%lx` let the attacker read the canary (and ASLR bases) off the stack
  - **OOB read**: an out-of-bounds read past a buffer can disclose the canary before the overflow
  - **Canary brute-forcing**: only feasible in **fork-servers** (child inherits the parent's canary) — guess one byte at a time (256 × 7 tries on 64-bit, not 256⁷)
  - Does **not** protect non-`ret` pointers (function pointers, VTable, GOT)

</v-clicks>

::right::

<div class="img-col">
<img src="./images/stack_canary_layout.svg" />
</div>

---
layout: two-cols
---

# Control Flow Integrity

```c
bool lt(int x, int y) {
  return x < y;
}

bool gt(int x, int y) {
  return x > y;
}

sort2(int a[], int b[], int len) {
  sort(a, len, lt);
  sort(b, len, gt);
}
```

::right::

<div class="img-col">
<img src="./images/cfi_call_graph.svg" />
</div>

---

# Data integrity

- Easy: check bounds after each read/write of any variable!
- **SoftBound + CETS** — compile-time transformations enforcing spatial & temporal safety for C
  - Huge overhead!
- **Write Integrity Testing / Data Flow Integrity / Data Space Randomization**

---

# Protection mechanism summary

| Protection | Policy | Technique | Weakness | Perf. | Comp. |
|------------|--------|-----------|----------|-------|-------|
| Hijack | W⊕X | Page flags | JIT | 1x | good |
| Hijack | Return integrity | Stack cookies | Direct overwrite | 1x | good |
| Hijack | Address space rand. | ASLR | Info-leak. | 1.1x | good |
| Hijack | Control-flow integ. | CFI | Over-approx. | 1.4x | Libraries |
| Generic | Memory safety | SB+CETS | None | 2-4x | good |
| Generic | Data integrity | WIT | Over-approx. | 1.2x | Libraries |
| Generic | Data space rand. | DSR | Over-approx. | 1.3x | Libraries |
| Generic | Data-flow integrity | DFI | Over-approx. | 2-3x | Libraries |


---
layout: section
---

# Beyond the stack

---
layout: two-cols
---

# What about exploiting `.data`?

<div style="padding: 1em; font-size: 0.9em;">

```c
/* the "vtable": per-module function pointers */
struct msg_funcs {
  void (*init)(struct message *msg);
  void (*print)(struct message *msg);
  void (*clear)(struct message *msg);
};

/* each message = vtable pointer + payload */
struct message {
  const struct msg_funcs *funcs; // 4B/8B — who to call
  int len;                       // 4B
  char text[255];                // 255B — attacker input
};
```

</div>

::right::

<div style="margin-top: 2.7em; padding: 1em; font-size: 0.9em;">

```c
struct message all_messages[10]; // .data / .bss, not the stack

int main() {
  // initialize modules…
  for (i = 0; i < n; i++) {
    struct message *msg = &all_messages[i];
    msg->funcs->init(msg);  // call through the vtable…
    gets(msg->text);        // …then read 255+ bytes, unchecked
  }
}
```

<p style="font-size: 0.85em; line-height: 1.35; color: #3f4b52;">
  <code>text</code> is the last field of the element, so an over-long
  input keeps writing into <b>the next element</b> and overwrites its
  <code>funcs</code> pointer. That call happens on the <b>next iteration</b>:
  the CPU jumps to the attacker's function!
</p>

</div>

---

# Object Oriented Security

<div style="text-align: center;">
Virtual Tables (<b>VTable</b>)!
<img src="./images/vtable_polymorphism.svg" style="width: 700px; display: inline;" />
</div>

---
layout: two-cols
class: cols-55-45
---

# The Heap

- Dynamic memory allocation: `malloc` / `new`
- GLibC: one **main arena** + up to `8 × cores` thread arenas; each one allocates virt. mem. segments using `mmap` / `sbrk`
- Memory is managed in **chunks**: header (`prev_size`, `size`) + payload; free chunks sit in **bins** (doubly linked free lists)
- `malloc()` → cuts a free chunk, returns its payload
- `free()` → marks the chunk free and writes `fd` / `bk` bin pointers **into the payload** - the data itself is *not* wiped

[4] [GLibC Malloc Internals](https://sourceware.org/glibc/wiki/MallocInternals)

::right::

<div class="img-col">
<img src="./images/glibc_thread_arena.svg" />
</div>

---
layout: two-cols
---

# Dangling Pointer

- Return/store a pointer to an object that will become invalid after a while (e.g., after `free`)
- The pointer still points to valid memory!
- Example: returning stack-local pointers (frame becomes invalid after return)
- Dangerous, especially in OOP languages (e.g., C++) → attacker can override objects' VTable!

::right::

<div style="padding: 1em; font-size: 0.9em; margin-top: 2em;">

```c
char *parse_name(char *input) {
  char buf[100]; // process username
  return buf;
}

int main(...) {
  char *name = parse_name(argv[1]);
  process_more_data(argv[2]);
  if (strcmp(name, "admin") == 0)
    printf("Welcome master!\n");
}
```

</div>

---

# Use After Free

- Free the memory of an object (not needed anymore)
- Next, application allocates a new object with **attacker-controlled data**
- Another section of the application uses the released object (still has an old pointer stored in a variable)
- Are scripting languages safe? Nope!

<div style="font-size: 0.9em;">

```js
// Adobe Flash exploit (ActionScript)
ps = PSDK.pSDK;
ps.release();
ms = new MediaResource("jack", 0x54336677, null);
try {
  ps.createDefaultContentFactory();
} catch (e:Error) {
}
```

</div>

*[5] [infosecwriteups.com/use-after-free](https://infosecwriteups.com/use-after-free-13544be5a921)*

---

# Size checks vs integer overflows

```c
#define HEADER_SIZE 128
uint16_t payload_len = user_payload_size();
uint8_t *buffer = malloc((uint16_t)(payload_len + HEADER_SIZE));
// user gives a valid payload len: 65534
// 65534 + 128 overflows!
// => malloc allocates just 126 bytes...

read_input_into_buffer(buffer, payload_len);
```

---

# Format string attacks

- `printf("x=%d, y=%d, z=%d", x, y, z)`
- What if the user controls the format string? `printf(user_input)`
- `"%s"` — read string from an address argument
- `"%X %X %X …"` — print args as hex
- Read-only vulnerability? Nope …
- `"%n"` — consume next argument as address (pointer) and store the number of bytes written so far into it

[6] [exploit-db.com format string exploitation](https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf)

---
layout: two-cols
class: cols-40-60
---

# Just in Time + scripting 

=> shellcode injection!

- Defeats W ⊕ X: a JIT produces **writable and executable** pages
- **JIT spraying**: make the JIT emit data that is also valid machine code

::right::

```
VAL = (VAL + 0xA8909090)|0; // JS code

// JIT emits:
00: 05 90 90 90 A8      ADD EAX, 0xA8909090
05: 05 90 90 90 A8      ADD EAX, 0xA8909090

// the immediate 0xA8909090 is stored in Little-Endian
// and 0x90 is NOP, execution slides on...
01: 90 90 90            NOP x 3
04: A8 05               TEST AL, 0x05  ; harmless, 2 bytes
06: 90 90 90            NOP x 3
09: A8 05               TEST AL, 0x05
=> a NOP sled made of data!
```

<style>
code {font-size: 0.9em;}
</style>

---

# Data oriented attacks

- Memory overflows … non-control flow exploit?
- Defeats W ⊕ X, stack canaries, CFI etc. (we don't alter code execution!)
- **Data Oriented Programming Gadgets**
- Pointer write access → write to **ANY** program variable!

```c
int authenticated = 0;
struct user_info *user_ptr = auth_users[last_idx];
char username[100];
gets(username);
// meanwhile: check name & password
if (authenticated) {
  user_ptr->valid = 1;
  strcpy(user_ptr->name, username);
  last_idx++;
}
```

---
layout: two-cols
class: cols-45-55
---

# Drilling down into root causes

Microsoft (BlueHatIL 2019). Top root causes since 2016:

- **#1: heap out-of-bounds**
- **#2: use after free**
- **#3: type confusion**
- **#4: uninitialized use**

- Stack corruptions: essentially dead
- UAF: spiked 2013–15, killed by MemGC
- Spatial safety is still #1: heap OOB reads


::right::

<div class="img-col">
<img src="./images/bluehatil_cve_root_causes.jpg" />
</div>

---
layout: section
---

# Finishing thoughts

---

# Is zero-vulnerability software even possible?

Though a disputed claim, **qmail** [7]

- Mail Transfer Agent by Daniel J. Bernstein, 1995 (last version: 1.03, 1998)
- **Zero security vulnerabilities so far!** _in default configuration_
  - _In 2005, security researcher Georgi Guninski found an integer overflow in qmail_
- Security practices:
  - Keep It Simple, Stupid (KISS)
  - Unix Philosophy (modular development, each component KISS)
  - Separate functions into multiple unprivileged binaries
  - Don't parse! Pass uniform/binary messages between programs!
  - Write careful code, avoid libc (`gets`, `printf`, `malloc`/`free` etc.)!

[blog.acolyer.org](https://blog.acolyer.org/2018/01/17/some-thoughts-on-security-after-ten-years-of-qmail-1-0/)

---

# Memory safety defense?

- Scripting (Python, JS etc.) / Java / C#?
  - not if you need performance (e.g., games, system level stuff) …
- Rust / Golang (etc.)
  - still able to write 'unsafe' code (syscalls / hardware interfaces / optimizations)
- Stronger typing systems:
  - Pure-functional programming (e.g., Haskell)
  - ATS (write both code + mathematical proofs!) → HARDEST
- Backwards compatibility … no money to rewrite everything from scratch
- Use secure coding practices, static analysis tools etc.
- Hardware pointer/boundary checks Intel CET (Control-flow Enforcement Technology — Shadow Stack & IBT) and ARM MTE (Memory Tagging Extension).

---

# References

- [1] [Microsoft: 70% of security bugs are memory safety issues](https://www.zdnet.com/article/microsoft-70-percent-of-all-security-bugs-are-memory-safety-issues/)
- [2] [security-summer-school.github.io/binary](https://security-summer-school.github.io/binary/)
- [3] [SoK: Eternal War in Memory (PDF)](https://www.ieee-security.org/TC/SP2013/papers/4977a048.pdf)
- [4] [GLibC: Malloc Internals](https://sourceware.org/glibc/wiki/MallocInternals)
- [5] [Use After Free](https://infosecwriteups.com/use-after-free-13544be5a921)
- [6] [Linux format string exploitation (PDF)](https://www.exploit-db.com/docs/english/28476-linux-format-string-exploitation.pdf)
- [7] [Thoughts on security after ten years of qmail 1.0](https://blog.acolyer.org/2018/01/17/some-thoughts-on-security-after-ten-years-of-qmail-1-0/)
- [8] [toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)

---
layout: end
class: text-center
---

# Thank you

**Further reading:**
*Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
