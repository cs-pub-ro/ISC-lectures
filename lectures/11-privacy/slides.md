---
routerMode: hash
download: 'slides.pdf'
theme: default
colorSchema: light
title: Lecture 11 — Privacy Preserving Technologies
info: |
  ## ISC — Lecture 11 · Privacy
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
---

# Privacy Preserving Technologies

<font size=4>Tracking, regulation, and ways to resist both</font>

<div class="mt-12 py-1" @click="$slidev.nav.next" hover:bg="white op-10">
  Press Space for next slide
</div>

<!--
Welcome students; today: how we are watched, who regulates it, and the technologies that fight back.
-->

---

# Objectives

- Internet Tracking
- Regulation: **GDPR, IAPP**
- Privacy solutions:
  - VPNs
  - Mix Nets / Onion routing / TOR
  - Private Information Retrieval (PIR)
  - ORAM
  - Decentralization

---
layout: quote
class: text-center
---

# Motivation

'There was of course no way of knowing whether you were being watched at any given moment...You had to live - did live, from habit that became instinct - in the assumption that every sound you made was overheard and, except in darkness, every movement scrutinized.'

— George Orwell, *1984* (1948)

---

# Digital privacy

- 'There is no privacy in the digital age.'
  - Ubiquitous data collection
  - Mobile platform duopoly
- 'No one cares about privacy anymore.'
  - Centralized social networks
- 'If you haven't done anything wrong you have nothing to hide.'
- **yet …**
  - Stolen address databases fuels global SPAM mails, phone scams etc.!

---

# How are we tracked?

- **Source IP address**, traffic sniffing (e.g., DNS requests)
- **Behavioral tracking**
- **Browser / device fingerprinting**
- Web tracking:
  - Cookies
  - Pixels
  - Ads
  - **Third party JavaScript** (e.g., social network snippets / marketing / analytics)
- **Centralization** (CDNs / social media / browser monopoly etc.)

---

# Mass surveillance / legal tracking

- **UKUSA (1941)**
  - The **Five Eyes**: USA, Australia, Canada, New Zealand, and the UK
  - In 1975 the United States revealed the existence of the **NSA**
- **ECHELON (1971)**
  - mass surveillance and industrial espionage
- **CALEA** (Communications Assistance for Law Enforcement Act, 94)
  - 'China had been tapping communications in the U.S. using that infrastructure for months' 🥲
- **PRISM (2007)**
  - collects network traffic from all US major online service providers
  - must have warrant to intercept traffic
- **TEMPEST**: spying through leaking EM emanations

---

# Legitimate reasons (ofc)

**● 'Hacker-ul român care a spart serverele NASA a fost reținut de procurorii DIICOT' (RO)**

::right::

**● 'U.S. Charges Russian Man as Boss of LockBit Ransomware Group' (EN, May 7, 2024)**

- Sanctioning of Dmitry Khoroshev as the alleged leader of LockBit, jointly with UK & Australia

---

# Web tracking

- HTTP Origin request header
- **Tracking URLs**
  - via query string parameters
- **Cross-Site Tracking Cookies/JavaScript**
  - Google Analytics, Facebook/Twitter/TikTok Share widgets etc.
- **Spy Pixel**
  - Email client makes remote request to display image, contains unique ID / email hash

---

# Device fingerprinting

- Build a **multi-variable vector**:
  - User's IP address + Geo Location, VPN / local network IP address
  - Operating System / User agent / browser version
  - HTTP request headers
  - Cookies / history (`:visited` colors on links — by JS)
  - Plugins / fonts / browser extensions
  - Screen resolution / battery info / CPU/GPU statistics
  - Settings (time zone, language)
- **Identify user across networks & devices → Profit!**

---

# Cloud centralization

- Cloud hosting & CDNs:
  - CloudFlare, Google, AWS
- **TLS connections are terminated by cloud provider ingress servers!**
- Hosted libraries / fonts
  - Load JS libraries from Google & GitHub
  - Web-based font requests logged
- Behavioral tracking: websites + social media
  - Marketing dept. dream: mouse pointer tracking → Heat Map
  - Doom Scrolling → user pauses → record interests!

---

# Web browser monopolies

- **IE 5-8 era:** Microsoft controlled 'web standards'
- **2024:** Google controls web standards..
- **Google Chrome: Manifest v3**
  - Removed **webRequest** API
  - Use declarative Net Req. API instead!
  - Rules limit, no behavioral ad blocking …
  - **No uBlock for you!**
- **Federated Learning of Cohorts (FLoC)**

---

# Corporate harvesting

- **Commercial:** Amazon, Google, Facebook, Apple [12]
- **Data Brokers** (information resellers):
  - Target services: marketing / advertising, financial services / fraud detection, people search etc.
  - Data acquisition: web tracking, public record scraping, commercial sharing/selling (by card transactions, retailers & advertising companies)
- How? You simply **agree to it** (check License Agreement)
- Government agencies often **bypass warrant requirements** by doing commercial agreements with companies (

---

# Regulatory approach: GDPR

- 'The **General Data Protection Regulation (GDPR)** is the toughest privacy and security law in the world.'
- Disclose any data collection
- **Right to be forgotten**
- **Data minimisation**
- Only collect / store required personal information
- Exemptions: law & national security
- Downloading / exporting your personal data from providers

---

# GDPR effects

- French watchdog slaps **Google with $57 million fine** under new EU law
  - *Jan 21, 2019*
- 'I'm glad Swedish television is taking seagull privacy so seriously' (ofc)

---

# Not only GDPR anymore

- The GDPR has inspired many imitators:
  - Brazil's **LGPD**
  - California's **CCPA**
- While many of these laws agree on the broad terms of data protection, each implements these protections in its own way
- US states (Nevada, New York, Texas, Washington) following California's lead

---

# IAPP

- GDPR training?
- **International Association of Privacy Professionals**

[iapp.org/certify](https://iapp.org/certify/programs/)

---
layout: section
---

# Definitions

---

# Privacy concepts

- **Anonymity:** the state of being unidentifiable
- **Pseudonymity:** the use of pseudonyms as IDs — allows both privacy protection and accountability
- **Unobservability:** ensures that a user may use a resource or service without others being able to observe that the resource or service is being used
- **Unlinkability** of sender and recipient (relationship anonymity): it is untraceable who is communicating with whom

---

# Privacy-Enhancing Technologies (PETs)

1. **PETs for minimizing/avoiding personal data** (Anonymity, Pseudonymity, Unobservability, Unlinkability)
   - At communication level: VPN, MixNet, Onion Routing, TOR, Crowds
   - At application level: Anonymous Ecash, Private Information Retrieval, Anonymous Credentials
2. **PETs for the safeguarding of lawful processing**
   - Platform for Privacy Preferences Project (P3P) / Do Not Track
   - Privacy policy languages
   - Transparency Enhancing Tools (TETs)
3. **Combination of 1 & 2**
   - Privacy-enhanced Identity Management

---
layout: section
---

# VPNs

---

# VPNs

- **Virtual Private Network**
- Use cases: business (corporate) / user privacy (consumer)
- **Consumer VPN services:**
  - for privacy / bypass geoblocking (e.g., Netflix) & censorship
  - E.g., ProtonVPN, ExpressVPN, NordVPN, Mullvad etc.
- Anonymization & logging
- Security vulnerabilities
- **Hot! Tunnel Vision (CVE-2024-3661)** [13]

---

# CVE-2024-3661 — typical routing table

- Static route injection via **DHCP option 121** will bypass any VPN default GW :D
- Most VPN services & OS platforms are vulnerable

```
141.85.241.131/32 via 192.168.0.1 dev eth0 metric 100
10.13.37.0/30 dev tun0 scope link src 10.13.37.2 metric 100
192.168.0.0/24 dev eth0 scope link src 192.168.0.100 metric 100
0.0.0.0/0 via 10.13.37.1 dev tun0 metric 50
```

---

# CVE-2024-3661 — after the attack

Static route injection via DHCP option 121:

```
141.85.241.131/32 via 192.168.0.1 dev eth0 metric 100
10.13.37.0/30 dev tun0 scope link src 10.13.37.2 metric 100
192.168.0.0/24 dev eth0 scope link src 192.168.0.100 metric 100
0.0.0.0/1 via 192.168.0.1/24 dev eth0 metric 100     <-- traffic leaks
0.0.0.0/0 via 10.13.37.1 dev tun0 metric 50
```

<!--
The injected /1 route is more specific than the VPN default route — traffic goes clear.
-->

---

# Mix Networks

- Use one or many **proxy servers**, mixing traffic
- Input **encrypted with public key of mixer**
- Mixer decrypts and extracts **next hop address**
- Anonymization of **sender-destination relationship**
- **High latency:** mixer must wait & aggregate multiple messages before sending them

---

# Onion routing

- Originator picks path through multiple nodes, encrypts packet in **multiple layers** with each node's public key (Matryoshka-like encapsulation)
- Each intermediary node **decrypts with own key** and forwards it
- Result: **anonymization overlay network**
- First + Last-Hop-based vulnerabilities in low-latency networks:
  - **Timing correlations**
  - **Message length** (no. of packets traversing network)

---

# TOR

- **No mixing** is employed, just onion network overlay (low-latency)
- Uses **SOCKS encapsulation** of application traffic
- TOR server may be hosted on separate device (e.g., Raspberry PI)

---

# Mixnets vs Onion routing

> 'Tor plays with **space alone** (the bytes that you send across the network go through various other servers thus they aren't where they are supposed to be) and mixnets play with both **space and time** (adds delays and shuffles the request through various servers as well).'

---

# Pretty Good Privacy

- **Web-of-Trust**
- Peer-to-peer model
- Individuals digitally sign each other keys
- Different levels of trustworthiness
- E.g., ultimately trust your friends
- Implementation: **gpg**
- Used by Linux package managers, git signatures, pass managers etc.
- Unpopular due to UX/learning curve

[keys.openpgp.org](https://keys.openpgp.org/)

---

# Off-the-Record protocol

- Problem: peer to peer chat, end to end encryption
- Use PGP? Long term private key compromised → **entire chat history becomes decryptable!**
- **OTR → perfect forward secrecy!**
- **Non-repudiability vs forgeability**
- Use **Malleable Encryption**:
  - change 1 bit in plain text → changes in ciphertext, too!
  - XOR-based cipher, e.g., stream / CTR / GCM block modes etc.

---

# Private Information Retrieval (PIR)

- Privacy for the **item of interest**:
- Allows a user to retrieve an item from a database server **without revealing which item** he is interested in
- Application example: patient database
- Simple (but expensive) solution:
  - Download all database entries and make local selection
- Cryptographic generalization: **Oblivious Transfer (OT)** [14]

---

# Oblivious RAM

- Problem: Trusted Execution Environments, encrypted RAM …
  - have **location + timing side channels** → data is still insecure!
- **Oblivious RAM:** compiler that translates code to another one, same function, **randomized memory access patterns**
- Naive implementation: for each read/write instruction, do a full memory scan → **O(n) overhead!**
- More efficient (but simple) methods exist: **Path ORAM** [15]

---
layout: section
---

# Practical privacy

---

# Web privacy

- Don't use big tech-owned browsers (Chrome, Edge)
- Use **Open Source** variants: Firefox & Chromium
- Privacy extensions:
  - Privacy Badger
  - uBlock Origin / Adblock
  - Disconnect
  - Ghostery, LocalCDN, DecentralEyes etc.
- Block / isolate **third party cookies** (e.g., Facebook Container)
- Use **Encrypted DNS** (dnscrypt-proxy / Firefox DNS over HTTPS)!

---

# Privacy: future work

- Decentralized social networks (Mastodon, Bluesky)
- **Personal Cloud** (e.g., Self-Hosted on a Raspberry PI)
- **pi-hole**: local network ad-blocking / privacy proxy & DNS
- Use privacy-focused OSes / apps
  - **Tails**: Amnesia Incognito Live System
- Sandboxed Applications (Containers)

---

# Decentralized currencies

- E.g., Bitcoin, Ethereum, Monero, DogeCoin etc.
- **Blockchain**: huge transaction ledger cryptographically protected from modification
- Consensus: **Proof of Work** vs **Proof of Stake**
- Anonymization via **mixers** (alt name: tumblers)!
- Issues: no rollback, energy-intensive, financial fraud, money laundering etc.

---
layout: end
class: text-center
---

# Thank you

**Further reading:**
*Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
