---
routerMode: hash
download: 'slides.pdf'
theme: ../../isc-theme
colorSchema: light
selectable: false
touying:
  preset: isc
title: Lecture 4 — Authorization & Access Control
info: |
  ## ISC — Lecture 4 · Authorization & Access Control
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
src: ../_shared/intro.md#1
---
---
layout: cover
title: "Lecture 4: Authorization & Access Control"
subtitle: "Access control models, DAC vs MAC, RBAC, OS security and the human factor"
---

::default::

<!--
Welcome students. This lecture covers who is allowed to do what on a system:
access control models from theory (PEI, BLP, Biba) to practice (POSIX, OAuth).
-->

---
layout: section
---

# Access control

---
layout: two-cols
class: cols-55-45
---

# Examples of Access Control

<v-clicks>

- **Social Networks** — access to personal information
- **Web Browsers** — access restricted between web domains (same origin policy)
- **Operating Systems** — one user cannot arbitrarily access/kill another user's files/processes
- **CPU Memory Protection** — code in one region (e.g., Ring 3) cannot access data in a more privileged region (e.g., Ring 0)
- **Firewalls** — if a packet matches certain conditions, it is dropped

</v-clicks>

::right::

<div class="img-col" style="padding: 3em;">
<img src="./images/gandalf_shall_not_pass.jpg" />
</div>

---

# PEI Model [1]

Access control = **P**olicy – **E**nforcement – **I**mplementation:

- **Policy** — intent / goals, rules;
- **Enforcement** — access mediation layer;
- **Implementation** — technologies, protocols etc.

---

# Vocabulary

Basic abstractions:

- **Subjects** — entities who wish to access a certain object
- **Objects** — the resources being accessed (e.g., a file, a network packet)
- **Rights** / **permissions** — the different modes of access / actions allowed (e.g., reading, writing)

<!--
Emphasize: subject = active, object = resource, rights = how subject can use object.
-->

---

# Users and Principals

- A **Principal** is a **user** authenticated in a context
- Principals are the **unit of access control and authorization**
- The user can create principals with **downgraded privileges**

---

# Principals and subjects

- A **subject** is a **program executing on behalf of a principal**

Example:

- You (user) → authenticate (principal) → run a browser (subject acting for you)

---

# Users ↔ Principals relationship

- Users and Principals: **One-To-Many** relation
- Allows **accountability** of user's actions
- Use the **least privileges** required for a task
- E.g., **service accounts / API keys** (authentication w/o password)
- For simplicity, a principal and a subject can be treated as identical concepts

---

# Objects

- An **object** is anything on which a subject can perform operations (mediated by rights)
- Usually objects are **passive**:
  - File
  - Directory (Folder)
  - Memory segment
- But **subjects (e.g., processes) can also be objects**, with specific operations:
  - `kill`, `suspend`, `resume`

---
layout: section
---

# Access control models

---

# Access control enforcement — overview

- **DAC** (Discretionary Access Control) — access rights can be **propagated** from one subject to another; possession of a right is sufficient to allow access
- **MAC** (Mandatory Access Control) — access based on **system-wide policies** (security labels), changeable only by the administrator
- **RBAC** (Role-Based Access Control) — can be configured as both MAC or DAC; access based on **roles**

---

# Access control enforcement — more

- **ABAC** (Attribute-Based Access Control) — **properties of a subject/object/action** are used when access decisions are made
- **UCON** (Usage Control) — generalization of access control to include:
  - authorization, **obligations**, **conditions** (e.g., quotas)
  - continuity and mutability of attributes

---

# Discretionary Access Control (DAC)

- **No precise definition**
- Basically, DAC allows access rights to be propagated **at the subject's discretion**
- Often has the notion of **owner** of an object
- Used in **UNIX, Windows**, etc.

<!--
Ask: is "discretion" a feature or a bug? We'll see both sides.
-->

---

# Formal rule representation

Let $S$ be the set of all subjects, $O$ the set of all objects, $P$ the set of all permissions:

- Access control = a set $A \subseteq S \times O \times P$
- Adding a permission → add a triplet to $A$
- Revoking → delete the triplet

---

# Matrix representation

- An **access control matrix** $(M_{s,o})$: rows = subjects, columns = objects
- Element $M_{s,o} \subseteq P$ = permissions subject $s$ has for object $o$

<br>

| Subjects | catalog.csv | cat-anonim.txt | /dev/kmem | /sbin/sudo | PID 1001 |
| -------- | ----------- | -------------- | --------- | ---------- | -------- |
| Root     | rw          | rwx            | -         | rwx        | kill     |
| mihai    | rw          | rw             | -         | rx         | kill     |
| student  | -           | r              | -         | rx         | -        |
| guest    | -           | -              | -         | -          | -        |

---

# Access Control Lists (ACL)

- An **ACL** is a set $\{A_o \mid o \in O\}$ — **one element for each object**
- Each element = the pairs $(s, p)$ of subjects $s$ with permission $p$ for that object

::right::

```text
catalog.csv
  root:  rw
  mihai: rw

cat-anonim.txt
  root:  rw
  mihai: rw
  student: r

/sbin/sudo
  root:  rwx
  mihai: rx
  student: r
```

---

# Classic POSIX Model

- **Objects:** files · **Permissions:** R, W, X + specials (SUID/SGID/sticky)
- **Subjects:** users, groups, others
- Stored as **bit masks** (written in base 8 — octal) on inodes
- Bit mask: `111|101|100` → octal **754**
- Modern OSes support **full Access Control Lists** (multiple subjects!)

```bash
➜ ls -l /usr/bin/sudo
-rwsr-xr-x 1 root admin 92K Jan 18 08:05 /usr/bin/sudo
```

---

# Capability lists

- Alternate implementation: each **user stores a list of his capabilities**, instead of objects storing ACLs
- Storing capabilities = giving each subject **tokens** that grant access to the permissions they are entitled to

|         | catalog.csv | cat-anonim.txt | /dev/kmem | /sbin/sudo | PID 1001 |
| ------- | ----------- | -------------- | --------- | ---------- | -------- |
| Root    | rw          | rw             | rw        | rwx        | kill     |
| mihai   | rw          | rw             | -         | rx         | kill     |
| student | -           | r              | -         | rx         | -        |
| guest   | -           | -              | -         | -          | -        |

<!--
Transpose of the matrix representation: rows are now users holding tokens.
-->

---

# Capability examples

- **Posix API descriptors:**

```c
int fd = open("/etc/passwd", O_RDWR);
// Code flow: fork() -> setuid/setgid() -> exec()
// -> new process inherits fd (the authorization 'token')
```

- **Linux:** per-process capabilities
- **Windows:** Security Identifier (**SID**) with associated capabilities in an Active Directory

---

# ACL vs. Capabilities

- **ACL** require **authentication** of subjects
- **Capabilities** do not require authentication, but require:
  - **unforgeability**
  - **control of propagation** (usually via cryptography)
- The **Confused Deputy Problem** [N. Hardy, 1988]
  - E.g.: Cross-Site Scripting/Forgery (XSS / CSRF), setuid privilege escalation (e.g., `sudo`)
- **Solution:** bundle resource access together with capability

---

# DAC problems

- DAC philosophy: subjects can determine who has access to **their** objects
- But there's a difference between **trusting a person** and **trusting a program**
- Copies of a file are **not controlled**
- **Trojan Horse attack** [1970]
- Solution: use **MAC** ☺

::right::

# Trojan Horse / buggy software

- When a subject (e.g., buggy software) is exploited, it executes **the attacker's code**, while using **the privileges of the user who started it**
- → **DAC-only systems cannot be trusted with classified information!**

<!--
The horse carries the attacker's payload with the victim's keys.
-->

---

# Principle of Least Privilege

- Each subject should have **only the necessary privileges**
- Privilege elevation / dropping:
  - **Unix:** `setuid()` / `setgid()` system calls
- **Example POSIX scenario:**
  - Only root can open ports < 1024
  - Web server (e.g., `apache2`) starts as **root**
  - Opens log files, sockets, etc. — then **drops root** (user → `www-data`)
- Modern alternative: **Linux capabilities** (`CAP_NET_BIND_SERVICE`)
- Better yet: **DAC + MAC!**

---

# Mandatory Access Control (MAC)

- Access rights assigned based on **regulations by a central authority**
- Implemented using a **'reference monitor'**
- Small **Trusted Computing Base (TCB)** [John Rushby, 1981]
  - Kernel < Hypervisor < Hardware
- **TOCTTOU** (Time Of Check To Time of Use) problem:
  - Authority checks access to an object
  - Attacker **replaces the object** in the meantime
  - Privileged subject operates on an **attacker-controlled object**

---

# MAC implementations — Type Enforcement

- E.g.: **SELinux**
- Subjects → grouped in **domains** (labels)
- Objects → grouped in **types** (another/same kind of labels)
- **Domain-Domain + Domain-Type permissions**
- If a MAC rule fails → **DAC not checked, access denied!**

```text
# TE rule: allow passwd_t shadow_t : file {read, write …}
# ls -Z /etc/shadow
-rw-r----- root root  system_u:object_r:shadow_t  shadow
# ps -aZ
gigel:user_r:passwd_t  16532 pts/0 00:00:00 passwd
```

<!--
Contrast with DAC: MAC rules take precedence — no DAC fallback.
-->

---
layout: section
---

# Multi-level security

- Multi-level security (MLS)
  - **Bell-LaPadula** (BLP)
  - **Biba** Model
- **Chinese Wall**

---

# Multi-level security (MLS)

- The capability of a system to carry information with **different sensitivities**, e.g. *Top Secret*
- **Bell-LaPadula (BLP)** Model [1973]
- **Biba** Model

---

# Bell-LaPadula (BLP) Model

- Captures **confidentiality** requirements only. 
- Modelled as **transitions through a set of states**, from an initial state
- **State** = current access set, access matrix, level function
- State transition rules describe how the system goes from one state to another
- Each object has a **classification level**
- Each subject $s$ has a **security clearance**

---

# BLP Model — security properties

A state is **secure** if:

- **A) Simple Security Property (SS):** no subject may **read** data at a **higher** level (no read up)
- **B) \* (Star)-Property (SP):** no subject may **write** data at a **lower** level (fear of Trojan Horse / information leaks — no write down)

> A system is secure **if and only if** every reachable state is secure.

<!--
Mnemonic: read up blocked, write down blocked.
-->

---

# BLP in practice

- FreeBSD `mac_mls` + SELinux MLS policy (used by gov. defence / NATO)
- Data diodes / one-way gateways (e.g., SCADA systems -- no write down)
- Separation kernels (avionics / automotive)
- VM compartmentalization (Qubes OS / sandboxes)

---

# BLP problems

- **No communication** (e.g., acknowledging) from High to Low
- Not all components can be enforced by BLP — e.g., **memory management** needs access to all levels
  - Called **'trusted subjects'** (part of TCB)
- **Covert channels** cannot be blocked by the star-property

---

# Biba Model

Integrity is also very important:

- Each subject (process) has an **integrity level**; each object has an **integrity level**; levels are **ordered**
- **NO read down; NO write up** — BLP **upside down**

---

# Biba Model in practice

- Windows Integrity Control + Mark of the Web:
  * Internet Explorer/Edge Protected Mode, Office Protected View cannot execute;
  * Overwriting system-protected files is denied by lower processes!
- iOS Gatekeeper: unsigned applications cannot execute!

<!--
Biba protects integrity (from untrusted low), BLP protects confidentiality (from snooping high).
-->

---

# Chinese Wall [1989, Brewer and Nash]

**Read rule** — $S$ can read $O$ only if:

- $O$ is in the **same company dataset** as some object previously read by $S$ (*within the wall*), **or**
- $O$ belongs to a **conflict-of-interest class** in which $S$ has read nothing (*in the open*)

**Write rule** — $S$ can write $O$ only if:

- $S$ can read $O$ by the simple security rule, **and**
- no object can be read that is in a **different company dataset** than the one being written

<!--
Motivating example: auditors must not mix data of competing companies.
-->

---
layout: section
---

# RBAC

---

# Group-based access control

- Real-world security policies are **dynamic**
- E.g., a user is promoted → their rights must change (deleted, added, etc.)
- **RBACs are more flexible: can simulate MAC & DAC!**

---

# Roles as policy

A role brings together:

- a collection of **users**
- a collection of **permissions**

- These collections can be **modified independently**
- A user can be a member of **many roles**
- Each role can have **many users** as members
- Roles may be **hierarchical**

---

# RBAC shortcomings

- Role granularity may lead to **role explosion**
- Role design and engineering is **difficult and expensive**
- Assignment of users/permissions to roles is **cumbersome**
- Adjustment based on local/global **situational factors** is difficult

---
layout: section
---

# Auth Implementations

---

# OAuth

- Open **Authorization**, not **Authentication**!**
- Users **delegate API access** to third-party services **without giving their password**
  - E.g., give Google Calendar API access to a task management app
- **JSON Web Token (JWT)** — may contain subject IDs + capability lists
- Authorization flow: client-side / server-side
- **OpenID Connect:** popular extension for **SSO Authentication**
  - Identity Provider authorizes access to `/userinfo` endpoint via token
    → third-party service **identifies you**

---

# Writing authorization code

Tons of conditionals?

```python
if is_admin or (can_read(obj.parent) and can_write(obj)): ...
```

**Solution:** use language features & authorization frameworks:

```python
@authorize.create(Article)
def create_article(name):
    # implementation here

@authorize.read
def read_article(article):
    # implementation here
```

---

# Best practices

<v-clicks>

- Design during the **early requirements phase**
- Model as **subjects, objects, permissions**
- Use an **appropriate policy model** (DAC, RBAC, ABAC, etc.)
- Use **middleware / framework** if available
- If not, create your own! **Do NOT copy-paste duplicate code!**
- Implement **resource limits / quotas**
- **Sanitize/normalize user input!!!**

</v-clicks>

::right::

```python
requested_file.startswith("/home/user/share/")
# but requested_file = "/home/user/share/../../../etc/shadow"
```

<!--
The classic path traversal: prefix checks are not normalization.
-->

---
layout: section
---

# The Human Factor

---

# Security and humans

- Security policies must be in place … **and must be followed**
- Regardless of how strong (and expensive) your secure deployment is:
  - Humans can still write their **passwords on post-it notes**
  - Humans can still **give their passwords** to anyone they trust
  - Humans can still open **tempting attachments** …

---

# Social engineering

<img src="./images/social_engineering.jpg" style="width: 40%; margin-left: 2em; float: right;" />

- **Non-technical intrusion** — tricking people to break security policies
- **Manipulation** — relies on false confidence:
  - Everyone trusts someone
  - Authority is usually trusted by default
  - Non-technical people don't want to admit their lack of expertise → they ask fewer questions
- **Most people are eager to help**
  - When the attacker poses as a fellow employee in need
- People are **not aware** of the value of the information they possess
- **Vanity, authority, eavesdropping** — they all work
- When successful, social engineering **bypasses ANY kind of security**

---

# Types of phishing

**By technology used:**

- **Smishing** (SMS)
- **Vishing** (Voice)
- **Email phishing**
- **Angler phishing** (via social networks)

**By target:**

- **Watering Hole** phishing (people visiting a certain website)
- **Spear phishing** (a specific organization)
- **Whaling** (C-level of a specific organization)

---

# Resources

- [1] [PEI Framework](https://profsandhu.com/confrnc/misconf/collabcom09_pei_pre.pdf)
- [2] [Cornell CS5430 — Non-Logical Access Control](http://www.cs.cornell.edu/courses/cs5430/2011sp/NL.accessControl.html)
- [3] [CS526 — Access Control slides](http://cnitarot.github.io/courses/cs526_Spring_2015/s2014_526_ac.pdf)
- [4] [Rutgers CS419 — Access Control notes](https://people.cs.rutgers.edu/~pxk/419/notes/access.html)

---
class: text-center
---

# Thank you

**Further reading:**
*Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
