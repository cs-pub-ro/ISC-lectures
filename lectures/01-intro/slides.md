---
routerMode: hash
download: 'slides.pdf'
theme: ../../isc-theme
colorSchema: light
selectable: false
title: Lecture 1 — Introduction to Computer Security
info: |
  ## ISC — Lecture 1 · Introduction
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
---

# Introduction to Computer Security

<font size=4>Cybersecurity properties, threats, and defenders</font>

<div class="mt-12 py-1" @click="$slidev.nav.next" hover:bg="white op-10">
  Press Space for next slide
</div>

<!--
Welcome students, introduce the course and its source.
-->

---
layout: quote
class: text-center
---

# Honor Code

'My job is to talk to you, and your job is to listen. If you finish first, please let me know.'

— Harry Hershfield
---

# Selected topics

<v-clicks>

1. Introduction. Cybersecurity properties.
2. Cryptography fundamentals.
3. Authentication & Key Establishment.
4. Access Control & OS Security.
5. Application Security (Buffer overflow).
6. Malware and anti-malware techniques.
7. Web Applications Security (DB security, XSS).
8. Local Network Security.
9. Public Key Infrastructure.
10. Remote Network Security.
11. Privacy Preserving Technologies.
12. Hardware Security.
13. Wireless Security.
14. AI/ML security.

</v-clicks>

---

# Materials

- Course page: [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
- Roadmap: [roadmap.sh/cyber-security](https://roadmap.sh/cyber-security)

---

# Grading

- **1 p** — Homework 1
- **1 p** — Homework 2
- **1 p** — 11 Labs *(11 × 0.1818...)*
- **3 p** — Final practical exam *(ultimul lab, no LLMs)*
- **4 p** — Final written exam (TBD)

**Total = 10 pts** · Min. **5 pts** to pass the course.

---
layout: section
---

# Introduction to cyber security

---

# Outline

- CIA + Non-repudiation
- Threat modeling
    - STRIDE
    - Dolev–Yao

---

# What is security? (theory)

> Cybersecurity is, given an **attacker's model** and a specific **context**, the technique to control **who** may **use** or **modify** the **data**.

---
layout: quote
---

# What is security? (reality)

'Measures designed to produce a feeling of security rather than the reality.'

— Bruce Schneier

---

# Theory vs. reality — economics

- Don't protect **$1B** with encryption that can be broken for **$1M**.
- Don't spend **$10M** to protect **$1M**.

> "A CRYPTO NERD'S IMAGINATION: let's build a million-dollar cluster to crack it!
> WHAT WOULD ACTUALLY HAPPEN: drug him and hit him with this $5 wrench
> until he tells us the password."

---

# Romanian legislation (not translated)

- **Legea 286/2009, art. 360:**
  - (1) Accesul, fără drept, la un sistem informatic — închisoare de la 3 luni la 3 ani sau amendă.
  - (2) Fapta din alin. (1), comisă în scopul obținerii de date informatice — 6 luni – 5 ani.
  - (3) Sistem informatic la care accesul este restricționat/interzis pentru anumite categorii de utilizatori — 2 – 7 ani.
- Introducerea / modificarea / ștergerea de date, restricționarea accesului, împiedicarea funcționării unui sistem informatic — 2 – 7 ani.

---
layout: section
---

# Security properties

---

# Rainbow Series (1985)

Department of Defense **TCSEC** (Trusted Computer System Evaluation Criteria):

- **Orange Book** — computers:
  - D = no security
  - C1 = discretionary access control
  - B3 = trusted path & tamperproof
  - A1 = formal methods & supply-chain security
- **Red Book** — networks · **Green Book** — passwords

[See the series](https://en.wikipedia.org/wiki/Rainbow_Series)

---

# Common Criteria (CC)

> "Cybersecurity meets bureaucracy" ;)

Two kinds of evaluation:

- **Protection Profile (PP)** — describes a family of products
- **Security Target (ST)** — addresses security issues relative to a specific product
- **EAL** — Evaluation Assurance Level

Examples:

- Canonical Ubuntu Server 18.04.4 → **EAL2**
- Microsoft Windows 11 / Server 2022 → **EAL4+**

[commoncriteriaportal.org](https://www.commoncriteriaportal.org/)

---

# TCSEC vs. CC

| TCSEC | CC    |
| ----- | ----- |
| D     | —     |
| —     | EAL1  |
| C1    | EAL2  |
| C2    | EAL3  |
| B1    | EAL4  |
| B2    | EAL5  |
| B3    | EAL6  |
| A1    | EAL7  |

---

# Security properties — basics

- **Confidentiality** — prevent reading of sensitive information by unauthorized parties
- **Integrity** — protection/detection of data from intentional or accidental modification
- **Availability** — assurance that systems and data are accessible by authorized users when needed

---

# Security properties — non-repudiation

- **Non-repudiation** — origin and/or reception of a message cannot be denied in front of a third party

---

# Security properties — privacy

- **Data protection / personal data privacy** — fair collection and use of personal data (in Europe, a set of legal requirements)
- **Anonymity / untraceability** — ability to use a resource without disclosing identity/location
- **Pseudonymity** — anonymity with accountability for actions

---

# Security properties — unlinkability

- **Unlinkability** — use a resource multiple times without others being able to link these uses together
  - *Bad examples:* HTTP "cookies", most cryptocurrencies
- **Unobservability** — use a resource without revealing this activity to third parties

---

# Security properties — control

- **Rollback** — return to a well-defined valid earlier state (backup, revision control, undo)
- **Audit** — monitoring and recording of user-initiated events to detect and deter violations
- **Copy protection / information flow control** — control the use and flow of information (Digital Rights Management)

---

# What is there to secure?

- Data at rest
- Data in transit
- Data in use

---
layout: section
---

# Assets, threats, attackers

---

# Assets

- What is interesting — and why — in the cyber world?
- Often **not** sufficiently accounted for → therefore hackable
  - E.g. because everyone wants fast business increases

::right::

# Exploitability

- Example: **Adobe Acrobat zero-day** (CVE-2021-28550)
  - "exploited in the wild in limited attacks targeting Adobe Reader users on Windows"

---

# Terms & attack surface

- **bug** → **vulnerability** → **exploit**

Attack surface:

- External
- Internal
  - Malicious
  - Mistake

---

# Attackers

From pranksters to professionals:

- **Script kiddies**
- Attackers — white / grey / black
- Vulnerability brokers vs. cybercriminals
- Bug bounty programs
- **Hacktivists**
- National state adversaries
- **Advanced persistent threat (APT)**

---

# Types of threats

- **Social engineering**
- **Network threats**
- **Denial of Service**
- **Malware**
  - Trojan
  - Keyloggers
  - Rootkits
  - Worms
  - Fileless malware
  - Ransomware
  - Virus
  - ...

---

# Types of malware

- **Virus** — infects files, spreads when opening them
- **Worm** — automatically infects other systems!
- **Logic bomb**
- **Trojan horse** — user must explicitly open crafted exe
- **Remote Access Trojan**
- **Ransomware** — money for your data!
- **Spyware** — NSA, Pegasus, etc.
- **Adware** — the entire WWW :(

---

# Attackers vs. defenders

- Anti-viruses?
- In general, it's **easier to destroy than to create** — `rm -rf /`
- Attacker evasion:
  - Encryption and tunneling
  - Resource exhaustion
  - Traffic fragmentation
  - Protocol-level misinterpretation
  - Traffic substitution

---

# Attacker models

- **Dolev–Yao**
  - formal networking analysis
  - crypto is unbreakable
- **STRIDE**
  - [en.wikipedia.org/wiki/STRIDE_model](https://en.wikipedia.org/wiki/STRIDE_model)

---

# TTPs, IoC, IoA

- **TTPs** — Tactics, Techniques, and Procedures (generalized statement of adversary behavior)
  - Campaign strategy (tactics) · attack vectors (techniques) · specific tools (procedures)
- **IoC** — Indicators of Compromise (specific evidence of intrusion)
- **IoA** — Indicators of Attack

[attack.mitre.org](https://attack.mitre.org/matrices/enterprise/)

---
layout: section
---

# Security by design

---

# Security building blocks

- **Cryptography**
- **Access control**

::right::

# Zero Trust

- Never trust, always verify.

---

# Least privilege

- Complex systems are more difficult to secure.
- The more applications deployed, the more possible vulnerabilities.

::right::

# Weakest link

> An infrastructure is as strong as its weakest link.

---

# Security vs. the world (complexity)

- **Downside:** complexity brings vulnerability
  - How secure is a 1000-computer network with >1000 users and 200 applications?
  - How secure is a simple button?
- Still, we **do** need complexity to accomplish our tasks

---
layout: section
---

# Security administration

---

# Security administration

- Paperwork is important — "dosar cu șină"
- Policies
- Standards
- Guidelines
- Procedures
- Baselines

---

# Security policy

- A **contract** stating how to protect information assets
- Should be **S.M.A.R.T.** (Specific, Measurable, Achievable, Timely)
- Management instructions guiding present & future decisions
- Must be **communicated** to others
- Defines what "security" means for an organization

---

# Policy example

- **Authentication policy** — who may access resources + verification procedures
- **Password policy** — minimum requirements, regular changes
- **Acceptable Use Policy (AUP)** — allowed applications/uses + ramifications
- **Remote access policy** — how remote users connect and what they can reach
- **Maintenance policy** — OS and application update procedures
- **Incident handling procedures** — how incidents are handled

---

# Supporting documents

- **Standards** — dictate specific minimum requirements in policies
- **Guidelines** — suggest the best way to accomplish certain tasks
- **Procedures** — provide the method by which a policy is accomplished (the instructions)

---

# Policy design exercise

Your protected health data is stored in a personal electronic folder. Design a policy to protect it.

- What is there to protect?
- From whom?
- How long should data be saved?
- What about **CIA**?
- Enter **HIPAA** rules and regulations.

---

# References

- Phishing history: [phishing.org](http://www.phishing.org/history-of-phishing/)
- OWASP appsec: [owasp.org](https://www.owasp.org/)
- Mat Honan story: [wired.com](http://www.wired.com/2012/08/apple-amazon-mat-honan-hacking/)
- Spamhaus DDoS: [arstechnica.com](http://arstechnica.com/security/2013/03/spamhaus-ddos-grows-to-internet-threatening-size/)
- NIST Rainbow Series (DoD 85): [csrc.nist.gov](https://csrc.nist.gov/)

---
layout: end
class: text-center
---

# Thank you

**Further reading:**
*Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
