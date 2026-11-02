---
routerMode: hash
download: 'slides.pdf'
theme: ../../isc-theme
colorSchema: light
selectable: false
touying:
  preset: isc
info: |
  ## Cyber-Physical Security (IT vs OT)
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left

layout: cover
title: "Cyber-Physical Security"
subtitle: "ICS/OT security — when bits move the physical world"
---

::default::

<style>
/* Mermaid inside a two-cols column: fit the column instead of overflowing the slide */
.slidev-layout .mermaid svg { max-width: 100% !important; height: auto !important; }
.slidev-layout .img-col .mermaid { width: 100%; }
</style>

---
layout: section
---

# Context

---

# This lecture

<v-clicks>

1. Context: **IT vs OT** (Operational Technology)
2. Security principles
3. Threats & attacks
4. **Attacking the process** — ICS specifics
5. **Impact**: safety and availability
6. Defense

</v-clicks>

---
layout: two-cols
---

# IT vs OT

- **IT** — Information Technology: servers, cloud, business data
- **OT** — Operational Technology: PLCs, RTUs, sensors, actuators
- Two different worlds, historically **air-gapped**
- Latest trend: connecting CPS to the ☠️ **Internet** ☠️
  - **IIoT** — Industrial Internet of Things
- **IT/OT convergence** — one network, two sets of priorities

::right::

<div class="img-col">
<img src="./images/it_ot_convergence.png" />
<em>IT/OT convergence</em>
</div>

---

# Cyber-physical systems (CPS)

- Software + network + **physical process**
- Examples: power grid, autonomous vehicles, **ICS/SCADA**, smart buildings, medical devices, manufacturing lines
- Main security concerns are **Availability + Integrity**
- An attack is no longer only "data leaked" - it can **cause harm / disruption**

<br/>

**"Cyber" is not the target — the physical process is.**

---

# Anatomy of an ICS — the Purdue model

```mermaid {theme: 'isc-cartoon', scale: 0.62}
flowchart LR
  subgraph ITZ["IT · corporate"]
    A["L4/5 Enterprise<br/><em>ERP, mail, cloud</em>"]
  end
  subgraph DMZZ["DMZ · L3.5"]
    B["Historian<br/>jump host"]
  end
  subgraph OTZ["OT · plant floor"]
    C["L3 Site ops<br/><em>MES</em>"] --> D["L2 Supervisory<br/><em>SCADA / HMI</em>"]
    D --> E["L1 Basic control<br/><em>PLC / RTU / SIS</em>"]
    E --> F["L0 Process<br/><em>sensors / actuators</em>"]
  end
  A --> B --> C
```

- **L1**: Intelligent Devices zone: Programmable Logic Controllers, Remote Terminal Units, 
  Safety Instrumented Systems;
- **L2**: Control Systems zone: SCADA, DCS (Distributed Control), Human-Machine
  Interfaces;
- **L3**: Manufacturing Operations: management / execution / data historians;
- **L3.5 DMZ** is an industry convention, **not** part of the original PERA model
- Every level is a target: steal credentials (IT), rewrite logic (PLC), lie to the operator (HMI)

---

# Security priorities: IT vs OT

<div style="width: 90%; margin: 1em auto;">

|            | **IT security**                 | **OT / CPS security**                                 |
| ---------- | ------------------------------- | ----------------------------------------------------- |
| Priority   | **CIA** - confidentiality first | **Safety · Reliability · Resilience**                 |
| Control    | cryptography                    | **physical fail-safe** mechanisms                     |
| Worst case | data loss, downtime, fines      | **harm, environmental damage, disruption**            |
| Threat     | malware, phishing, insiders     | all of the above **+ the physical world as actuator** |

</div>

> In OT, availability is not a number in a SLA — it is a pump that must keep running.

---

# Why OT cannot simply be patched

- The plant runs **24/7** — a reboot is a production stop, sometimes a safety event
- Equipment lives **20–40 years**; firmware is frozen and **vendor-certified**
- Any change may require **re-certification / re-validation** of the process
- Old OS on HMIs (Win XP / 7); **no AV agent on a PLC** (real-time, no resources)
- One maintenance window per year, negotiated with production

<v-click>

**⇒ You cannot "just patch". You compensate:**

- Segmentation (**IEC 62443 zones & conduits**), allow-listing
- Passive monitoring, virtual patching (IPS), offline backups of logic
- A **tested** manual-operation mode

</v-click>

---

# Motivation — 25 years of ICS incidents

<div class="cps-tl">
  <div><b>2000</b>Maroochy<br/>insider, sewage</div>
  <div><b>2007</b>Łódź trams<br/>4 derailed</div>
  <div><b>2010</b>Stuxnet<br/>≈1,000 centrifuges</div>
  <div><b>2015</b>Ukraine grid<br/>~225,000 dark</div>
  <div><b>2017</b>Triton<br/>SIS attacked</div>
  <div><b>2021</b>Colonial<br/>OT untouched</div>
  <div><b>2023</b>Unitronics<br/>password <code>1111</code></div>
  <div><b>2024</b>Lebanon<br/>pagers</div>
  <div><b>2025</b>Jaguar Land Rover<br/>5 weeks idle</div>
  <div><b>2026</b>French Supermarket Refrigerators</div>
</div>

<div class="text-sm opacity-70" style="margin-top: 1.5em">
We'll have some slides about these, stand by... ;)
</div>

<style>
.cps-tl { display: flex; gap: .55em; margin-top: 3.2em; }
.cps-tl > div { flex: 1; border-top: 3px solid #000; padding-top: .55em; font-size: .62em; line-height: 1.4; }
.cps-tl b { display: block; font-size: 1.6em; margin-bottom: .25em; }
</style>

---
layout: section
---

# Security principles

---

# Security principles (recap)

- **Cyberattack** — unauthorized use of a digital system
- **CIA triad**
  - **C + I** → cryptography-based solutions
  - **A** → redundancy, fail-overs, good architectures
- **AAA model** — Authentication, Authorization, Accounting
- Data in **use / transit / at rest**
- Threats & attacks: network, malware, social engineering
- Security frameworks: **NIST CSF**, **IEC 62443**, ISO 27001/27019

---
layout: two-cols
class: cols-60-40
---

# Attacker model & economics

- Don't protect **$1B** with encryption broken for **$1M**
- Don't spend **$10M** to protect **$1M**
- In CPS the attacker may simply **walk up to the device**
  - Default passwords, exposed debug ports, unlocked cabinets

::right::

<div class="img-col" style="margin-top: 5em;">
<img src="./images/xkcd_security_538.png" />
<em>https://xkcd.com/538/</em>
</div>

---
layout: section
---

# Threats & attacks

---

# Threat classification

- **Source:** external / internal
- **Motivation:** hacktivism / economic / espionage / warfare …
- **Attack vectors**
  - Network access
  - Software/hardware vulnerabilities
  - Physical access
  - Supply chain
  - Social engineering
- **Impact**, lifecycle stages, target components (cyber-physical layers)
- **Advanced Persistent Threats (APT)**

---
layout: two-cols
---

# Types of attackers

From pranksters to professionals:

<v-clicks>

- Script kiddies
- Vulnerability brokers
- Cybercriminals
- Hacktivists / security researchers
- **National state adversaries**

</v-clicks>

::right::

<div class="img-col">
<img src="./images/hackers_cast.png" />
<em>"Hackers", 1995 — the professional look</em>
</div>

---

# Vulnerabilities

- **Complexity ⇒ bugs** (software / hardware)!
- **Vulnerability** — a bug that introduces a security risk
  - Design/implementation flaws (buffer overflows, broken crypto …)
  - Configuration errors (weak ACLs, hardcoded passwords)
  - Supply chain (vulnerabilities in third-party components)
  - Human stupidity (social engineering)
- **Discovery ⇒ exploitation ⇒ patching**
- **Zero-days!**

---

# Common Weakness Enumeration

- MITRE's **CWE** (similar: OWASP Top 10)
- **CWE Top 25 — 2025** [1]:
  - CWE-79: Cross-site Scripting
  - CWE-89: SQL Injection
  - CWE-352: Cross-Site Request Forgery (CSRF)
  - CWE-862: Missing Authorization
  - CWE-787: Out-of-bounds Write
  - CWE-22: Path Traversal
- In ICS the interesting weaknesses are usually **misconfiguration**, not code

[cwe.mitre.org/top25](https://cwe.mitre.org/top25/)

---

# Common Vulnerabilities & Exposures

- Vulnerabilities in public / commercial software
- The **CVE Program** is sponsored by **CISA** (US DHS); **MITRE** operates it as the primary CNA / CNA-of-Last-Resort (~400+ CNAs worldwide)
  - Since 2025 governance is moving to the non-profit **CVE Foundation**
- Examples
  - **CVE-2010-2772** — Siemens Simatic WinCC / PCS 7 SCADA uses a **hard-coded password** — used by Stuxnet to move laterally
  - **CVE-2023-36028** — Microsoft PEAP Remote Code Execution (CVSS 9.8)
  - **CVE-2023-21608** — Adobe Acrobat use-after-free RCE
- CVEs often come with **Proofs of Concept** (exploit code)!

---

# The intrusion kill chain

<div class="img-col">
<img src="./images/intrusion_kill_chain.png" style="max-height: 300px; max-width: 100%;" />
<em><a href="https://en.wikipedia.org/wiki/Cyber_kill_chain">Lockheed Martin, 2011 (Wikipedia)</a></em>
</div>

---

# MITRE ATT&CK for ICS

- Adversary tactics for ICS — **12**, not the enterprise 14
- The familiar ones: *Initial Access · Execution · Persistence · Privilege Escalation · Evasion · Discovery · Lateral Movement · Collection · Command & Control*
- **The three that exist for process safety:**
  - **Inhibit Response Function** — blind or disable safety, protection, alarms, operator response
  - **Impair Process Control** — manipulate or damage the control loop
  - **Impact** — interrupt, manipulate or destroy the process

[attack.mitre.org/matrices/ics](https://attack.mitre.org/matrices/ics/)

---

# Two maps, one attack

<div style="width: 90%; margin: 0.2em auto; font-size: 0.9em;">

| Kill chain (Lockheed, 2011) | ATT&CK for ICS                   |
| --------------------------- | -------------------------------- |
| Reconnaissance              | Discovery · Collection           |
| Weaponization               | *(enterprise-only: Resource Development)* |
| Delivery                    | Initial Access · Lateral Movement |
| Exploitation                | Execution · Privilege Escalation |
| Installation                | Persistence · Evasion            |
| Command & Control           | Command and Control              |
| Actions on objective        | **Impair Process Control** · **Inhibit Response Function** · **Impact** |

</div>

The kill chain tells a **story**; ATT&CK gives you **detections**. The last row is where ICS/OT differs from IT.

---

# Intrusion workflow — examples

| Phase                | In practice                                                       |
| -------------------- | ----------------------------------------------------------------- |
| Reconnaissance       | `nmap` (**never** on a live plant), distributed IP scanning, **Shodan** |
| Weaponization        | buy an exploit kit (worm + RAT + rootkit), or a plant-specific tool |
| Delivery             | phishing / social engineering, crafted packet or document, USB      |
| Exploitation         | **RCE** and/or privilege escalation                                |
| Installation         | rootkit + remote access trojan                                     |
| Command & Control    | covert + encrypted channel, on stolen servers / IoT equipment      |
| Actions on objective | ??? ⇒ **profit!**                                                  |

---
layout: section
---

# Attacking the process

---

# OT protocols were not built for security

- **Modbus/TCP** (TCP 502) — no authentication, no integrity, no encryption
- **DNP3** (IEEE 1815) — base protocol unauthenticated; Secure Authentication (**SAv2**) added in IEEE 1815-2012, **SAv5** later
- **PROFINET** (RT/IRT, DCP), **EtherNet/IP + CIP** — unauthenticated by default
- Security came as **add-ons**: Modbus/TCP Security over TLS (2018), **CIP Security**, **DNP3 SA**, **IEC 62351** for power protocols
- **OPC UA** (IEC 62541) is the exception — X.509, Sign / SignAndEncrypt by design

<div class="text-sm opacity-70">

These protocols were designed for determinism and field-bus efficiency on isolated networks!

</div>

---

# Attack surface in OT

- **Internet-exposed** HMIs / PLCs · **default / shared credentials** · **remote vendor access**
- **USB** and removable media · **IT→OT pivot** · **supply chain** · no logging

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.8}
flowchart LR
  I(["Internet"]) -->|Shodan| H["HMI"]
  I -->|VPN / AnyDesk| E["Eng. workstation"]
  U["USB ·<br/>vendor laptop"] --> E
  H --> P["PLC / RTU"]
  E --> P
  P --> X["physical process"]
```

</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Maroochy Shire (2000)

- **Where:** sewage system, Queensland, Australia
- **Who:** Vitek Boden — ex-contractor, rejected for a job
- **How:** laptop + radio from his car → **unauthenticated** wireless pump controllers
- **Impact:** ~**800,000 L** of raw sewage into parks, canals, hotel grounds; dead fish, 46 spills, **300+ alarms ignored**
- **Caught:** by matching his car's movements with the alarm times → jailed (2001)

<br/>

**Lesson:** no authentication on field comms + insider knowledge + nobody watching the alarms.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.72}
flowchart TD
  A["laptop +<br/>radio"] --> B["pump controllers<br/><em>no auth</em>"]
  B --> C["sewage<br/>pumps"]
  C --> D["parks, canals"]
```

<em>one insider, a laptop and a radio</em>
</div>

<!--
The first famous ICS attack was an insider with a radio. No zero-day, no exploit,
just unauthenticated commands and no monitoring.
-->

---
layout: two-cols
class: cols-60-40
---

# Example: Oldsmar plant (2021)

- **Where:** water treatment plant, Oldsmar, Florida
- **How:** remote access via **TeamViewer** — one shared password for all users, unsupported version, **no firewall**
- **What:** intruder took the HMI twice and moved the **lye** setpoint **100 ppm → 11,100 ppm**
- **Saved by:** an operator watching the screen saw the cursor move and set it back
- **Never charged** — the suspect was never publicly identified

<br/>

**Lesson:** remote access **is** an OT control. Shared passwords are not "IT details".

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.85}
flowchart TD
  I(["Internet"]) --> T["TeamViewer<br/><em>shared password</em>"]
  T --> H["HMI"]
  H --> L["lye dosing<br/><em>100 → 11,100 ppm</em>"]
```

<em>the human in the loop is the control</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Unitronics PLCs (2023)

- **Who:** *CyberAv3ngers* — IRGC-affiliated, anti-Israel hacktivism
- **How:** internet-exposed **Unitronics Vision** PLC/HMI, factory password **`1111`**, TCP 20256, no authentication
- **Impact:** pumps and booster stations at small US utilities (Aliquippa, PA) disabled, HMIs defaced → manual operation; **no loss of water service**
- **Also:** water utilities in Ireland
- **Response:** CISA advisory AA23-335A, exposure scans, password resets

<br/>

**Lesson:** the default password **is** the vulnerability.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.85}
flowchart TD
  I(["Internet"]) --> H["Unitronics HMI<br/><em>1111 · :20256</em>"]
  H --> P["PLC"]
  P --> B["booster pumps"]
```

<em>three words of config away from a plant</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Industroyer (2016)

- **Where:** Pivnichna 330 kV substation, Ukraine
- **How:** malware modules that **speak the grid's own protocols** — IEC 60870-5-101/104, IEC 61850, OPC DA — straight to the RTUs
- **Impact:** ~⅕ of Kyiv without power (~200 MW) for about an hour; wiper alongside
- **2022 — Industroyer2:** IEC-104 with hard-coded breaker commands; **blocked** by CERT-UA / ESET

<br/>

**Lesson:** no exploit needed — **the protocol is the weapon**.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.85}
flowchart TD
  A["Industroyer<br/><em>IEC-104 · 61850 · OPC</em>"] --> R["RTU /<br/>bay controller"]
  R --> B["breakers"]
  B --> G["330 kV<br/>substation"]
```

<em>industrial malware without a single exploit</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Stuxnet (2010)

- **Target:** Natanz enrichment plant, Iran
- **Motivation:** sabotage by a nation-state (*ahem*)
- **How:** USB + **4 Windows zero-days** → Windows hosts → **rewrote the S7-315 PLC logic** (+ CVE-2010-2772)
- **Deception:** replayed **21 s** of normal telemetry to the HMI and blocked alarms
- **Impact:** ≈**1,000 of ~8,700** IR-1 centrifuges (ISIS estimate, range 1–2k); ≈**1–2 years** delay (contested)

::right::

<div class="img-col">
<img src="./images/stuxnet_centrifuge_cascade.jpg" style="max-height: 300px" />
<em>Gas centrifuge cascade — U.S. Department of Energy (public domain)</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Aurora (2007)

- **What:** a controlled test at **Idaho National Laboratory**, not an incident
- **How:** spoofed control traffic opened and closed a breaker **out of phase**
- **Result:** the generator fought itself, jumped off its mounts and threw debris — **destroyed**
- **No malware, no exploit** — just the right packets at the right moment

<br/>

**Lesson:** the worst case in CPS is not data loss, it is **physical destruction** — and it needs no vulnerability at all.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.78}
flowchart TD
  A["spoofed packets"] --> B["breaker"]
  B -->|out of phase| C["generator<br/><em>2.25 MW · 27 t</em>"]
  C --> D["destroyed<br/>+ debris"]
```

<em>two commands, one dead generator</em>
</div>

---

# Example: Volt Typhoon (2023 →)

- **Who:** PRC state-sponsored, "living off the land"
- **How:** valid accounts + built-in tools, staged through compromised **SOHO routers**; no bespoke ICS malware
- **Where:** US critical infrastructure — energy, water, transport, communications
- **Impact so far: none publicly observed** — this is **pre-positioning**

<br/>

<v-click>

**Lesson:** *capability ≠ effect*. Hunting for malware finds nothing here; you hunt **behaviour** and **identity**. Assume the network is already compromised.

</v-click>

---
layout: two-cols
class: cols-60-40
---

# Example: Lebanon pagers (2024)

- **When:** 17–18 Sep 2024 — pagers, then walkie-talkies
- **How:** a front company (BAC Consulting, Budapest) supplied Gold Apollo-branded **AR-924** pagers with explosive and a detonator built into the battery compartment — **implanted during production**, not "intercepted in transit"
- **Impact:** ≈**37 killed, 3,000+ injured** across the two days

<br/>

**Lesson:** the **supply chain is an attack surface** for every connected device. Physical access to a device is a cyber capability.

::right::

<div class="img-col">
<img src="./images/pager_ar924.png" style="max-height: 170px" />
<em>Gold Apollo AR-924 — photo: TobiToaster, CC BY-SA 4.0</em>
</div>

---
layout: section
---

# Impact

---

# Safety vs security

- A **Safety Instrumented System (SIS)** is an independent layer that drives the plant to a **safe state** (IEC 61511, SIL levels)
  - Safety PLCs, trips, interlocks, relief systems
- It was designed for **safety**, not for security
  - No authentication, no crypto, frozen firmware, almost never patched
  - Excluded from IT scanning and IT change management — "do not touch"
  - Engineering workstations are often **dual-homed** (IT + SIS network)
- **Fail-safe vs fail-secure**: safety wants to *stop* the process, security wants to *keep it available* — the goals can conflict
- Security controls must **never break the safety case** (no AV on the SIS, no aggressive scanning)

---
layout: two-cols
class: cols-60-40
---

# Example: Triton (2017)

- **Where:** petrochemical plant, Saudi Arabia — **Triconex SIS**
- **How:** IT → **engineering workstation** → **TriStation** protocol (unauthenticated, TCP 1502) → reprogram the safety controllers
- **Impact:** a safety trip shut the plant down; the intent was to **disable the safety layer** → risk of catastrophic release
- **Note:** custom tooling built for one specific SIS model

<br/>

**Lesson:** the safety layer is a target. An SIS that nobody monitors, patches or audits is the softest spot in the plant — and the most valuable one.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.6}
flowchart TD
  A["corporate IT"] --> B["engineering<br/>workstation"]
  B --> C["TriStation<br/><em>:1502, no auth</em>"]
  C --> D["Triconex SIS"]
  D --> E["process"]
  D -.->|trip| F["plant<br/>shutdown"]
```

<em>the layer that is supposed to save you</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Ukraine grid (2015)

- **When:** 23 Dec 2015, ~15:35 — three distribution utilities, **~225,000** customers, outages 1–6 h
- **How:** BlackEnergy spear-phishing → IT → SCADA; attackers **drove the HMIs by hand** to open breakers
- **Also:** KillDisk wiper on the SCADA hosts, and a **telephony DoS** so customers could not report the outage
- **Recovery:** manual switching at substations, hours to days

<br/>

**Lesson:** you do not need automation — an operator console is enough. **Blinding the response** is part of the attack.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.8}
flowchart TD
  P["spear-phish"] --> I["IT"]
  I --> S["SCADA"]
  S --> H["HMIs<br/><em>by hand</em>"]
  H --> B["breakers<br/><em>~225k dark</em>"]
  S -.->|KillDisk| W["logs wiped"]
```

<em>no automation needed</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Colonial Pipeline (2021)

- **When:** 7 May 2021 — DarkSide ransomware
- **How:** **legacy VPN account**, reused leaked password, **no MFA**; ~100 GB exfiltrated
- **Hit:** **IT / billing only — OT was never compromised**
- **Impact:** pipeline **shut ~6 days by decision** → fuel shortages; 75 BTC ≈ **$4.4M** paid, FBI recovered ≈**$2.3M**

<br/>

**Lesson:** IT downtime becomes a **physical supply-chain event**. MFA and account hygiene are OT controls — and the shutdown, not the malware, caused the shortage.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.72}
flowchart TD
  A["IT / billing<br/><em>ransomware</em>"] --> B{"shut<br/>down?"}
  B -->|yes, 6 days| C["pipeline stopped<br/><em>OT never compromised</em>"]
  C --> D["fuel shortage"]
```

<em>the seam between IT and OT</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Norsk Hydro (2019)

- **When:** 19 Mar 2019 — LockerGoga ransomware
- **How:** Windows IT / Active Directory; no OT compromise reported
- **Impact:** ~22,000 machines affected; extrusion plants switched to **pen and paper** within hours; output partly maintained
- **Cost:** tens of millions USD (quarterly report), plus reputation

<br/>

**Lesson:** a **tested manual-operation mode** is a security control — and "IT-only" can still stop physical production.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.9}
flowchart TD
  A["Windows IT<br/><em>LockerGoga</em>"] --> B["AD + files<br/>encrypted"]
  B --> C["plants switch to<br/><em>pen & paper</em>"]
  C --> D["output partly<br/>maintained"]
```

<em>degraded mode, on purpose</em>
</div>

---
layout: two-cols
---

# Example: Jaguar Land Rover

- **When:** 31 Aug 2025 — Qilin ransomware
- **How:** corporate IT; plants depend on ERP/MES for scheduling and parts
- **Impact:** production **halted ~5 weeks** (resumed 8 Oct 2025), supplier cash crisis, thousands of workers idled
- **Cost:** UK-wide impact modelled at ≈**£1.9bn** — reported as the costliest UK cyber incident (estimate, not audited)

<br/>

**Lesson:** a modern factory **is** a cyber-physical system. If the planning systems die, the robots stop.

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.9}
flowchart TD
  A["corporate IT<br/><em>Qilin</em>"] --> B["ERP / MES"]
  B --> C["no schedule,<br/>no parts"]
  C --> D["lines stop<br/><em>~5 weeks</em>"]
```

<em>a factory runs on planning systems</em>
</div>

---
layout: two-cols
class: cols-60-40
---

# Example: Supermarket fridges (2026)

- **When:** night of 11–12 Oct 2026, up to **~700** French supermarkets
- **How:** internet-exposed **Danfoss AK-SM800 / AK-SC355** fridge controllers - web login `admin` + 
  **the device date is the password**
- **Known** vulnerability (Claroty), patched in Aug 2025, but only on SM800A
  (newer models); older ones were **end-of-life** (2016-2021)!
- **Impact:** **continuous defrost** → **+50 °C** after 6h, melted units, fires; 10s of mill. € food discarded

::right::

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.82}
flowchart TD
  I(["Internet"]) --> D["Danfoss AK-SM800<br/><em>admin / date · EOL</em>"]
  D -->|defrost| F["+50 °C<br/><em>6 h, food inside</em>"]
  F --> G["melted units,<br/>fires"]
  F --> H["cold chain gone<br/><em>till emptied</em>"]
```

<em>a fridge is an actuator too</em>
</div>

---
layout: section
---

# Defense

---

# Defender's tasks

- **Penetration testing** — black box / white box / gray box
  - In OT: a testbed or digital twin first, **never** a production scan
- **TTPs** — Tactics, Techniques and Procedures
  - Campaign strategy (**tactics**), attack vectors (**techniques**), tools (**procedures**)
- **IoC / IoA** — indicator of compromise / of attack
  - Reactive: evidence of intrusion
  - Logs, **SIEM** alerts, correlation of system and threat data
- **ATT&CK for ICS** — the map you detect against

---

# Detection in OT

- **No agents** on controllers; no EDR on a PLC
  - **No heuristics-based AV detection**: false-positives may stop the processes!
- **No active scanning**: brittle devices, and a scan can trip a protection
- **Passive monitoring** via SPAN / TAP: protocol-aware baselining of Modbus, DNP3, S7, EtherNet/IP
  - Sources: engineering workstations, HMIs, switches, firewalls, **physical access control**
  - Correlate in a SIEM; map detections to **ATT&CK for ICS**
- Exercises: tabletop incident response where **safety comes before containment**

<div class="img-col">
<img src="./images/siem_dashboard.png" style="max-height: 130px" />
</div>

---

# Segmentation: zones & conduits

- A **zone** groups assets with the same security requirement (**SL1–SL4**)
- A **conduit** is the *only* allowed path between two zones — firewall, proxy, data diode
- Default **deny** between zones; allow only what the process needs
- Same idea as the DMZ, applied **per process area**: not one wall, but many small ones

<div class="img-col">

```mermaid {theme: 'isc-cartoon', scale: 0.62}
flowchart LR
  subgraph Z1["Zone 1 · enterprise · SL1"]
    A["ERP / mail"]
  end
  subgraph Z2["Zone 2 · supervisory · SL2"]
    B["SCADA / HMI"]
  end
  subgraph Z3["Zone 3 · control · SL3"]
    C["PLC"]
  end
  A -->|conduit: firewall + proxy| B
  B -->|conduit: no routing| C
```

<em>IEC 62443-3-2 zones & conduits</em>
</div>

---

# Best practices — IT vs OT

<div style="width: 96%; margin: 0.5em auto;">

| Area         | **IT**                        | **OT / ICS**                                              |
| ------------ | ----------------------------- | --------------------------------------------------------- |
| Patching     | weekly, automated             | maintenance window, vendor-certified, **compensate**       |
| Endpoint     | EDR / AV on every host        | **no agents on controllers** → allow-listing, app control  |
| Remote access| VPN + MFA                     | jump host + MFA, **no direct vendor access**               |
| Monitoring   | agents + SIEM                 | **passive taps**, protocol baselines, no active scans      |
| Backup       | images, tested restores       | PLC logic / HMI configs **+ tested manual mode**           |
| IR & testing | isolate, reimage, pentest     | **safety first**, then isolate; testbed, not production    |

</div>

---

# Assurance: Common Criteria & IEC 62443

- **Common Criteria** — certifies IT products
  - **Protection Profile (PP)**, **Security Target (ST)**, **EAL1–EAL7** (EAL1 = basic … EAL7 = formal)
  - Measures the *assurance process*, not "safe for a plant"
- **IEC 62443** — the ICS standard
  - **Zones & conduits**: group assets by security requirement, control every path between them
  - **Security Levels SL1–SL4**, component requirements (62443-4-2), certification schemes
- For energy utilities: **ISO/IEC 27019**; for OT programmes: **NIST SP 800-82 Rev.3 (2023)** — *Guide to OT Security*

---

# Human & organizational factors

- **Operator training & awareness**
  - The human is both the weakest link and the first line of defense
  - The Oldsmar attack was caught by an operator watching the screen
- **Policies and governance**
  - **NIST SP 800-82**, **IEC 62443**, plant change management
- **Supply chain security**
  - Hardware trust, firmware signing, **vendor access** management
- **Cross-disciplinary collaboration**
  - Process engineers, OT staff, IT staff and management coordinate
  - Security asks "who can reach it?"; safety asks "what happens if it stops?"

---

# Key takeaways

<v-clicks>

1. In CPS you protect **CIA + safety, reliability, resilience** — and availability usually wins.
2. The **air gap is gone**: IT is the road into OT. MFA, segmentation and monitoring are OT controls.
3. You **cannot patch a running plant** — you compensate: zones, allow-listing, passive detection, tested manual mode.
4. Attackers target **the process, and sometimes the safety layer** (Triton). The worst case is physical.
5. Assume compromise: hunt **behaviour** (ATT&CK for ICS), not just malware — and keep an offline, tested recovery path.

</v-clicks>

---

# References — incidents

<small>

- Łódź trams: [The Register, 11 Jan 2008](https://www.theregister.com/off-prem/2008/01/11/polish-teen-derails-tram-after-hacking-train-network/759671) · [The Telegraph](https://www.telegraph.co.uk/news/worldnews/1575293/Schoolboy-hacks-into-citys-tram-system.html)
- Maroochy Shire: [MITRE case study (2008)](https://www.mitre.org/sites/default/files/pdf/08_1145.pdf)
- Aurora: Idaho National Laboratory generator test, 2007
- Stuxnet: [ISIS, "Did Stuxnet Take Out 1,000 Centrifuges?" (2010)](https://isis-online.org/isis-reports/detail/did-stuxnet-take-out-1000-centrifuges-at-the-natanz-enrichment-plant/) · [Langner, "To Kill a Centrifuge" (2013)](https://www.langner.com/wp-content/uploads/2017/03/to-kill-a-centrifuge.pdf)
- Ukraine 2015: [CISA IR-ALERT-H-16-056-01](https://www.cisa.gov/news-events/ics-alerts/ir-alert-h-16-056-01) · SANS/E-ISAC analysis
- Industroyer: [ESET, 2017](https://www.welivesecurity.com/2017/06/12/industroyer-biggest-threat-industrial-control-systems-since-stuxnet/)
- Triton: [Mandiant, "TRITON — new ICS attack framework" (2017)](https://cloud.google.com/blog/topics/threat-intelligence/attackers-deploy-new-ics-attack-framework-triton)
- Oldsmar: [Dragos analysis](https://www.dragos.com/blog/recommendations-following-the-oldsmar-water-treatment-facility-cyber-attack/) · CISA/INL CyOTE case study
- Unitronics: [CISA AA23-335A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-335a)
- Colonial Pipeline: [CISA AA21-131A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-131a) · DOJ ransom seizure, 2021
- Volt Typhoon: [CISA AA24-038A](https://www.cisa.gov/news-events/cybersecurity-advisories/aa24-038a)
- Lebanon pagers: [Reuters, Sep 2024](https://www.reuters.com/world/middle-east/hezbollah-handed-out-pagers-hours-before-blasts-even-after-checks-2024-09-20/)
- JLR 2025: [Wikipedia — Jaguar Land Rover cyberattack](https://en.wikipedia.org/wiki/Jaguar_Land_Rover_cyberattack) (estimates are modelled)

</small>

---

# References — standards & further reading

<small>

- [MITRE ATT&CK for ICS](https://attack.mitre.org/matrices/ics/) · [CWE Top 25](https://cwe.mitre.org/top25/) · [CVE Program](https://www.cve.org/)
- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) (CSWP 29, Feb 2024)
- [NIST SP 800-82 Rev.3 — Guide to OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) (2023)
- [ISA/IEC 62443 series](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) · ISO/IEC 27019 (energy utilities)
- [Common Criteria](https://www.commoncriteriaportal.org/)
- [CISA ICS advisories](https://www.cisa.gov/news-events/ics-advisories)
- **Further reading:** *Industrial Network Security* — Eric D. Knapp & Joel Thomas Langill (Syngress)
- *Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

**Image credits:** centrifuge cascade — U.S. Department of Energy (PD) · AR-924 pager — TobiToaster, CC BY-SA 4.0 · kill chain — Wikipedia (CC BY-SA) · IT/OT convergence, CSF cycle, AV logos, Datadog dashboard, *Hackers* still — from the original course deck

</small>

---
layout: end
class: text-center
---

# Thank you

**Questions?**

