---
theme: default
colorSchema: light
title: Lecture 3 — Authentication and Key Establishment
info: |
  ## ISC — Lecture 3 · Authentication
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
---

# Authentication and Key Establishment

<font size=4>Proofs of identity, factors, and protocols</font>

<div class="mt-12 py-1" @click="$slidev.nav.next" hover:bg="white op-10">
  Press Space for next slide
</div>

<!--
Welcome students; frame the lecture around proving who you are — and agreeing on secrets.
-->

---

# Who do we authenticate?

::right::

# Users

- The **human operator**
- Authentication is typically **slow**
- Local or over-the-wire
- Authentication only
- The human brain cannot do proper cryptography just yet :((

---

# Principals

- The user's **digital identity**
- Authentication should be **fast and scalable**
- Mostly over-the-wire
- Goal: **Authentication & key establishment**

<!--
Users authenticate once; principals keep authenticating at machine speed.
-->

---

# AAA framework

<v-clicks>

1. **Identify** — map a real person/subject to a virtual account
2. **Authenticate** — request a proof from the account
3. **Authorize** — verify if the account can access a resource
4. **Accounting** — log/monitor what the account is doing

</v-clicks>

---

# Identification vs. authentication

- **Identification** — *one-from-many*
  - Find your fingerprints in a police database
- **Authentication** — *one-to-one* relation
  - Compare your (based on the username) input to a previously saved one

::right::

# Enrollment vs. recognition

- **Enrollment** — can be slow, must be precise
- **Recognition** — must be quick

- **Cooperation:**
  - Identification: the user does **not** cooperate
  - Authentication: the user **is** cooperative

---

# Just authentication?

- Is authentication alone enough?
  - **Yes** for local systems (e.g., console/GUI login)
  - Not very good for remote systems (e.g., telnet) → **session hijack**

- Key establishment only?
  - For **anonymity** purposes
  - Not very practical (e.g., plain D–H over a MitM channel)

> Usually: we do **both**!

---

# Attacks on protocols?

| Attack         | Short description                                                     |
| -------------- | --------------------------------------------------------------------- |
| replay         | reusing a previously captured message in a later protocol run         |
| reflection     | replaying a captured message to the originating party                 |
| relay          | forwarding a message in real time from a distinct protocol run        |
| interleaving   | weaving together messages from distinct concurrent protocols          |
| middle-person  | eavesdropping on communication                                        |
| bruteforce     | usable for short credentials (e.g., PIN codes without rate limiting)  |
| dictionary     | using a heuristically prioritized list in a guessing attack           |
| forward search | feeding guesses into a one-way function, seeking output matches       |
| pre-capture    | extracting client OTPs by social engineering, for later use           |

---
layout: section
---

# Authentication

---

# The concept

- The **authenticator** (e.g., server, website) asks to prove that you are who you pretend to be, based on one or more pieces of evidence called **factors**.
- May also be **mutual**: the server also authenticates to the client!
- Evidence can be presented:
  - **directly** (e.g., password authentication)
  - **indirectly**, by using it in a cryptographic calculation (e.g., challenge-response protocol)
- Indirect proof uses cryptographic algorithms — also known as **implicit authentication**

---

# Types of factors

<v-clicks>

- Something you **know** (Knowledge Factor)
- Something you **have** (Possession Factor)
- Something you **are** (Inherence Factor)
- Other authentication attributes:
  - Somewhere you are
  - Someone you know

</v-clicks>

---

# Chaining factors

- **N-factor authentication**
  - Factors should be **different**
- **N-step verification**
  - Can be the **same** factor

[rublon.com — 2FA vs 2SV](https://rublon.com/blog/2fa-2sv-difference/)

---

# Something you know — Passwords

- Require people to remember them
- Used on multiple occasions
- Shoulder surfing / key logging
- Can be enhanced through policies (e.g., minimum 20 characters)

> **44 million Microsoft users** reused passwords in the first three months of 2019 —
> identified against a database of **3 billion** publicly leaked credentials.

---

# Most common passwords

- Top lists change very little year to year

[nordpass.com — most common passwords](https://nordpass.com/most-common-passwords-list/)

::right::

> THROUGH 20 YEARS OF EFFORT, WE'VE SUCCESSFULLY TRAINED EVERYONE TO USE PASSWORDS THAT ARE HARD FOR HUMANS TO REMEMBER, BUT EASY FOR COMPUTERS TO GUESS.
>
> — [xkcd.com/936](https://xkcd.com/936/)

---

# Something you have

- Phone number / email
- Public / private key
- Symmetric key

**Best:** on a **hardware token** (write+execute-only private keys)

---

# Something you are

- Fingerprint
- Facial recognition
- Speech recognition
- Odour recognition
- Gait

::right::

# Biometric properties

- **Not 100% accurate**
  - Because of sensors
  - Because of changes in biometrics
- **Not 100% applicable**
  - E.g., fingerprints w/o hands
- Typically **hard to profile, easy to collect/verify**
  - E.g., scanning of face multiple times to enable FaceID on Apple

---

# Storing passwords

- **Plain text** — just don't
- `Hash(Password)`
- `Hash(Salt + Password)`
- `Hash(Salt + Password + Pepper)`

---

# Attacks on stored passwords

**Offline:**

- Brute force
- Dictionary (better: crunch wordlists)

::right::

**Online:**

- Rate-limit
- Lock out after N failed attempts
- Some cryptographic hardware devices are 'online'!

---

# Storing keys

- Which factor is a random key?
- **Software-protected** memory / files
  - `chmod 600`
  - E.g., SSH keys, WebAuthn 'passkeys'
  - → Weakest "something you have" factor!
- **Hardware** Security Tokens / **TPM**
  - Key becomes a stronger "something you have"
  - Requires online attacks → rate limiting, auto-wipe after 10 failures etc.

---

# Password managers

- One ring to rule them all
- Master key can be derived from a password
- Use multiple factors (e.g., tokens)!
- Database storage: local or cloud
- Encourage **different password per service**: password generators, browser integration
- **Back it up** / don't forget/lose the keys!

---

# Password-based key derivation

- Problem: passwords have **arbitrary lengths**
- Cryptographic algorithms require keys of **specific lengths**
  - E.g., AES-256 requires a 256-bit key → 32 bytes
- Solution: **Key Derivation Functions (KDF)**:

```
DerivedKey = KDF(password, salt, iterations)
```

- Algorithms: **PBKDF2**, **Argon2**
- E.g., per-domain derived passwords: [spectre.app](http://spectre.app)

---

# FIDO2 / passkeys

- Previously: **U2F** — Universal Second Factor
- **FIDO2 WebAuthn** → asymmetric crypto!
- Give a **unique public key** to the web server (no reuse!)
- Use the private key **instead of a password**
- Private key must be stored on **secure hardware**!
- FIDO-certified security keys: Yubikey, SoloKey, NitroKey ;)
- Hardware validates the 2nd factor:
  - Something you **know** (PIN — rate limited!)
  - Something you **are** (fingerprint, FaceID etc.)
- **Must always enroll backup keys!**

---
layout: section
---

# One-time passwords

---

# OATH one-time pass standards

- **OATH**: **HOTP** & **TOTP**
- **TOTP**: [RFC 6238](https://datatracker.ietf.org/doc/html/rfc6238)

```
TOTP = HOTP(K, T)
T = unix_timestamp / 60   (expiry time, e.g., 30 or 60 s)
```

- **Private key shared** between user and auth server

---
layout: section
---

# Key establishment protocols

---

# Authentication protocols

- **Symmetric** (shared secret)
  - How to ask for a known secret over insecure channels?
  - Hash the password? → **Challenge-Response**
- **Asymmetric** protocols
  - **Diffie–Hellman**!
  - **Forward secrecy**

---

# Burrows–Abadi–Needham notation

- $ID_A$, $ID_B$, $ID_S$ — unique identifiers for A, B and S (Trusted Server)
- $k_{A,B}$ — a key shared between A and B
- $\{ID_A\}_{K_A}$ — encryption/signature of $ID_A$ under the key of A
- $A \to B : \{ID_A\}_{k_{A,B}}$ — A sends to B the message $ID_A$ encrypted by the shared key of A and B

---

# Plain Diffie–Hellman — classic MitM

```
Attacker Trudy:
1. A -> T : DH_A
2. T -> B : DH_T
3. B -> T : DH_B, {ID_B} k_T,B
4. T -> B : {ID_A} k_T,B
5. T -> A : DH_T, {ID_B} k_A,T
... etc.
```

::right::

```
A and B (think) they talk:
1. A -> B : DH_A        (g^a mod p)
2. B -> A : DH_B, {ID_B} k_A,B   (both obtain the same k_A,B)
1. A -> B : {ID_A} k_A,B
```

<!--
Trudy terminates two separate DH exchanges and relays identities.
-->

---

# Protocol for asymmetric encryption (STS simplified)

```
1. A -> B : DH_A
2. B -> A : DH_B, { {DH_A, DH_B} pubA } k_A,B
3. A -> B : { {DH_A, DH_B} pubB } k_A,B
```

- We assume each party has private/public keys
- Public keys known to all entities
- The problem is **how to distribute public keys**
  - **Public Key Infrastructure**
  - **Pretty Good Privacy**

---

# Symmetric authentication

- Given A and B who trust **S**, A and B should be able to create a shared key $k_{A,B}$ for secret communication
- $k_{A,B}$ known only to A and B (and possibly to S)
- A and B should know $k_{A,B}$ is **newly generated**
- A and B should **authenticate** each other

> Why? **Enterprise authentication!**

---

# Symmetric protocol (1) — naive

```
1. A -> S : ID_A, ID_B                (I am A, give me key for B)
2. S -> A : k_A,B                     (key transferred in unencrypted form)
3. A -> B : ID_A, k_A,B               (key transferred in unencrypted form)
```

**Possible attacks:**

- An attacker with MITM capabilities gets $k_{A,B}$

---

# Symmetric protocol (2) — encrypted at the server

```
1. A -> S : ID_A, ID_B
2. S -> A : {k_A,B} k_A,S             (encrypted with A,S shared secret)
3. A -> B : ID_A, {k_A,B} k_B,S       (encrypted with B,S shared secret)
```

**Possible attack — reflection:**

```
3'. A -> T : ID_A, {k_A,B} k_B,S
4'. T -> B : ID_T, {k_A,B} k_B,S
```

(Trudy replaces the identity A presented to B!)

---

# Symmetric protocol (2') — Trudy in the middle

```
1. A -> T : ID_A, ID_B
2. T -> S : ID_A, ID_T
3. T -> A : {k_A,T} k_A,S, {k_A,T} k_B,S  (from S)
4. T -> B : ID_T, {k_A,T} k_B,S           (as if from S, for A)
```

Trudy in the middle …

<!--
Every message looks legitimate because each is sealed by S.
-->

---

# Symmetric protocol (3) — include IDs

```
1. A -> S : ID_A, ID_B
2. S -> A : {k_A,B, ID_B} k_A,S, {k_A,B, ID_A} k_B,S
3. A -> B : ID_A, {k_A,B, ID_A} k_B,S
```

**Possible attacks:**

- **Replay** of an old (broken) key

---

# Protocol (4) — Needham–Schroeder (1978)

```
1. A -> S : ID_A, ID_B, N_A
2. S -> A : {k_A,B, ID_B, N_A, {k_A,B, ID_A} k_B,S } k_A,S
3. A -> B : {k_A,B, ID_A} k_B,S
4. B -> A : {N_B} k_A,B
5. A -> B : {N_B - 1} k_A,B
```

**Possible attack — Denning–Sacco replay:**

```
1. T -> B : { k'_A,B, ID_A } k_B,S     (old broken key)
2. B -> T : {N_B} k'_A,B
3. T -> B : {N_B - 1} k'_A,B
```

---

# Symmetric protocol (5) — final form

```
1. B -> A : ID_B, N_B
2. A -> S : ID_A, ID_B, N_A, N_B
3. S -> A : {k_A,B, ID_B, N_A, N_B, {k_A,B, ID_A, N_B} k_B,S} k_A,S
4. A -> B : {k_A,B, ID_A, N_B} k_B,S
```

**Possible attacks:**

- **None of the above** (of our list)

---

# Notes on protocols — Abadi & Needham

- If the identity of a principal is essential to the meaning of a message, mention the principal's name **explicitly** in the message
- Be **clear about why** encryption is being done
- When a principal signs material that has already been encrypted, it should **not** be inferred that the principal knows the content of the message
- Be clear about what **properties** you are assuming about **nonces**
- If **timestamps** are used as freshness guarantees, then the difference between local clocks at various machines must be **much less** than the allowable age of a message

---
layout: section
---

# Digital Identity

---

# European Digital Identity

- Digital identity for **all Europeans**
- Every EU citizen and resident will be able to use a **personal digital wallet**
- Usable for **online and offline** public and private services across the EU
- Key principles: user control of what data is shared, and how

> "One that we trust and that any citizen can use anywhere in Europe to do anything from paying your taxes to renting a bicycle."
>
> — Ursula von der Leyen, State of the Union, 16 September 2020

---

# NIST SP 800-63 Digital Identity Guidelines

| Document     | Title                                     | URL |
| ------------ | ----------------------------------------- | --- |
| SP 800-63-3  | Digital Identity Guidelines               | [doi.org/10.6028/NIST.SP.800-63-3](https://doi.org/10.6028/NIST.SP.800-63-3) |
| SP 800-63A   | Enrollment and Identity Proofing          | [doi.org/10.6028/NIST.SP.800-63a](https://doi.org/10.6028/NIST.SP.800-63a) |
| SP 800-63B   | Authentication and Lifecycle Management   | [doi.org/10.6028/NIST.SP.800-63b](https://doi.org/10.6028/NIST.SP.800-63b) |
| SP 800-63C   | Federation and Assertions                 | [doi.org/10.6028/NIST.SP.800-63c](https://doi.org/10.6028/NIST.SP.800-63c) |

---
layout: section
---

# Federation &amp; assertions

---

# Single Sign-On (SSO)

- **Password managers**
- **Enterprise level SSO**
  - Same-domain authentication
  - Kerberos, RADIUS with LDAP / Active Directory databases
- **Federated Identity**
  - Cross-domain authentication
  - Based on **assertions** containing the result of authentication
  - Factors **cannot** be shared between domains
  - RADIUS, **OpenID Connect**, **SAML** etc.

---

# Kerberos

- Developed by **MIT in 1983**
- Was **banned for export** till 2000 by the US
- Used for key establishment between multiple entities
- The Kerberos server is **trusted** by all entities
- Assumes existing pre-shared keys between entities and the Kerberos server
- Can be adapted to multiple symmetric encryption algorithms
- **Kerberos v5 uses AES**

---

# Kerberos — assumptions

- The adversary can **compromise the network**, not the host (e.g., secrets, keys)
- Based on the fixed **Needham–Schroeder** protocol
- Uses **tickets** to create a legitimate session key

---

# Kerberos (v1) protocol

```
1. A -> KAS : ID_A, ID_B, N_A
2. KAS -> A : {k_A,B, ID_B, T_KAS, N_A} k_A,KAS, {k_A,B, ID_A, T_S} k_B,KAS
3. A -> B : {k_A,B, ID_A, T_KAS} k_B,KAS, {ID_A, T_A} k_A,B
```

- $k_{A,B}$: session key between A and B
- $\{k_{A,B}, ID_A, T_{KAS}\}_{k_{B,KAS}}$: **ticket** for A to use when contacting B
- $T_A > T_{KAS}$: B validates the time window by comparing $T_A$ and $T_{KAS}$

<!--
KAS = Kerberos Authentication Server; T_S = Timestamp server.
-->

---

# Kerberos (v2)

- Usually the shared key between A and KAS is **derived from a user input/password**
- The previous version requires **credentials input every connection** to a new application server (B)
- **Ticket granting separate from user authentication:**
  - User authenticates using passwords with KAS and receives a session key for the **Ticket Granting Service**
  - Entities use that session key to request tickets for multiple applications

---

# SAML

- **Security Assertion Markup Language** — XML-based federation format
- Carries authentication results as **assertions** between domains

---

# RADIUS / EAP

- **RADIUS** — central authentication, authorization and accounting protocol
- **EAP** — Extensible Authentication Protocol
  - Wraps authentication methods (e.g., EAP-TLS, EAP-PEAP)
  - Common in Wi-Fi (802.1X) and remote access

---
layout: end
class: text-center
---

# Thank you

**Further reading:**
*Computer Security and the Internet: Tools and Jewels* — Paul C. van Oorschot (Springer, 2021)

[people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)
