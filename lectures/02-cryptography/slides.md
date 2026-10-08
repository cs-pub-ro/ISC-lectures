---
routerMode: hash
download: 'slides.pdf'
theme: ../../isc-theme
colorSchema: light
selectable: false
touying:
  preset: isc
title: Lecture 2 — Introduction to Cryptographic Systems
info: |
  ## ISC — Lecture 2 · Cryptography
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
src: ../_shared/intro.md#1
---
---
layout: cover
title: "Lecture 2: Cryptography"
subtitle: "Cryptographic ciphers, protocols, applications and attacks"
---

::default::

---

# This lecture

<v-click>

**Is not about:**

- **Steganography** - concealing a file/message/image/video within another
- **Obfuscation** - hiding program implementation without altering execution (Indistinguishability Obfuscation [9])
- **Cryptocurrency** (//hype gone//)

</v-click>

<v-click>

**Is about:**

- **Cryptography** — the science of writing a secret message;
- **Cryptanalysis** — the science of breaking cryptography;
- **Cryptology** — the overall study of secure communication.

</v-click>

---

# Vocabulary

- **Ciphertext** - result of encryption performed on **plaintext** using an algorithm, the **cipher**:

```
c = encrypt(m, k)
```

- **Decryption** - the reverse process, to obtain the original message:

```
m = decrypt(c, k)
```

---
layout: section
---

# History

---
layout: two-cols
---

# Early encryption schemes

- **~1500 BCE** - clay tablets in Mesopotamia
- Hides a recipe of pottery glaze
- Used **substitution** as an encryption algorithm
- ...and the encryption was broken

::right::

<div class="flex flex-col items-center" style="text-align: center;">

![Tablet (Rimush, Louvre AO 5476)](./images/hist_rimush_tablet.jpg)

<a style="font-style: italic; font-size: 9pt;"
	href="https://commons.wikimedia.org/wiki/File:Tablet_Rimush_Louvre_AO5476.jpg">Tablet (Rimush, Louvre AO 5476)</a>
</div>
<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%; 
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>

---
layout: two-cols
---

# Substitution

- E.g. **Atbash system**, used in the Bible [12]
- Jeremiah 25:26: *"And after all of them, the king of Sheshak will drink it too."*
  - In original Hebrew, the word **Sheshak** commutes into **"Babylon"**

::right::

<div class="flex flex-col items-center" style="text-align: center;">

![Tablet](./images/hist_atbash_cipher.gif)

<a style="font-style: italic; font-size: 9pt;"
	href="https://medium.com/@amangondaliya555/atbash-cipher-70e284ad921e">https://medium.com/@amangondaliya555/atbash-cipher-70e284ad921e
</a>
</div>

<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%;
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>

---

# Transposition

- Characters **change their position** in the text, but keep their original meaning
- E.g. **scytales**: rods wrapped in a strip of leather/papyrus (similar to the Rail Fence Cipher [13])

<div class="flex justify-center items-center">
<div style="margin-top: 2em; width: 70%">

![hist_scytale_cipher.png](./images/hist_scytale_cipher.png)
[toebes.com — Flynns, 1924](https://toebes.com/Flynns/Flynns-19241213.htm)

</div>
</div>

---
layout: two-cols
---

# Fast forward on crypto history

<v-click>

- **Caesar cipher** (100 BCE – 44 BCE)
  - Shift cipher, e.g., k=4 → A→E, T→X …
  - Most of Caesar's enemies would have been illiterate ⇒ secure

</v-click>
<v-click>

- **Vigenère cipher** (1553 CE)
  - Poly-alphabetic substitution

</v-click>
<v-click>

- **1st & 2nd WW** → electro-mechanical cipher machines:
  - **Enigma** for encryption
  - **Bombe** for decryption and cracking

</v-click>

::right::

<div v-after class="flex flex-col items-center" style="text-align: center;">

![Enigma Machine](./images/enigma_museo_scienza_Milano.jpg)
[Military Model Enigma I, 1930](https://en.wikipedia.org/wiki/Enigma_machine)

</div>
<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%;
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>

---
layout: section
---

# Modern cryptography

---

# What does an ideal cipher look like?

<v-clicks>

 - No correlation between **plaintext**, **key**, and **ciphertext**
 - Cannot recover **key** from known plaintext + ciphertext
 - Shannon's **Confusion & Diffusion** !
   > Do unbreakable algorithms exist?

</v-clicks>

<!--
Leave the question open — we'll revisit with One-time Pad and modern ciphers.
-->

---

# The XOR operator

* Most useful crypto building block.

* Properties:

$$
A \oplus B = B \oplus A \qquad
A \oplus 0 = A \qquad
A \oplus A = 0
$$

$$
(B \oplus A) \oplus A = B \oplus 0 = B
$$

   → Apply XOR between message & key, apply with key again to **decrypt**!

---

# One-time Pad (Vernam, 1916)

- Protects against **infinitely powerful adversaries**
- XOR between a message and a **same-length secret**
- **Bad news:** if you want to encrypt N bits of data, you need an N-bit secret key

---

# One-time Pad — worked example

<v-click>

**Message** `M = 'a'` = 01100001, **Key** `K` = 10100111 (random, same length)

</v-click>

<div class="flex justify-center items-start gap-1 font-mono text-2xl" style="margin-top: 1.5em;">
<span style="text-align: right; line-height: 1.9; padding-right: 0.5em;">
  M<br>⊕ K<br>───<br>= C
</span>

<v-click><div class="otp-col"><div>0</div><div>⊕</div><div>1</div><div>─</div><div>1</div></div></v-click>
<v-click><div class="otp-col"><div>1</div><div>⊕</div><div>0</div><div>─</div><div>1</div></div></v-click>
<v-click><div class="otp-col"><div>1</div><div>⊕</div><div>1</div><div>─</div><div>0</div></div></v-click>
<v-click><div class="otp-col"><div>0</div><div>⊕</div><div>0</div><div>─</div><div>0</div></div></v-click>
<v-click><div class="otp-col"><div>0</div><div>⊕</div><div>0</div><div>─</div><div>0</div></div></v-click>
<v-click><div class="otp-col"><div>0</div><div>⊕</div><div>1</div><div>─</div><div>1</div></div></v-click>
<v-click><div class="otp-col"><div>0</div><div>⊕</div><div>1</div><div>─</div><div>1</div></div></v-click>
<v-click><div class="otp-col"><div>1</div><div>⊕</div><div>1</div><div>─</div><div>0</div></div></v-click>

</div>
<v-click>

**Ciphertext** `C` = 11000110 — decrypt: `C ⊕ K` = 01100001 = `a` ✔

</v-click>
<style>
.otp-col {
  display: flex; flex-direction: column; align-items: center;
  line-height: 1.9; text-align: center; width: 1.6em;
}
</style>

<!--
One click per bit column: M row first, then key bit, then result bit.
Point out C ⊕ K = M — the key *is* the decryption.
-->

---
layout: two-cols
---

# Shannon's S-P network

<v-clicks>

- **Claude Shannon** — father of Information Theory (1949) [10]
- **Substitution** provides *'confusion'*
  - By building a complex binding between input and output
<!-- that each binary digit (bit) of the ciphertext should depend on several
parts of the key -->
- **Permutation** (transposition) provides *'diffusion'*
  - By moving bits, one single bit of plaintext should influence about half of output bits
<!-- if we change a single bit of the plaintext, then about half of the bits in
the ciphertext should change-->
- Encryption algorithms / functions **MUST be invertible**

</v-clicks>

::right::

<div v-click="2" class="flex flex-col items-center" style="text-align: center;">

![S-P Network](./images/substitution_permutation_network.svg)

[S-P Network](https://en.wikipedia.org/wiki/Substitution%E2%80%93permutation_network)

</div>
<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%;
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>


---
layout: two-cols
---

# From military to business

<br>

![Bombardier](./images/app_bombardier.png)

::right::

<br>
<br>

![ATM](./images/app_atm.png)

<style>
.slidev-layout.two-columns {
	img {
		display: inline; max-width: 90%;
	}
}
</style>

---

# Encryption schemes

- Two main families based on the **keys** used for encryption/decryption

<v-click>

- **Symmetric:**
  - Same key used for both encryption and decryption
  - Two variants: **Block** and **Stream**

</v-click>
<v-click>

- **Asymmetric:**
  - Different keys: **public** ≠ **private**
  - New feature unlocked: **digital signatures**!

</v-click>

---

# Encryption ideologies

**Public algorithms** — all details are in the public domain, known to everyone.

<v-click>

- **Kerckhoffs' principle** (Dutch cryptographer): a cryptosystem should be secure even if everything about the system, **except the key**, is public knowledge.
- Reformulated as **Shannon's maxim**: *"the enemy knows the system"* — one ought to design systems under the assumption that the enemy will immediately gain full familiarity with them.

</v-click>
<v-click>

**Proprietary algorithms** — details known only to the designers and users.

- ...security through obscurity.

</v-click>

---

# The Foundation of Crypto: Randomness

- Cryptography relies absolutely on unpredictability (for Keys, IVs, Nonces).
- **PRNG (Pseudo-Random Number Generator):** 
  - Functions like `rand()` in C or `Math.random()`.
  - Highly predictable if you know the seed (e.g., `time(NULL)`).
  - **NEVER USE THESE FOR CRYPTOGRAPHY.**
- **CSPRNG (Cryptographically Secure PRNG):**
  - Gathers actual entropy from OS hardware events (mouse movements, CPU interrupts).
  - Use `/dev/urandom` or `getrandom()` (Linux), `BCryptGenRandom` (Windows), or `crypto.getRandomValues()` (Web).

---
layout: section
---
# Symmetric ciphers

---

# Symmetric ciphers

<v-clicks>

- A symmetric cipher is built of:
  - A **'secret key'** (data exchanged 'in secret' by the two parties)
  - An encryption algorithm
  - A decryption algorithm

- The strength of a cipher is given by:
  - **Key size** (small keys can be exhaustively searched in a decent amount of time)
  - **Algorithm strength** (for example against statistical cryptanalysis)

- Two modes for symmetric encryption: **stream** and **block** 😕

</v-clicks>

---
class: text-center
---

# The cipher hierarchy

<br>

```mermaid
flowchart TD
  S([Symmetric]) --> St([Stream])
  A([Asymmetric])
  S --> B([Block])
  B --> ECB[ECB]
  B --> CBC[CBC]
  B --> CTR[CTR]

  style S fill:#dcfce7,stroke:#16a34a,stroke-width:2px
  style A fill:#dcfce7,stroke:#16a34a,stroke-width:2px
  style St fill:#fef9c3,stroke:#ca8a04
  style B fill:#fef9c3,stroke:#ca8a04
```

<!--
Same key vs key pair → stream (bit by bit) vs block (fixed-size chunks) → block needs a mode of operation.
-->

---

# Stream ciphers

<v-clicks>

- **Keystream** — an 'infinite' stream of bits generated from a key and a Nonce/IV (for key reuse)
- Operations (remember One-Time Pad?):
  - `keystream ⊕ message → ciphertext`
  - `ciphertext ⊕ keystream → original message`
- The keystream must be **deterministic**, yet difficult to predict (without the key)
- Popular algorithms:
  - **RC4** (deprecated / broken)
  - **Salsa20 / ChaCha** (used by WireGuard)

</v-clicks>

---
layout: two-cols
---

# Block ciphers: DES (and 3DES)

- Developed by **IBM** as **LUCIFER**, modified by the **NSA**
- LUCIFER used a **128-bit** key — reduced to **56 bits** for DES ☺
- Adopted in **1977** as the **Data Encryption Standard** — DES
- Key length too small (56 bit) ⇒ **brute-force-able**

*Built on the **Feistel network**.*

::right::

<div class="flex flex-col items-center" style="text-align: center;">

![Feistel Network](./images/feistel_cipher.png)

[Feistel Network](https://en.wikipedia.org/wiki/Feistel_cipher)

</div>
<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%;
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>

---
layout: two-cols
---

# Block ciphers: AES

<v-clicks>

- January **1997**: NIST announced a competition for the successor to DES
- October **2000**: NIST selected **Rijndael** (pronounced "Rhine doll") by Belgian cryptographers **Joan Daemen** & **Vincent Rijmen**
- **2003**: AES approved for use with Secret and Top Secret classified information of the U.S. government

- Parameters:
  * **Key length**: 2 variants, `128` or `256` bits
  * **Block size**: `128` bits (`16` bytes)
  * `10-14` S-P rounds ;) 

</v-clicks>

::right::

<div v-click="4" class="flex flex-col items-center" style="text-align: center;">

![AES Round Function](./images/aes_round_function.png)

[AES Round Function](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

</div>
<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%;
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>

---

# Block cipher modes

- Total data length ≫ block size! (e.g., **1 MByte** vs **128 bit**)
- How do we use one block cipher on a long message?

<v-click>

<div class="flex flex-col items-center gap-1 font-mono" style="margin: 1.2em 0;">
  <div class="bm-data">data (1 MByte)</div>
  <div style="color: #64748b;">↓ split into fixed-size blocks</div>
  <div class="flex justify-center items-center gap-2">
    <div class="bm-block">128bit</div>
    <div class="bm-block">128bit</div>
    <div class="bm-block">128bit</div>
    <div class="bm-block">128bit</div>
    <span class="bm-ellipsis">⋯</span>
  </div>
  <div style="color: #64748b;">each block ↓ ↓ ↓ one by one  </div>
  <div class="flex items-center gap-3">
    <div class="bm-key">enc. key<br>(256bit)</div>
    <div style="color: #64748b;">+</div>
    <div class="bm-cipher">encrypt()</div>
    <div style="color: #64748b;">=></div>
    <div class="bm-ciphertext">ciphertext</div>
  </div>
</div>

<style>
.bm-data {
  width: 65%; height: 1.7em; display: flex; align-items: center; justify-content: center;
  background: #dcfce7; border: 2px solid #16a34a; border-radius: 0.3em; color: #14532d;
}
.bm-block {
  width: 4.1em; height: 1.7em; display: flex; align-items: center; justify-content: center;
  background: #fef9c3; border: 2px solid #ca8a04; border-radius: 0.3em;
}
.bm-key {
  text-align: center;
  width: 7.7em; height: 2.55em; display: flex; align-items: center; justify-content: center;
  background: repeating-linear-gradient(45deg, #fef2f2, #fef2f2 0.5em, #fecaca 0.5em, #fecaca 1em);
  border: 2px solid #7f1d1d; border-radius: 0.3em; font-size: 0.77em;
  color: #7f1d1d;
}
.bm-cipher {
  width: 6em; height: 2.2em; display: flex; align-items: center; justify-content: center;
  background: #fce7f3; border: 2px solid #db2777; border-radius: 0.3em; font-weight: bold;
}
.bm-ciphertext {
  width: 6.8em; height: 2.2em; display: flex; align-items: center; justify-content: center;
  background: repeating-linear-gradient(45deg, #f1f5f9, #f1f5f9 0.5em, #e2e8f0 0.5em, #e2e8f0 1em);
  border: 2px dashed #475569; border-radius: 0.3em; color: #475569;
}
.bm-ellipsis { font-size: 1.5em; color: #64748b; }
</style>

</v-click>

<v-click>

- `Last block < block size`? => **padding**!

</v-click>


---

# Mode 1: Electronic Codebook (ECB)

- Each block encrypted **independently** ⇒ identical plaintexts encrypted similarly
- No chaining, no error propagation
- **Does not hide data patterns** — unsuitable for long messages!

<EcbDiagram width="660px" height="143px" />

---
layout: two-cols
---

# Why ECB is a bad idea

- **Electronic Codebook (ECB)** maps the exact same plaintext block to the exact same ciphertext block.
- While the data is completely encrypted, the **structural patterns** remain completely visible!
- This is why we need Initialization Vectors (IVs) and chaining modes (CBC, GCM).

::right::

<div class="flex flex-col items-center mt-4" style="text-align: center;">

<img src="https://upload.wikimedia.org/wikipedia/commons/5/56/Tux.jpg" class="h-40 mb-2" />
<em class="text-sm">Original Plaintext Image</em>

<img src="https://upload.wikimedia.org/wikipedia/commons/f/f0/Tux_ecb.jpg" class="h-40 mb-2" />
<em class="text-sm">Encrypted with AES-ECB</em>

</div>

<style>
.slidev-layout.two-columns { grid-template-columns: 55% 45%; }
</style>

---

# Mode 2: Cipher-Block Chaining (CBC)

- Chaining: ciphertext block cⱼ depends on xⱼ and all preceding plaintext blocks (dependency contained in cⱼ₋₁)
- Identical messages → different ciphertext
- Allows random access to ciphertext (decryption is still parallelizable)
- **Error propagation!**

<CbcDiagram width="800px" height="180px" />

---

# Mode 3: Cipher Feedback (CFB)

- Same Encryption algorithm used for Decryption 
- Identical messages: as in CBC
- Chaining: similar to CBC
- Errors: self-synchronizing

<CfbDiagram width="660px" height="179px" />

---

# Mode 4: Output Feedback (OFB)

- Preprocessing possible (keep enc/decrypting previous output block)
- No random access, not parallelizable
- Identical messages: same as CBC
- No chaining dependencies
- Error propagation: a single bit error on cⱼ may only affect the corresponding bit of xⱼ
- **IVs should not be reused!**

<OfbDiagram width="660px" height="159px" />

---

# Mode 5: Counter (CTR) / GCM

- Preprocessing possible
- Allows random access
- Both encryption & decryption are parallelizable
- Identical messages: changing the **nonce** results in different ciphertext
- No chaining dependencies, no error propagation
- **Nonce should be random**, and changed if a previously used key is reused

<CtrDiagram width="660px" height="159px" />

---

# Which mode for what task?

| Task | Mode |
| --- | --- |
| General file or packet encryption | **CBC** (input must be padded to a multiple of the cipher block size) |
| Resiliency / loss of ciphertext | **CFB** |
| Noisy line / no error propagation | **OFB** |
| High-speed data processing | **CTR / GCM** |
| Integrity check is required | **GCM** |

<!--
CBC requires padding to a multiple of the block size — common interview question.
-->

---
layout: section
---

# Asymmetric cryptography

---

# The problem

- **Symmetric key distribution** — how to do it securely?
- Can two parties agree on a **shared secret** without private communication?
  - [Ralph Merkle] (April 1975) *"Secure Communications Over Insecure Channel"*

---
layout: two-cols
---

# Diffie–Hellman (1976)

<v-clicks>

- One of the earliest **public-key protocols**
- Took Ralph Merkle's idea (Merkle's puzzle) and improved it so the attacker requires **exponential computations**
- Establish a secret between 2 (possibly unacquainted) parties!
- **Security:** discrete logarithm problem

</v-clicks>

::right::

<div v-click class="flex flex-col items-center" style="text-align: center;">

![Diffie-Hellman Paint Analogy](./images/diffie_helman.svg)
[Diffie-Hellman Paint
Analogy](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange)

</div>
<style>
.slidev-layout.two-columns {
	grid-template-columns: 65% 35%;
	.col-right img {
		display: inline; max-width: 85%;
	}
}
</style>

---

# Diffie–Hellman example

Common parameters (publicly shared):
  * $p = 23$ (prime); $g = 5$ ([primitive
  root](https://owlsmath.neocities.org/Primitive%20Root%20Calculator/calculator))

<br>

<v-clicks>

| Step | Value |
| --- | --- |
| Alice's private key: $a = 4$; sends public key → Bob: $A = g^a \mod{p} = 5^4 \mod{23}$ | **4** |
| Bob's private key: $b = 3$; sends public key → Alice: $B = g^b \mod{p} = 5^3 \mod{23}$ | **10** |
| Alice computes: $s = B^a \mod{p} = 10^4 \mod{23}$ | **18** |
| Bob computes: $s = A^b \mod{p} = 4^3 \mod{23}$ | **18** |

</v-clicks>

<v-click>

**Both now share the same secret key -- over a public channel.**

</v-click>

<!--
Walk through the example line by line; point out that p and g are public.
-->

---
layout: two-cols
---

# RSA (1977)

<v-click>

- **Ron Rivest, Adi Shamir, Leonard Adleman**
- **Key pair:**
  - Private key: p, q … ⇒ **decryption key**
  - Public key: n = p·q, e
- **Security:** factorization problem!

</v-click>
<v-click>

- **Primitives:**

```
c = encrypt(m, PubKey)
m = decrypt(c, PrivKey);

s = sign(m, PrivKey)
if (verify(s, PubKey)) ...
```

</v-click>

::right::

<v-click>

<br><br><br><br>

<div class="flex flex-col justify-center items-center gap-2">

$c \equiv m^e \pmod{n}$

$c^d \equiv (m^e)^d \equiv m \pmod{n}$

</div>

</v-click>

---

# RSA — worked example

Key Generation: Alice chooses primes p = 17, q = 11.

| Step | Value |
| --- | --- |
| Alice computes modulus **n** = p · q = 17 · 11 | **187** |
| Alice computes totient **φ(n)** = (p-1) · (q-1) = 16 · 10 | **160** |
| Alice chooses public key **e** (1 < e < 160, coprime to 160) | **7** |
| Alice computes private key **d** (e · d ≡ 1 mod 160) → 7 · 23 = 161 | **23** |
| Bob encrypts message **m = 88**: **c** = mᵉ mod n = 88⁷ mod 187 | **11** |
| Alice decrypts ciphertext **c = 11**: **m** = cᵈ mod n = 11²³ mod 187 | **88** |

**Alice's Public Key: (n=187, e=7) · Private Key: (d=23)**

<br>

<div class="text-sm bg-blue-50 p-4 rounded text-black border-l-4 border-blue-500">
💡 <b>Verify the Math!</b> Open <a href="https://owlsmath.neocities.org/dynamic?Calculators|type|tool" target="_blank">Owls Math Calculators</a>:
<ul class="mt-2 mb-0">
<li><b>Euler's Totient Calculator:</b> Enter <code>187</code> to automatically compute φ(n) = 160.</li>
<li><b>Prime Factor Calculator:</b> Play the attacker! Enter the public modulus <code>187</code> to instantly extract the secret primes <code>17</code> and <code>11</code>.</li>
</ul>
</div>

<!--
PRESENTER NOTES / DEMO:
- The private key trick: "Look at step 4. 7 * 23 = 161. What is 161 modulo 160? It's 1. That's all a private key is." This perfectly demystifies the trapdoor math without needing to put the Extended Euclidean Algorithm on screen.
- Emphasize the core vulnerability of RSA using the tool: If an attacker intercepts the public key (n=187), they can break the encryption *if* they can factor it. 
- You can also mention that Owls Math has a "Primitive Root Calculator" which is exactly how 'g' is chosen for the Diffie-Hellman parameters from the previous slide!
-->

---

# The UK version

- **James H. Ellis** — idea of non-secret encryption in **1970** (5 years before Merkle)
- **Clifford Cocks** — equivalent of RSA in **1973** (3 years before RSA)
- **Malcolm J. Williamson** — equivalent of DH in **1974** (2 years before DH)

- [yep, no profit!]
- **GCHQ** decided to keep the discoveries secret till **1998**

---

# The Real World: Hybrid Cryptography

- **Asymmetric crypto** (RSA/ECC) solves the key exchange problem, but is incredibly slow and computationally heavy.
- **Symmetric crypto** (AES) is incredibly fast, but has the key distribution problem.
- **Solution: Combine them! (How TLS/HTTPS works):**
  1. **Handshake (Asymmetric):** Alice and Bob use RSA or ECDH to safely exchange a temporary "Session Key" over the public internet.
  2. **Bulk Data (Symmetric):** Alice and Bob use the shared Session Key with AES-GCM to encrypt the actual multi-gigabyte data stream.

---

# Elliptic Curve Cryptography

- Another approach to asymmetric encryption
- Elliptic curves over finite fields

   $y^2 = x^3 + ax + b$

- **Smaller numbers for equivalent security** (e.g., **384 vs 4096 bits**)
- Same domain parameters (e.g., $p, a, b, G, n, h$) ⇒ **standard curves** (e.g., NIST)!
- Algorithms: **ECDH**, **ECIES**, **ECDSA**, **EdDSA**, etc.

---
layout: section
---

# Hashing, integrity & attacks

---

# Message digest functions (hashing)

- **One-way functions** providing data 'summarization'

  * E.g., `5eb63bbbe01eeed093cb22bb8f5acdc3`
 
- Message **integrity**, **key derivation**
- Collisions exist but should be **hard to find**
- Popular algorithms:
  - **MD5** (broken): 1991, 128 bits
  - **SHA-1** family (1995): 160 bits (Broken / Deprecated — SHAttered 2017)
  - **SHA-2** family (2001), **SHA-3** (2015): 256–512 bits

---

# Practical integrity

- Hashing alone is not enough — an attacker can simply change both the message **and** the hash
- **MAC** (message authentication code) uses a **secret key** together with the function:
  - **HMAC** — function is hashing
  - **CBC-MAC** — function is CBC encryption mode
- **Asymmetric signature:** RSA, DSA, ECDSA, etc.

---

# Authenticated Encryption (AEAD)

- **AEAD (Authenticated Encryption with Associated Data)**
- In the past, developers manually combined Encryption (CBC) with a MAC (HMAC). This was error-prone and led to devastating bugs (e.g., Padding Oracle Attacks).
- AEAD modes provide **Confidentiality AND Integrity** simultaneously in a single, safe API call.
- *Rule of thumb for modern software engineers:* Never build your own crypto puzzle. Use standard AEADs.
  - **AES-GCM** (Standard for TLS, Wi-Fi WPA3)
  - **ChaCha20-Poly1305** (Standard for WireGuard)

---

# Passive vs. active attacks

**Passive attacks**

- No communication with victim
- Stealing of private data without the victim knowing

**Active attacks**

- Involves changing data with the victim
- Unauthorized data access in order to modify / delete / alter it

---

# Types of attacks (1)

- **Ciphertext Only Attack (COA)** — attacker has ciphertext(s), not the plaintext; successful when the plaintext can be determined from the ciphertext
- **Known Plaintext Attack (KPA)** — attacker knows plaintext for parts of the ciphertext; task: decrypt the rest (typically by finding the key)
- **Chosen Plaintext Attack (CPA)** — attacker gets text of his choice encrypted; simplifies finding the encryption key
- **Chosen Ciphertext Attack (CCA)** — attacker obtains decryptions of chosen ciphertexts; can attempt to recover the decryption key

---

# Types of attacks (2)

- **Dictionary Attack** — attacker builds a dictionary of ciphertexts and corresponding plaintexts over time; later looks up the plaintext
- **Brute Force Attack (BFA)** — try all possible keys
- **Man in Middle Attack (MIM)** — targets public-key cryptosystems with key exchange before communication
- **Side Channel Attack (SCA)** — exploits weaknesses in the **physical implementation**
- **Timing/Power Analysis Attacks** — different computations take different times on a processor

---

# Practicality of attacks

- Often **highly academic**
- Weaker versions used (e.g., AES with fewer rounds)
- Unrealistic assumptions:
  - In chosen-ciphertext attacks, the attacker requires an impractical number of deliberately chosen ciphertexts

---
layout: section
---

# Beyond classical crypto

---

# Post-quantum cryptography

- **GNFS** (_General number field sieve_) — fastest known (classical) algorithm to factor a number on a binary processor (time depends on b bits).
  Complexity:

  $$O(\exp\!\left(\left(\sqrt[3]{\tfrac{64}{9}} + o(1)\right) \cdot (\log N)^{1/3} \cdot (\log\log N)^{2/3}\right))$$


- **Shor's algorithm** (Peter Shor) — computes a prime factorization on a **quantum computer**, much number
  
  $$O\!\left((\log N)^{3}\,(\log\log N)^{2}\right)$$

  → Shor's algorithm breaks factorization-based crypto (RSA!). We need new assumptions.


--- 

# Identity / Attribute based encryption

- **Hierarchical Identity-Based Encryption**
  * Derive an unlimited **tree** of child keys, e.g. `org → team → user`
  * **Root** holds one master secret key and can decrypt anything below!
  * A child key decrypts only ciphertexts addressed to its **subtree**

- **Attribute-Based Encryption**
  * **Authority** holds a master key
  * Issues private keys bound to **attribute sets**

     e.g. `role = engineer ∧ clearance ≥ 3 ∧ dept = R&D`

  * Either _ciphertexts_ or _keys_ carry an **access policy**!

---

# Homomorphic encryption

- Allows **computations on encrypted data**
- Not many operations are supported
- Mostly **addition and multiplication**
- In **2020**, there was a solution for **encrypted machine learning**

---
layout: two-cols
---

# Resources

- [1] [History of cryptography — Wikipedia](https://en.wikipedia.org/wiki/History_of_cryptography) 
- [2] [Attacks on cryptosystems — TutorialsPoint](https://www.tutorialspoint.com/cryptography/attacks_on_cryptosystems.htm)
- [3] [Caesar cipher — Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [4] [DES history](http://www.umsl.edu/~siegelj/information_theory/projects/des.netau.net/des%20history.html)
- [5] [Modes of operation](http://www.utdallas.edu/~muratk/courses/crypto07_files/modes.pdf)
- [6] [Modes of block ciphers](http://www.crypto-it.net/eng/theory/modes-of-block-ciphers.html)
- [7] [History of encryption — SANS](https://www.sans.org/reading-room/whitepapers/vpns/history-encryption-730)

::right::

<br><br>

- [8] [Encryption research review](http://www.eng.utah.edu/~nmcdonal/Tutorials/EncryptionResearchReview.pdf)
- [9] *Indistinguishability Obfuscation from Well-Founded Assumptions* — Jain, Lin, Sahai
- [10] *Communication Theory of Secrecy Systems* — C. E. Shannon [PDF](https://www.cs.virginia.edu/~evans/greatworks/shannon1949.pdf)
- [11] [The Atlantic — history of encryption](https://www.theatlantic.com/technology/archive/2016/01/the-long-and-winding-history-of-encryption/423726/)
- [12] [Atbash code](https://www.gotquestions.org/Atbash-code.html)
- [13] [Transposition ciphers](http://cochranmath.pbworks.com/w/page/118045167/Transposition%20Ciphers)

---
class: text-center
---

# Thank you

**Further reading:**
*Communication Theory of Secrecy Systems* — Claude E. Shannon (1949)

[cs.virginia.edu/~evans/greatworks/shannon1949.pdf](https://www.cs.virginia.edu/~evans/greatworks/shannon1949.pdf)
