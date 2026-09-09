## [Introduction to Computer Security Lecture Slides](https://ocw.cs.pub.ro/courses/isc)

© 2024 by Mihai Chiroiu &amp; Florin Stancu

is licensed under Attribution-NonCommercial-ShareAlike 4.0 International

<!-- image -->

## Authentication and key establishment

<!-- image -->

## Who do we authenticate

## · Users:

- The human operator
- Authentication is typically slow
- Local or over-the-wire
- Authentication only
- human brain cannot do proper cryptography just yet :((

## · Principals

- User's digital identity
- Authentication should be fast and scalable
- Mostly over-the-wire
- Goal: Authentication &amp; key establishment

<!-- image -->

<!-- image -->

## AAA framework

- Identify
- Map a real-person/subject to a virtual account
- Authenticate
- Request a proof from the account
- Authorize
- Verify if the account can access a resource
- Accounting
- Log/monitor what the account is doing

<!-- image -->

## Identification vs authentication

- Identification means one-from-many
- Find your fingerprints in a police database
- Authentication means one-to-one relations
- Compare your (based on the username) input to a previously saved one
- Enrollment (can be slow, must be precise) vs Recognition (must be quick)
- Cooperation
- In identification, the user does not cooperate
- In authentication, the user is cooperative

<!-- image -->

## Just authentication?

- Is authentication alone enough?
- Yes, for local systems (e.g., console/GUI login)
- Not very good for remote systems (e.g. telnet) -&gt; session hijack
- Key establishment only?
- For anonymity purposes
- Not very practical (e.g. plain D-H over MitM channel)
- Usually: we do both!

<!-- image -->

## Attacks?

| Attack         | Short description                                                    |
|----------------|----------------------------------------------------------------------|
| replay         | reusing a previously captured message in a later protocol run        |
| reflection     | replaying a captured message to the originating party                |
| relay          | forwarding a message in real time from a distinct protocol run       |
| interleaving   | weaving together messages from distinct concurrent protocols         |
| middle-person  | eavesdropping on communication                                       |
| bruteforce     | usable for short credentials (e.g., PIN codes without rate limiting) |
| dictionary     | using a heuristically prioritized list in a guessing attack          |
| forward search | feeding guesses into a one-way function, seeking output matches      |
| pre-capture    | extracting client OTPs by social engineering, for later use          |

<!-- image -->

## Authentication

<!-- image -->

## The concept

- The authenticator (e.g. server, website) asks to prove that you are who you pretend to be based on one or more pieces of evidence called factors .
- May also be mutual: server also authenticates to the client!
- The  evidence  can  be  presented  either  directly  (e.g.  password authentication) or indirectly by using it in cryptographic calculation (e.g. challenge authentication protocol).
- Indirect proof use some form of cryptographic algorithms.
- Indirect proof also known as implicit authentication.

<!-- image -->

## Types of factors

- Something you know (Knowledge Factor)
- Something you have (Possession Factor)
- Something you are (Inherence Factor)
- Other authentication attributes that can be used:
- Somewhere you are
- Someone you know

<!-- image -->

## Chaining factors

- N-factor authentication
- Factors should be different
- N-step verification
- Can be same factor

<!-- image -->

[https://rublon.com/blog/2fa-2sv-difference/](https://rublon.com/blog/2fa-2sv-difference/)

<!-- image -->

## Something you know - Passwords

- Require people to remember them
- Used on multiple occasions
- Shoulder surfing / key logging
- Can be enhanced through policies
- E.g. Minimum 20 characters

## 44 million Microsoft users reused passwords in the first three months of 2019

Microsoft used a database of three billion publicly leaked credentials to identify users who reused passwords.

<!-- image -->

## Something you know - Passwords

<!-- image -->

[https://nordpass.com/most-common-passwords-list/](https://nordpass.com/most-common-passwords-list/)

<!-- image -->

## Something you know - Passwords

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

THROUGH 20 YEARS OF EFFORT, WE'VE SUCCESSFULLY TRAINED EVERYONE TO USE PASSWORDS THAT ARE HARD FOR HUMANS TO REMEMBER, BUT EASY FOR COMPUTERS TO GUESS.

[https://xkcd.com/936/](https://xkcd.com/936/)

<!-- image -->

## Something you have

- Phone number / email
- Public / private key
- Symmetric key

<!-- image -->

Best: On a hardware token ( write+execute-only private keys)

<!-- image -->

## Something you are

- Fingerprint
- Facial recognition
- Speech recognition
- Odour recognition
- Gait

<!-- image -->

## Biometric properties

- Not 100% accurate
- Because of sensors
- Because of changes in biometrics
- Not 100% applicable
- E.g. Fingerprints w/o hands
- Typically hard to profile, easy to collect/verify
- E.g. Scanning of face multiple times to enable FaceID on Apple

<!-- image -->

## Storing factors

<!-- image -->

## Storing passwords

- Plain text - just don't
- Hash(Password)
- Hash(Salt + Password)
- Hash(Salt + Password + Pepper)

<!-- image -->

## Attacks on stored passwords

- Offline
- Brute Force
- Dictionary (better: crunch wordlists)
- Online
- Rate-limit
- Lock out after N failed attempts
- Some cryptographic hardware devices are 'online'!

<!-- image -->

## Storing keys

- Which factor is a random key?
- Storage: software vs hardware
- Software-protected memory / files
- chmod 600
- E.g.: SSH keys, WebAuthn 'passkeys';
- Weakest something you have factor!
- Hardware Security Tokens / Trusted Platform Module
- Key becomes a stronger something you have !
- Requires online attacks =&gt; rate limiting, auto-wipe after 10 failures etc.!

<!-- image -->

## Password managers

- One ring to rule them all
- Master key can be derived from password
- Use multiple factors (e.g., tokens)!
- Database storage: local or cloud
- Encourage different password per service: password generators, integration with browsers
- Back it up / don't forget/lose the keys!

<!-- image -->

<!-- image -->

## Password-based key derivation

- Problem: passwords have arbitrary lengths
- Cryptographic algorithms require keys of specific lengths!
- E.g., AES-256 requires 256-bits key =&gt; 32 bytes
- Solution: Key Derivation Functions (KDF):
- DerivedKey = KDF(password, salt, iterations)
- Algorithms: PBKDF2, Argon2
- E.g., per-domain derived passwords: http://spectre.app

<!-- image -->

## FIDO2 / passkeys

- Previously: U2F: Universal Second Factor
- FIDO2 WebAuthn =&gt; asymmetric crypto!
- Give a unique public key to the web server (no reuse!)
- Use private key instead of password
- Private key must be stored on secure hardware!
- FIDO-certified security keys: Yubikey, SoloKey, NitroKey ;)
- Hardware validates 2nd factor:
- Something you know (PIN - rate limited!)
- Something you are (fingerprint, FaceID etc.)
- Must always enroll backup keys!

<!-- image -->

## OATH One Time Pass standards

- OATH: HOTP &amp; TOTP

- TOTP: RFC6238

- TOTP = HOTP(K, T)

- Time: divided/rounded by expiry time, e.g., T = unix\_timestamp / 60

- Private key shared between user and auth server

<!-- image -->

<!-- image -->

## Key establishment protocols

<!-- image -->

## Authentication protocols

- Symmetric (shared secret)
- How to ask for a known secret over insecure channels?
- Hash the password?
- Challenge-Response
- Asymmetric protocols
- Diffie-Hellman!
- Forward Secrecy

<!-- image -->

## Burrows-Abadi-Needham logic (notation)

- ID A ,ID B , ID S
- An unique identifier for A, B and S (Trusted Server)
- k A,B
- A key shared between A and B
- {ID A } K A
- Encryption/signature of ID A under the key of A
- A -&gt; B : {ID A } k A,B
- A send to B the message ID A encrypted by the shared key of A and B

<!-- image -->

## Plain Diffie-Hellman

## Classic MitM attack:

1. A -&gt; B : DH\_A (g a mod p) 2. B -&gt; A : DH\_B, {ID B } K A,B (both obtain the same K A,B ) 1. A -&gt; B: {ID A } K A,B

```
1. A -> T : DH_A 2. T -> B : DH_ T 3. B -> T : DH_B, {ID B } K T ,B 4. T -> B : {ID A } K T ,B 5. T -> A : DH_ T , {ID B } K A, T … etc
```

<!-- image -->

## Protocol for asymmetric encryption (STS simplified)

1. A -&gt; B : DH\_A
2. B -&gt; A : DH\_B, { {DH\_A, DH\_B} pub A } K A,B
3. A -&gt; B: { {DH\_A, DH\_B} pub B } K A,B
- We assume each party has private/public keys
- Public key being know to all entities
- The problem is how to distribute public keys
- Public Key Infrastructure
- Pretty Good Privacy

<!-- image -->

## Symmetric authentication

- Given A and B who trust S, A and B should be able to create a shared key k A,B for secret communication
- k A,B should be know only to A and B (and possibly to S)
- A and B should know that k A,B is newly generated
- A and B should authenticate each other
- Why? Enterprise authentication!

<!-- image -->

## Protocol for symmetric encryption (1)

## Protocol steps

1. A -&gt; S : ID A , ID B I am A, give me key for B
1. S -&gt; A : k A,B (key get transferred in unencrypted form)
1. A -&gt; B : ID A , k A,B (key get transferred in unencrypted form)

<!-- image -->

## Possible attacks

- An attacker with MITM capabilities gets k A,B

## Protocol for symmetric encryption (2)

## Protocol steps

1. A -&gt; S : ID A , ID B I am A, give me key for B
1. S -&gt; A : {k A,B } k A,S ,{k A,B } k B,S (key encrypted with common secret between A,S)

## Possible attacks (1)

1. A -&gt; S : ID A , ID B
2. S -&gt; A : {k A,B } k A,S ,{k A,B } k B,S
3. A -&gt; T : ID A ,{k A,B } k B,S
4. T -&gt; B: ID T ,{k A,B } k B,S
1. A -&gt; B : ID A ,{k A,B } k B,S (key also encrypted with common B,S secret)

(Trudy replaces the identity A presented to B!)

<!-- image -->

## Protocol for symmetric encryption (2)

## Protocol steps

1. A -&gt; S : ID A , ID B

<!-- formula-not-decoded -->

3. A -&gt; B : ID A ,{k A,B } k B,S

## Possible attacks (2)

1. A -&gt; T : ID A , ID B
2. T -&gt; S : ID A , ID T

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

Trudy in the middle …

<!-- image -->

## Protocol for symmetric encryption (3)

## Protocol steps

1. A -&gt; S : ID A , ID B
2. S -&gt; A : {k A,B ,ID B } k A,S ,{k A,B , ID A } k B,S
3. A -&gt; B : {k A,B , ID A } k B,S

## Possible attacks

Replay of old broken key

1. A -&gt; T : ID A , ID B
2. T -&gt; A : {k' A,B , ID B } k A,S ,{k' A,B , ID A } k B,S
3. A -&gt; B : ID A ,{k A,B , ID A } k B,S

<!-- image -->

## Protocol (4) - Needham-Schroeder (1978)

## Protocol steps

1. A -&gt; S : ID A , ID B , Nonce A
2. S -&gt; A : {k A,B , ID B , N A , {k A,B , ID A } k B,S } k A,S
3. A -&gt; B : {k A,B , ID A } k B,S
4. B -&gt; A : {N B } k A,B
5. A -&gt; B : {N B -1} k A,B

## Possible attacks - Denning Sacco

Replay of old broken key

1. T -&gt; B : { k' A,B , ID A } k B,S
2. B -&gt; T : {N B } k' A,B
3. T -&gt; B : {N B -1} k' A,B

<!-- image -->

## Protocol for symmetric encryption (5)

## Protocol steps

1. B -&gt; A : ID B , N B
2. A -&gt; S : ID A , ID B , N A , N B

<!-- formula-not-decoded -->

,

<!-- formula-not-decoded -->

<!-- formula-not-decoded -->

<!-- image -->

## Possible attacks

- None of the above

## Notes on protocols - Abadi and Needham [2]

- If the identity of a principal is essential to the meaning of a message, it is prudent to mention the principal's name explicitly in the message.
- Be clear about why encryption is being done.
- When a principal signs material that has already been encrypted, it should not be inferred that the principal knows the content of the message.
- Be clear about what properties you are assuming about nonces.
- If timestamps are used as freshness guarantees, then the difference between local clocks at various machines must be much less than the allowable age of a message.

<!-- image -->

## Digital Identity

## European Digital Identity

PAGE CONTENTS

## Digital Identity for all Europeans

Digital Identity for all Europeans

Benefits of the European Digital Identity

Why is it needed?

Key principles

Practical use

Making things easier for citizens and businesses

Documents The European Digital Identity will be available to EU citizens, residents, and businesses who want to identify themselves or provide confirmation of certain personal information. It can be used for both online and offline public and private services across the EU.

<!-- image -->

Every EU citizen and resident in the Union will be able to use a personal digital wallet.

<!-- image -->

"Every time an App or website asks us to create a new digital identity or to easily log on via a big platform, we have no idea what happens to our data in reality. That is why the Commission will propose a secure European e-identity. One that we trust and that any citizen can use anywhere in Europe to do anything from paying your taxes to renting a bicycle. A technology where we can control ourselves what data is used and how.

Ursula von der Leyen, President of the European Commission, in her State of the Unionaddress,16September 2020

<!-- image -->

<!-- image -->

<!-- image -->

## NIST く

## Digital Identity Guidelines

The four-volume SP 800-63 Digital Identity Guidelines document suite is available in both PDF format and online.

PDF versions of the documents are available from:

| Document    | Title                                   | URL                                      |
|-------------|-----------------------------------------|------------------------------------------|
| SP 800-63-3 | Digital Identity Guidelines             | https://doi.org/10.6028/NIST.SP.800-63-3 |
| SP 800-63A  | Enrollment and Identity Proofing        | https://doi.org/10.6028/NIST.SP.800-63a  |
| SP 800-63B  | Authentication and Lifecycle Management | https://doi.org/10.6028/NIST.SP.800-63b  |
| SP 800-63C  | Federation and Assertions               | https://doi.org/10.6028/NIST.SP.800-63c  |

Links to the online version of the SP 800-63 suite are below.

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

Federation &amp; Assertions

## Single Sign-On (SSO)

- Password managers
- Enterprise level SSO
- Same-domain authentication
- Kerberos, RADIUS with LDAP / Active Directory databases
- Federated Identity
- Cross-domain authentication
- Based on assertions containing the result of authentication
- Factors cannot be shared between domains
- RADIUS, OpenID Connect, SAML etc.

<!-- image -->

## Kerberos

- Developed by MIT in 1983
- Was banned for export till 2000 by US
- Used for key establishment between multiple entities
- The Kerberos server is trusted by all entities
- Assumes existing pre-shared keys between entities and Kerberos server
- Can be adapted to multiple symmetric encryption algorithms
- Kerberos v5 uses AES

<!-- image -->

## Kerberos

- The adversary can compromise the network, not the host (e.g. secrets, keys)
- Based on fixed Needham-Schroeder protocol
- Uses tickets to create a legitimate session key

<!-- image -->

## Kerberos (v1)

1. A -&gt; KAS : ID A , ID B , N A · KAS = Kerberos Authentication Server
2. KAS -&gt; A : {k A,B , ID B , T KAS , N A } k A,KAS ,  {k A,B , ID A , T s } k B,KAS · T s = Timestamp server
3. A -&gt; B : {k A,B , ID A , T KAS } k B,KAS , {ID A , T A } k A,B
- k A,B : session key between A and B
- {k A,B , ID A , T KAS } k B,KAS : ticket for A to used when contacting B
- T a &gt; T KAS : B needs to validate time window by comparing T a and T KAS

<!-- image -->

## Kerberos (v2)

- Usually the shared key between A and KAS is deducted from a user input/password
- The previous version of the protocol requires credentials input every connection to a new application server (B)
- Ticket granting separate from user authentication
- User authenticates using passwords with KAS and receives session key for Ticket Granting Service
- Entities use session key to require tickets for multiple applications

<!-- image -->

## SAML

<!-- image -->

<!-- image -->

## RADIUS / EAP

<!-- image -->

<!-- image -->

## References

- [1]  'Protocols for Authentication and Key Establishment', Colin Boyd, Anish Mathuria, Douglas Stebila, 2020
- [2] Abadi, M., Needham, R.: Prudent engineering practice for cryptographic  protocols.  In:  IEEE  Symposium  on  Research  in  Security and Privacy, pp. 122-136. IEEE Computer Society Press (1994)
- [3] Computer Security and the Internet: Tools and Jewels, Paul C. van Oorschot. Springer, 2021.

[https://people.scs.carleton.ca/~paulv/toolsjewels.html](https://people.scs.carleton.ca/~paulv/toolsjewels.html)

<!-- image -->