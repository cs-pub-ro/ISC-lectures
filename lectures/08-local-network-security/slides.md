---
theme: default
colorSchema: light
title: Lecture 8 — Local Network Security
info: |
  ## ISC — Lecture 8 · Local Network Security
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
---

# Local Network Security

<font size=4>Attacks and defenses across the network layers</font>

<div class="mt-12 py-1" @click="$slidev.nav.next" hover:bg="white op-10">
  Press Space for next slide
</div>

<!--
Welcome students; frame this lecture around how attackers and defenders operate across the OSI layers within a local network.
-->

---
layout: section
---

# Network attacks

---

# Network attacks

<v-clicks>

- **Reconnaissance**
  - Ping sweep / Port Scan
  - Sniffing
- **Availability**
  - [Distributed] Denial of Service
  - Amplification / reflection
- **Unauthorized Access**
  - Traffic alteration (Man-in-the-Middle)
  - Authentication (password / protocol breakage)
  - Remote Code Execution

</v-clicks>

---

# OSI model

<!--
Playful mapping from the Purdue essay.
-->

| Dwarf    | Layer        | Gist |
|----------|--------------|------|
| Sleepy   | Physical     | Physical connections are boring |
| Sneezy   | Link         | Watch packets to see the "sneezy" pattern |
| Happy    | Network      | Everyone's happy with the Internet Protocol |
| Doc      | Transport    | It takes a Ph.D. to get transport right |
| Dopey    | Session      | A "dopey" unnecessary layer for comic relief |
| Bashful  | Presentation | Too "bashful" to appear in public |
| Grumpy   | Application  | Programmers and users always complain |

[Source [1]](https://www.cs.purdue.edu/homes/dec/essay.network.layers.html)

---

# L1: wire / fiber tapping

- You can buy one of these for ~**350$**
- Detect an attack like this by **loss of light**
  - Must be lower than **2%** in an acceptably-quality implementation

<!--
Physically tapping a line: cheap tools, detectable via light loss.
-->

---
layout: section
---

# L2 security

---

# L2 attacks

<v-clicks>

- **MAC Spoofing**
- **MITM attacks from insiders**
- **ARP Spoofing**
- **STP injection**
- **VLAN hacking**
  - VLAN hopping, Cisco DTP emulation, etc.
- Not on the same network?
  - Hack into the CEO's smart coffee machine / TV via its cloud service ;)
- **yersinia** — framework for L2 attacks (linux)

</v-clicks>

<!--
Note the lateral move: if not on the same network, pivot via a cloud-connected device.
-->

---

# ARP poisoning

- **ARP is unauthenticated!**
- Device's OS receives two ARP packets — who to trust, first / last?
- **Fix:** static ARP entries …
- **Better:** detection and alerting!

<!--
Emphasize: ARP has no authentication; the real fix is detection, not just static entries.
-->

---

# STP injection

- Insert a rogue bridge to manipulate the Spanning Tree Protocol topology

<!--
Rogue switch/bridge alters STP so traffic routes through the attacker.
-->

---

# VLAN hopping

- Trick the switch into treating untagged traffic as a different VLAN
- E.g., via double-tagging or DTP (Cisco) emulation

---

# Wardriving

- Driving around & cracking WiFis
- Tools: **aircrack-ng** + supported drivers :(
- + portable devices (rooted mobile phones, embedded SBCs, etc.)
- [WiFi Pineapple](https://shop.hak5.org/products/wifi-pineapple)
- [DIY: pwnagotchi](https://pwnagotchi.ai/)
  - Raspberry PI Zero-based, captures crackable WPA key material
  - With AI / auto-tuning capabilities

<!--
Modern wardriving is cheap and portable.
-->

---

# L2 protection

<v-clicks>

- Static ARP entries + **DHCP binding**
- **Sticky MAC** / switch port security
- **BPDU Guard**
- Secure wireless passwords
- **802.1x** / WPA Enterprise

</v-clicks>

<!--
These counter the specific L2 attacks just listed.
-->

---

# 802.1x

- Network devices enforcing different security policies

<!--
Port-based network access control; pairs with WPA Enterprise for wireless.
-->

---
layout: section
---

# L3 attacks

---

# L3 attacks

<v-clicks>

- **IP spoofing**
- **DHCP spoofing**
- **Source Routing** (SSRR / LSSR headers)
  - Sender can specify the path the packet should take through the network
- **Routing protocol spoofing**
  - Yet another MitM 🤖
- **[Distributed] Denial of Service!**

</v-clicks>

---

# DHCP spoofing

- DHCP uses **broadcast** (multicast for DHCPv6) over local network
- **Any server can declare itself authoritative!**
- Attacker makes itself **default gateway + DNS**
- **Bonus:** block responses from the legitimate DHCP (e.g., via L2 MAC spoofing the switch)
- **CVE-2018-5732**
  - Failure to properly bounds-check a buffer for DHCP options allows a malicious server to cause a buffer overflow …

<!--
Show how a rogue DHCP becomes the gateway/DNS: trivially a network MitM.
-->

---

# Routing protocol attacks

- **OSPF spoofing** …
  - [draft-ietf-rpsec-ospf-vuln](https://datatracker.ietf.org/doc/html/draft-ietf-rpsec-ospf-vuln-02)
- Mitigations:
  - **TTL Security Check** (value should be 255)
  - Add authentication for messages (preferably different for each router-link)
  - **OSPFv2 HMAC-SHA** from secret and message
- **BGP spoofing** …
  - (Sub)Prefix Hijacking
  - "China Telecom has been using poisoned internet routes to suck up massive amounts of US and Canadian internet traffic" — 2018 [12]

<!--
BGP prefix hijacking is a real-world, large-scale routing attack.
-->

---
layout: section
---

# L4: TCP/IP attacks

---

# L4: TCP/IP attacks

<v-clicks>

- Ping sweep / Port scanning
- **TCP sequence number prediction**
  - Inject counterfeit packets into stream
- Encrypted protocols? **Replay attacks!**
- Does **NAT** help with security?
  - Nope … But most NAT SoHo have stateful firewalls enabled!

</v-clicks>

[Source [4]](https://www.cs.columbia.edu/~smb/papers/ipext.pdf)

---

# Port scanning

- **TCP:**
  - **SYN/ACK** — easily detectable (OS records connection)
  - **SYN-only** — more stealthy, also used for flooding ;)
  - **X-MAS** — set many TCP flags, check server response
- **Protection?**
  - `iptables`' set module — rate limits scans from same sender
  - Use **IDS/IPS** system!
  - **Port knocking**
    - Hide important ports (e.g., ssh) from prying eyes!

<!--
Explain stealthy scan variants and cheap defenses like port knocking.
-->

---

# (Distributed) Denial of Service

- Examples: **TCP SYN Flood**
- **Distributed:** via botnets
  - **Zombies:** malware-infected machines
  - **Mirai Botnet:** IoT/routers
- Cannot be **blocked**, only **sinked!**
- Cloud-based reverse proxies (e.g., **Cloudflare**)

<!--
Key idea: DDoS can't be blocked at the edge, only absorbed/sunk.
-->

---

# DDoS: reflection / amplification

- Attacker **spoofs source IP address**
- Sends lots of requests to server
- Server replies **larger packets** to the spoofed victim
- Victim overflows with traffic
- Most **UDP services** are usable (DNS, QUIC, unauthenticated pub/sub, etc.)
- **Memcached** misconfiguration

<!--
Reflection turns a helper server into an attacker; amplification scales it.
-->

---

# L3 protection? Firewalls!

<v-clicks>

- **Access control**
  - `netfilter/iptables`: match traffic … `-j ACCEPT|DROP`
- **Layer X Firewall:** understanding of OSI level X or lower protocols
- Must be **fast!**
- **Stateful** vs. **Stateless**
- **Whitelisting** vs. **Blacklisting**
- Next-gen firewalls: **Deep Packet Inspection**
- **Virtual Private Networks (VPN)**

</v-clicks>

<!--
Firewalls are the primary L3 control; contrast stateful vs. stateless.
-->

---

# Networking equipment manufacturers

- Huge market!
- Palo Alto
- Fortinet
- Cisco
- Juniper
- Check Point
- Forcepoint
- Sophos
- Huawei

<!--
Big vendors; note that size does not imply security (next slide).
-->

---

# Intrusion Detection/Prevention Systems

- Intrusion detection is a **classification problem**
- **Proprietary** vs. **Open Source** (Snort, Suricata, etc.)
- Based on **signatures**
  - How to be fast? algorithms, GPU / FPGA

| Reality          | True       | False      |
|------------------|------------|------------|
| **Detection True** | True Positive   | False Positive |
| **Detection False** | False Negative  | True Negative |

<!--
Frame IDS/IPS as classification: explain TP/FP/FN/TN trade-offs.
-->

---

# Networking equipment attacks

- How do you figure out if a router/firewall is compromised?
- **Cisco Security Advisories:** 4854 vulnerabilities (as of 14.04.2024)
  - **CVE-2023-20198:** Multiple Vulnerabilities in Cisco IOS XE Software Web UI Feature
  - **CVE-2023-20214:** Cisco SD-WAN vManage Unauthenticated REST API Access Vulnerability
- **Palo Alto:** CVE-2024-3400 PAN-OS — OS Command Injection in GlobalProtect
- **Fortinet:** CVE-2023-42790 — FortiOS & FortiProxy — Out-of-bounds Write in captive portal

<!--
Point out: even top vendors ship serious, real vulnerabilities.
-->

---
layout: section
---

# Service & protocol security

---

# DNS security

- DNS requests and responses are **not authenticated**
- DNS relies heavily on **caching** for efficiency, enabling **cache pollution** attacks
- **DNSSec:**
  - Each domain signs their 'zone' with a private key
  - Public keys published via DNS
  - Zones signed by parent zones
  - Privacy: **TBD!**

[Source [5]](http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html)

<!--
DNSData is integrity/availability, not privacy — it's still TBD.
-->

---

# SNMP security

- **Simple Network Management Protocol**
- Management Information Base = **MIB**
- Uses standard **OIDs** instead of names, e.g.:
  - `net.snmp.example.heartbeat.rate` → `1.3.6.1.4.1.8072.2.3.2.1`
- **SNMPv1** is simple, effective, and provides the majority of SNMP service in the field
- **SNMPv2** adds some functionality to v1
- **SNMPv3** is a security overlay for either version, not a standalone replacement

<!--
OIDs are dotted-number paths; SNMPv3 layers security, it doesn't replace.
-->

---

# Email security

- **SPF**
- **DKIM**
- **DMARC**

<!--
Three anti-spoofing/anti-phishing mechanisms for domain-based email trust.
-->

---

# Honeypots

- Easy-to-hack environment (hopefully) administered by security personnel
- Used to learn about hackers' behavior, new threats, and/or as decoy
- **Low interaction** (emulated — may be detected) vs. **High interaction** (real OS/apps)
- Virtual Machines as honeypots

<!--
Honeypots are cheap intelligence: study attacks on a sacrificial system.
-->

---

# References

- [1] [https://www.cs.purdue.edu/homes/dec/essay.network.layers.html](https://www.cs.purdue.edu/homes/dec/essay.network.layers.html)
- [4] [https://www.cs.columbia.edu/~smb/papers/ipext.pdf](https://www.cs.columbia.edu/~smb/papers/ipext.pdf)
- [5] [http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html](http://unixwiz.net/techtips/iguide-kaminsky-dns-vuln.html)
- [12] [https://boingboing.net/2018/10/26/bgp-pop-mitm.html](https://boingboing.net/2018/10/26/bgp-pop-mitm.html)

---
layout: end
class: text-center
---

# Thank you

**Further reading:**
*Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
