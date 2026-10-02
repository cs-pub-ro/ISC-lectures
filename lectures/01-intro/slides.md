---
layout: cover
routerMode: hash
download: 'slides.pdf'
theme: ../../isc-theme
colorSchema: light
selectable: false
touying:
  preset: isc
title: Lecture 1 — Introduction to Computer Security
info: |
  ## ISC — Lecture 1 · Introduction
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
src: ../_shared/intro.md#1
---
---
layout: cover
title: "Lecture 1: Introduction"
subtitle: "Properties, threats and defenders"
---

::default::

---
layout: section
class: text-center
---
# Course Logistics
---

# Honor Code

'My job is to talk to you, and your job is to listen. If you finish first, please let me know.'

— Harry Hershfield

![Sleeping Student](./images/Sleeping.jpg)
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
- Roadmap: [https://pauljerimy.com/security-certification-roadmap/](https://pauljerimy.com/security-certification-roadmap/)

---

# Lab Logistics
- EG101 (Microsoft)
- Have a VM with Linux / Kali for easier access
- We use OpenStack 

---

# Grading

- **1 p** — Homework 1
- **1 p** — Homework 2
- **1 p** — 11 Labs *(11 × 0.1818...)*
- **3 p** — Final practical exam *(ultimul lab, no LLMs)*
- **4 p** — Final written exam (TBD)

**Total = 10 pts** · Min. **5 pts** to pass the course.

---

# AI/LLM agents prompt

- "Act as a patient security tutor, not a solver. Help me understand the concepts and approach, point me to the right tools (bash / python-based), and give me hints and guiding questions — but don't write out the full solution or complete code. Nudge me just enough to keep me trying, and only reveal more if I tell you I'm still stuck."

---
layout: section
---

# Introduction to cyber security

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

<br/>
<div class="flex flex-col items-center slideimg" style="text-align: center;">

![XKCD #538](./images/xkcd_security_538.png)

<a style="font-style: italic; font-size: 9pt;"
	href="https://xkcd.com/538/">https://xkcd.com/538/</a>
</div>

<style>
.slideimg {
	p { width: 40%; margin: 0.3em auto; text-align: center; }
	img { display: inline; }
}
</style>

---

# Romanian legislation (not translated)

- **Legea 286/2009, art. 360:**
  - (1) Accesul, fără drept, la un sistem informatic — închisoare de la 3 luni la 3 ani sau amendă.
  - (2) Fapta din alin. (1), comisă în scopul obținerii de date informatice — 6 luni – 5 ani.
  - (3) Sistem informatic la care accesul este restricționat/interzis pentru anumite categorii de utilizatori — 2 – 7 ani.
- Introducerea / modificarea / ștergerea de date, restricționarea accesului, împiedicarea funcționării unui sistem informatic — 2 – 7 ani.

---

# Rules of Engagement

> **With great power comes great responsibility.**

- In this course, you will learn techniques used by real attackers.
- **The Golden Rule:** NEVER attack a system you do not own or do not have explicit, written permission to test.
- **Do NOT** scan or attack UPB infrastructure (`curs.pub.ro`, `ocw.cs.pub.ro`, Eduroam) or your peers.

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

<div style="width: 10em; margin: 0 auto;">

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

</div>

---

# Security properties — basics

- **Confidentiality** — prevent reading of sensitive information by unauthorized parties
- **Integrity** — protection/detection of data from intentional or accidental modification
- **Availability** — assurance that systems and data are accessible by authorized users when needed
- CIA Triad

---

# Security properties — non-repudiation

- **Non-repudiation** — origin and/or reception of a message cannot be denied in front of a third party

---

# Security properties — privacy

- **Data protection / personal data privacy** — fair collection and use of personal data (in Europe, a set of legal requirements)
- **Anonymity / untraceability** — ability to use a resource without disclosing **source** identity/location
- **Pseudonymity** — anonymity with accountability for actions

---

# Security properties — unlinkability

- **Unlinkability** — use a resource multiple times without others being able to link these uses together
  - *Bad examples:* HTTP "cookies", most cryptocurrencies
- **Unobservability** — use a resource without revealing this activity to third parties

---

# Security properties — control

- **Rollback** — return to a well-defined valid earlier state (backup, revision control, undo)
- **Copy protection / information flow control** — control the use and flow of information (Digital Rights Management)

---

# The AAA Framework

Alongside the CIA Triad, Access Control relies on **AAA**:

- **Authentication:** *Who are you?* (Proving identity via Passwords, Biometrics, MFA).
- **Authorization:** *What are you allowed to do?* (Permissions, Access Control Lists).
- **Accounting (Audit):** *What did you do?* (Logs, Traces, Forensics).

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
layout: two-cols
---

# Assets

- What is interesting — and why — in the cyber world?
- Often **not** sufficiently accounted for → therefore hackable
  - E.g. because everyone wants fast business increases

::right::

<br/><br/><br/><br/><br/><br/>

<v-click>

### Exploitability

- Example: **Adobe Acrobat zero-day** (CVE-2021-28550)
  - "exploited in the wild in limited attacks targeting Adobe Reader users on Windows"

</v-click>

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
  - Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege
  - [en.wikipedia.org/wiki/STRIDE_model](https://en.wikipedia.org/wiki/STRIDE_model)

---

# TTPs, IoC, IoA

- Adversary Tactics and Techniques, Knowledge base
  - [attack.mitre.org](https://attack.mitre.org/matrices/enterprise/)

- **TTPs** — Tactics, Techniques, and Procedures (generalized statement of adversary behavior)
  - Campaign strategy (tactics) · attack vectors (techniques) · specific tools (procedures)
- **IoC** — Indicators of Compromise (specific evidence of intrusion)
- **IoA** — Indicators of Attack

---
layout: section
---

# Security by design

---

# Risk Management 101

Security is fundamentally about Risk Management. You cannot secure everything 100%.

> **Risk = Threat × Vulnerability × Impact**

- **Threat:** Someone or something that can cause harm (e.g., Ransomware gang, malicious insider).
- **Vulnerability:** A weakness in the system (e.g., unpatched software, exposed port).
- **Impact (Asset Value):** The cost if the asset is compromised (e.g., data loss, downtime).

*If any of these is zero (e.g., a vulnerable server that is completely disconnected from the network), the Risk is zero.*

---

# Security building blocks

- **Cryptography**
- **Access control**

---

# Kerckhoffs's Principle

- **"No security through obscurity."**
- Claude Shannon's Maxim: *"The enemy knows the system."*

---

# Zero Trust

- Never trust, always verify.

---

# Least privilege

- Complex systems are more difficult to secure.
- The more applications deployed, the more possible vulnerabilities.

---

# Weakest link

- An infrastructure is as strong as its weakest link.


---

# Defense in Depth

- **Concept:** Never rely on a single point of security. Controls *will* fail.
- **Example:** 
  1. Network Firewall
  2. Web Application Firewall (WAF)
  3. Strong Authentication (MFA)
  4. Database Encryption (Data at rest)

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
- Enter **GDPR/NIS2** rules and regulations.

---

# References

- Phishing history: [phishing.org](http://www.phishing.org/history-of-phishing/)
- OWASP appsec: [owasp.org](https://www.owasp.org/)
- Ro hospitals [https://www.cyberbreaches.org/en/incidents/romanian-hospitals-2024](https://www.cyberbreaches.org/en/incidents/romanian-hospitals-2024) 
- CrowdStrike [https://www.techtarget.com/whatis/feature/Explaining-the-largest-IT-outage-in-history-and-whats-next](https://www.techtarget.com/whatis/feature/Explaining-the-largest-IT-outage-in-history-and-whats-next) 
- Log4Shell [https://www.sophos.com/en-us/blog/log4shell-hell-anatomy-of-an-exploit-outbreak] (https://www.sophos.com/en-us/blog/log4shell-hell-anatomy-of-an-exploit-outbreak)
- NIST Rainbow Series (DoD 85): [csrc.nist.gov](https://csrc.nist.gov/)

---

# Further reading

- *Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)
[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
