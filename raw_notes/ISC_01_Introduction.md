# Introduction to Computer Security Lecture Slides

© 2025 by Mihai Chiroiu &amp; Florin Stancu is licensed under Attribution-NonCommercial-ShareAlike 4.0 International

ISC security crunch CC BY NC SA

# Introduction to cybersecurity

ISC security crunch CC BY NC SA

# Honor Code

*"My job is to talk to you, and your job is to listen. If you finish first, please let me know."*

Harry Hershfield

© Mihai Chiroiu

ISC security crunch

3

# Selected topics

1. Introduction. Cybersecurity properties.
2. Cryptography fundamentals.
3. Authentication &amp; Key Establishment.
4. Access Control &amp; OS Security.
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

© Mihai Chiroiu

4

https://roadmap.sh/cyber-security

ISC security crunch

CC BY NC SA

5

# Logistics

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

6

# Materials

- https://ocw.cs.pub.ro/courses/isc

ISC security crunch CC BY NC SA 7

# Grading

- **1p** - Homework 1
- **1p** - Homework 2
- **1p** - 11 Labs (11 x 0.1818181818...)
- **3p** - Final practical exam (ultimul lab, no LLMs)
- **4p** - Final written exam (TBD)
- **Total = 10p**
- **Min. 5p to pass the course.**

© Mihai Chiroiu ISC security crunch CC BY NC SA 8

# Introduction to cyber security

ISC security crunch CC BY NC SA

# Outline

- CIA + Non-repudiation
- Threat modeling
    - STRIDE
    - Dolev–Yao

# What is security? (theory)

- Cybersecurity is, given an **attacker's model** and a specific **context** , the technique to control **who** may **use** or **modify** the **data** .

© Mihai Chiroiu

ISC security crunch

11

# What is security? (reality)

- “Measures designed to produce a feeling of security rather than the reality.” Bruce Schneier

<!-- image -->

Windows Security dialog

© Mihai Chiroiu

ISC security crunch

12

# Theory vs. Reality

- Economics:
    - Don't protect $1B with encryption that can be broken for $1M.
    - Don't spend $10M to protect $1M.

A CRYPTO NERD'S IMAGINATION: HIS LAPTOP'S ENCRYPTED. LET'S BUILD A MILLION-DOLLAR CLUSTER TO CRACK IT. NO GOOD! IT'S 4096-BIT RSA! BLAST! OUR EVIL PLAN IS FOILED!

WHAT WOULD ACTUALLY HAPPEN: HIS LAPTOP'S ENCRYPTED. DRUG HIM AND HIT HIM WITH THIS $5 WRENCH UNTIL HE TELLS US THE PASSWORD. GOT IT.

© Mihai Chiroiu ISC security crunch CC BY NC SA 13

# Romanian Legislation (not translated)

- Introducerea, modificarea sau ștergerea de date informatice, restricționarea accesului la aceste date ori împiedicarea în orice mod a funcționării unui sistem informatic [...] se pedepsește cu închisoarea de la 2 la 7 ani.
- Lege 286/2009 – Art. 360
    - (1) Accesul, fără drept, la un sistem informatic se pedepsește cu închisoare de la 3 luni la 3 ani sau cu amendă.
    - (2) Fapta prevăzută în alin. (1), săvârșită în scopul obținerii de date informatice, se pedepsește cu închisoarea de la 6 luni la 5 ani.
    - (3) Dacă fapta prevăzută în alin. (1) a fost săvârșită cu privire la un sistem informatic la care [...] accesul este restricționat sau interzis pentru anumite categorii de utilizatori, pedeapsa este închisoarea de la 2 la 7 ani.

© Mihai Chiroiu

14

# Security properties

ISC security crunch CC BY NC SA 15

# Rainbow Series (1985)

- Department of Defense Trusted Computer System Evaluation Criteria (TCSEC)
- Orange Book – computers, examples:
    - D = No security
    - C1 = Discretionary Access Control
    - B3 = Trusted Path &amp; Tamperproof
    - A1 = Formal Methods &amp; Supply chain security
- Red Book – networks
- Green Book - passwords

https://en.wikipedia.org/wiki/Rainbow\_Series#//media/File:Rainbow\_series\_documents.jpg

ISC security crunch

CC BY NC SA

16

# Common Criteria for Information Technology Security Evaluation

- Cybersecurity meet bureaucracy ;)
- Two types kinds of evaluations:
    - A protection profile (PP) describes a family of products.
    - A security target (ST) addresses security issues relative to a specific product.
- EAL: Evaluation Assurance Level

ISC security crunch CC BY NC SA 17

# Common Criteria for Information Technology Security Evaluation

- https://www.commoncriteriaportal.org/
    - Canonical Ubuntu Server 18.04.4 : EAL2 (Evaluation assurance level 2), ALC\_FLR (Flaw remediation)
        - https://ubuntu.com/security/certifications/docs/16-18/cc
    - Microsoft Windows 11, Windows Server 2022: EAL4+
        - https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-platform-common-criteria

ISC security crunch CC BY NC SA

18

# TCSEC vs CC

| TCSEC   | CC   |
|---------|------|
| D       | -    |
| -       | EAL1 |
| C1      | EAL2 |
| C2      | EAL3 |
| B1      | EAL4 |
| B2      | EAL5 |
| B3      | EAL6 |
| A1      | EAL7 |

ISC security crunch

19

# Security properties - Basics

- Confidentiality
    - Prevent reading of sensitive information to unauthorized parties.
- Integrity
    - Protection/Detection of data from intentional or accidental modification.
- Availability
    - Assurance that systems and data are accessible by authorized users when needed.

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

20

# Security properties - Basics

- Non-repudiation – origin and/or reception of message cannot be denied in front of third party

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

21

# Security properties

- Data protection/personal data privacy
    - fair collection and use of personal data, in Europe a set of legal requirements
- Anonymity/untraceability
    - ability to use a resource without disclosing identity/location
- Pseudonymity
    - anonymity with accountability for actions.

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

22

# Security properties

- Unlinkability
    - ability to use a resource multiple times without others being able to link these uses together
    - Bad examples: HTTP “cookies” / most crypto-currencies
- Unobservability
    - ability to use a resource without revealing this activity to third parties

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

23

# Security properties

- Rollback
    - ability to return to a well-defined valid earlier state (backup, revision control, undo)
- Audit – monitoring and recording of user-initiated events to detect and deter security violations
- Copy protection, information flow control
    - ability to control the use and flow of information
    - Digital Rights Management

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

24

# What is there to secure?

- Data at rest
- Data in transit
- Data in use

© Mihai Chiroiu ISC security crunch CC BY NC SA 25

# Assets

- What is interesting and why in the cyber world?
- Often not sufficiently accounted for, therefore hackable
    - E.g. because everyone wants fast business increases

Attacker model

© Mihai Chiroiu ISC security crunch CC BY NC SA 27

# Exploitability of assets

Google

adobe acrobat zero-day

All | Videos | Images | Maps | Shopping | More | Tools

About 3,250,000 results (0.42 seconds)

According to Adobe, the zero-day vulnerability, which is tracked as **CVE-2021-28550** , "has been exploited in the wild in limited attacks targeting Adobe Reader users on Windows." Windows users of Adobe Reader may be the only ones currently targeted. May 11, 2021

https://threatpost.com › Vulnerabilities

Hackers Leverage Adobe Zero-Day Bug Impacting Acrobat ...

About featured snippets • Feedback

https://www.darkreading.com › vulnerabilities-threats

Adobe Issues Patch for Acrobat Zero-Day - Dark Reading

May 12, 2021 — Adobe Issues Patch for Acrobat Zero-Day. The vulnerability is being exploited in limited attacks against Adobe Reader users on Windows.

ISC security crunch

CC BY NC SA

28

# Terms

- bug
- vulnerability
- exploit

# Attack surface

- External
- Internal
    - Malicious
    - Mistake

# Attackers - headlines

- World's Biggest Data Breaches &amp; Hacks
    - http://www.informationisbeautiful.net/visualizations/worlds-biggest-data-breaches-hacks/
- Interesting maps
    - https://cybermap.kaspersky.com/
    - https://www.talosintelligence.com/
    - https://threatmap.fortiguard.com/
    - https://threatmap.checkpoint.com/

# Attackers

- From pranksters to professionals:
    - Script Kiddies
    - Attackers
        - white vs grey vs black
    - Vulnerability Brokers vs Cybercriminals
        - Bug bounty programs
    - Hacktivists
    - National State Adversaries
    - Advanced persistent threat (APT)

ISC security crunch CC BY NC SA 32

# Types of threats

- Threats
    - Social engineering
    - Network threats
    - Denial of Service
    - Malware
        - Trojan
        - Keyloggers
        - Rootkits
        - Worms
        - Fileless Malware
        - Ransomware
        - Virus
        - ...

ISC security crunch

CC BY NC SA

33

# Types of malware (lecture 06)

- Virus – infects files, spreads when opening them
- Worm – automatically infects other systems!
    - Logic bomb
- Trojan horse – user must explicitly open crafted exe
    - Remote Access Trojan
- Ransomware – Money for your data!
- Spyware – NSA, Pegasus etc. ;)
- Adware – the entire WWW :(

# Attackers vs defenders

- Anti-viruses?
- In general, it's easier to destroy than to create
    - "rm --rf --no-preserve-root /"
- Evasion Method
    - Encryption and tunneling
    - Resource exhaustion
    - Traffic fragmentation
    - Protocol-level misinterpretation
    - Traffic substitution

ISC security crunch 35

# Attacker model

- dolev yao model
    - formal networking analysis
    - crypto is unbreakable
- stride attacker model
    - https://en.wikipedia.org/wiki/STRIDE\_model

ISC security crunch CC BY NC SA 36

# Tactics, Techniques, and Procedures (TTPs)

- Generalized statement of adversary behavior
- Campaign strategy and approach (tactics)
- Generalized attack vectors (techniques)
- Specific intrusion tools and methods (procedures)
- Indicator of compromise (IoC)
    - Specific evidence of intrusion
    - Individual data points
    - Correlation of system and threat data
    - AI-backed analysis
    - Indicator of attack (IoA)
- https://attack.mitre.org/matrices/enterprise/

# Security (by) Design

ISC security crunch CC BY NC SA

# Security building blocks

- cryptography
- access control

ISC security crunch CC BY NC SA 39

# Zero Trust

ISC security crunch CC BY NC SA 40

# Least privilege

- Complex systems are more difficult to secure.
- The more applications deployed, the more possible vulnerabilities.

© Mihai Chiroiu

ISC security crunch

CC BY NC SA

41

# Weakest link

- An infrastructure is as strong as its weakest link.

ISC security crunch CC BY NC SA 42

# Security vs the world (complexity)

- Downside: Complexity brings vulnerability
    - How secure is a 1000-computer network with &gt;1000 users and 200 different applications?
    - How secure is a simple button?
- Still, we DO need complexity to accomplish our tasks

© Mihai Chiroiu

ISC security crunch

43

# Security Administration

ISC security crunch

CC BY NC SA

44

# Security Administration

- Paperwork is important
    - “Dosar cu șină”
- Policies
- Standards
- Guidelines
- Procedures
- Baselines

© Mihai Chiroiu

ISC security crunch

45

# Security Policy

- A **contract** that states how to protect information assets
    - It needs to be “s.m.a.r.t.” (specific measurable achievable timely)
    - Management instructions indicating a course of action, a guiding principle, or appropriate procedure
    - High-level statements that provide guidance to workers who must make present and future decisions
    - Must be communicated to others
- It defines what “security” means for an organization

© Mihai Chiroiu

46

# Security Policy - example

- Authentication policy
    - Specifies authorized persons that can have access to network resources and identity verification procedures.
- Password policies
    - Ensures passwords meet minimum requirements and are changed regularly.
- Acceptable Use Policy (AUP)
    - Identifies network applications and uses that are acceptable to the organization. It may also identify ramifications if this policy is violated.
- Remote access policy
    - Identifies how remote users can access a network and what is accessible via remote connectivity.
- Maintenance policy
    - Specifies operating systems and end user application update procedures.
- Incident handling procedures
    - Describes how security incidents are handled.

# Documents Supporting Policies

- Standards – dictate specific minimum requirements in our policies
- Guidelines – suggest the best way to accomplish certain tasks
- Procedures – provide a method by which a policy is accomplished (the instructions)

© Mihai Chiroiu ISC security crunch 48

# Policy Example

- Your personal (protected) health information is stored in a personal electronic folder. (https://ehr.des-cnas.ro/cnasportalext/index.html)
- Design a security policy to protect them.
    - What is there to protect?
    - From whom?
    - How long should data be saved?
    - What about CIA?
- Enter **HIPAA Rules and Regulations** .

ISC security crunch CC BY NC SA 49

# References

1. [http://www.phishing.org/history-of-phishing/](http://www.phishing.org/history-of-phishing/) (on 31.10.2022)
2. [https://www.owasp.org/images/2/25/OWASP\_angela\_sasse\_appsec\_eu\_aug2013.pdf](https://www.owasp.org/images/2/25/OWASP_angela_sasse_appsec_eu_aug2013.pdf) (on 31.10.2022)
3. [http://www.wired.com/2012/08/apple-amazon-mat-honan-hacking/](http://www.wired.com/2012/08/apple-amazon-mat-honan-hacking/) (on 31.10.2022)
4. [http://arstechnica.com/security/2013/03/spamhaus-ddos-grows-to-internet-threatening-size/](http://arstechnica.com/security/2013/03/spamhaus-ddos-grows-to-internet-threatening-size/) (on 31.10.2022)
5. [https://www.us-cert.gov/ncas/alerts/TA13-088A](https://www.us-cert.gov/ncas/alerts/TA13-088A) (on 31.10.2022)
6. [https://csrc.nist.gov/csrc/media/publications/conference-paper/1998/10/08/proceedings-of-the-21st-nissc-1998/documents/early-cs-papers/dod85.pdf](https://csrc.nist.gov/csrc/media/publications/conference-paper/1998/10/08/proceedings-of-the-21st-nissc-1998/documents/early-cs-papers/dod85.pdf) (on 1.03.2023)

© Mihai Chiroiu

50

# References (2)

## Online book:

*Computer Security and the Internet: Tools and Jewels* , Paul C. van Oorschot. Springer, 2021.

https://people.scs.carleton.ca/~paulv/toolsjewels.html

51