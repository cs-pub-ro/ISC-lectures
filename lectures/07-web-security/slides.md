---
download: 'slides.pdf'
theme: default
colorSchema: light
title: Lecture 7 — Web Security
info: |
  ## ISC — Lecture 7 · Web Security
  [ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
transition: slide-left
---

# Web Security

<font size=4>HTTP security, injections, and the browser as an attack surface</font>

<div class="mt-12 py-1" @click="$slidev.nav.next" hover:bg="white op-10">
  Press Space for next slide
</div>

<!--
© 2024 by Mihai Chiroiu & Florin Stancu, CC BY-NC-SA 4.0. Based on the ISC course slides.
-->

---

# Contents

<v-clicks>

1. HTTP Security
2. Cookies, Sessions
3. HTTPS
4. Server-side Security
5. Injection
6. Session Hijacking
7. Client-side / Browser Security

</v-clicks>

---
layout: section
---

# HTTP Security

---

# HTTP Protocol

- **Stateless**, text-based request–response protocol [1]

**Client → Server:**

```http
GET /index.html HTTP/1.0

Header1: value1
Header2: value2

<optional body>
```

**Server → Client:**

```http
HTTP/1.0 200 OK
Header1: value1
Header2: value2

<html><head>...</head>
<body>...</body></html>
```

---

# HTTP Methods

- **GET** — fetch a resource, may have query strings, e.g.:
  - `http://domain.com/browse.php?list=users&name=john` → request line:
    `GET /browse.php?list=users&name=john HTTP/1.0`
- **PUT / POST** — create or edit a resource (only POST is widely used)
- **DELETE** — delete resources (not used in practice)
- **HEAD** — like GET, but server responds with headers only
- **OPTIONS** — determine options for a resource
- **GET, HEAD and OPTIONS should be idempotent**

<!--
Note that query strings are visible in URLs, logs, and referrer headers — GET leaks data.
-->

---

# HTTP Methods & HTML Forms

- Links typically use a **GET** request for opening pages
- HTML forms can generate GET and POST requests:

```html
<form action="/login.php?user_type=regular" method="post">
  User: <input type="text" name="username">
  Password: <input type="password" name="pass">
</form>
```

```http
POST /login.php?user_type=regular HTTP/1.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 30

username=<username>&pass=<user's password>
```

<!--
Even with POST, the user_type parameter stays in the URL; the body carries the fields.
-->

---
layout: section
---

# Cookies, Sessions

---

# Cookies

- Small piece of data that the **browser** stores and sends back to the **server** on future requests
- Can be used to remember user preferences, server sessions, etc.

**Response header example:**

```http
HTTP/1.0 200 OK
Set-Cookie: c1=val1; flags
Set-Cookie: c2=val2; flags
```

**Request example:**

```http
GET / HTTP/1.1
Cookie: cook1=val1;cook2=val2
```

---

# Cookie Security

**Cookies are insecure:**

- The user can freely **read & modify** them
- They can be **intercepted** unless HTTPS is used for transport

**Must add confidentiality and integrity guarantees:**

- Using cryptography: **encryption & HMAC** [2]
- **Server-side sessions**

**Privacy implications:**

- Cookies can be used to **track users** (e.g. by analytics & ad servers)

---

# Server Sessions

- Also known as **server-side cookies**
- Server generates a **random, unique session ID**:

```
4125a859778b1bf9b9b778a236f01e01
```

- Server uses a **database** to store secrets associated with a session ID
- Persisted as a **cookie** / passed using **GET / POST** parameters:
  - `Cookie: PHPSESSID=4125a85...`
  - `show.php?phpsessid=4125a85...`

<!--
Moving secrets server-side means the client only holds an opaque token.
-->

---
layout: section
---

# HTTPS

---

# HTTPS [3]

- Based on **Secure Sockets Layer / Transport Layer Security**
- Creates a **private channel** between the client and the server
- The **server authenticates itself** using **certificates and PKI**
- **Diffie–Hellman** for forward secrecy
- **Cipher negotiation:** RC4, DES, AES-CBC, AES-GCM, etc.
- **Target of numerous attacks**

---

# TLS / HTTPS Attacks [4]

**Compression attacks** (CRIME, BREACH — 2013) — Compression Length Oracle

**Crypto weaknesses:**

- RC4 — broken · 3DES — Sweet32 · RSA — ROBOT
- **ROBOT:** Return Of Bleichenbacher's Oracle Threat (2018)
- **Lucky13:** timing padding oracle in CBC-mode

**Man-in-the-middle:** malicious certificates, SSL stripping

**Downgrade attacks:** FREAK, Logjam, POODLE (2014)

**Implementation bugs:**

- **Heartbleed** (CVE-2014-0160)
- Cloudflare parser bug (2017)

<!--
Every one of these was a deployed crypto system failing in practice — protocols rot.
-->

---

# TLS Testing Services

**Servers:**

[immuniweb.com/ssl](https://www.immuniweb.com/ssl/)

**For both clients / servers:**

[ssllabs.com/ssltest](https://www.ssllabs.com/ssltest/)

---
layout: section
---

# Server-side Security

---

# Server-side Processing

- Server generates **dynamic content**
- Scripting interfaces: **CGI** (legacy) / **FastCGI** / integrated modules [5]

**Sample directory layout — `/var/www`:**

```
|-- index.html
|-- login.php
|-- css/style.css
|-- images/
|-- logo.png
|-- map.png
```

**Example requests:**

```
> GET /index.html HTTP/1.0
> GET /images/logo.png HTTP/1.0
> POST /login.php HTTP/1.0
```

---

# Server-side Processing — Example (PHP)

```php
<?php
    $name = $_GET["name"];
    $curDate = date("l");
?>
<p>Hello, <i><?=$name?></i>. The date is <b><?=$curDate?></b></p>
<?php echo $message; ?>
```

**Example (Python / Flask):**

```python
@app.route("/")
def index():
    cur_date = datetime.now().strftime("%d.%m.%Y")
    return f"Hello, {request.args.get('name')}<br /> Date is {cur_date}!"
```

<!--
Note how user input flows straight into the response — the seed of injection issues.
-->

---

# SQL Intro

**Querying:**

```php
$query = "SELECT * FROM employees WHERE name LIKE 'florin%'";
$result = mysql_query($conn, $query);
```

**Modification queries:**

```sql
INSERT INTO employees (name, emp_date, status) VALUES
    ('Florin S.', '2023-10-01 08:00', 'active');

UPDATE employees SET status='terminated' WHERE id=2;
```

---
layout: section
---

# Injection

---

# SQL Injection (1)

**Code:**

```php
$query = "SELECT * FROM users WHERE user = '" .
    $_POST["user"] . "' AND password='" .
    hash($_POST["password"]) . "'";
$result = mysql_query($conn, $query);
```

**What if user input is `admin' -- comment`?**

```sql
SELECT * FROM users
WHERE user = 'admin' -- comment
' AND password=''
^<- injected input ->^
```

<!--
The comment kills the password check entirely — login as admin without a password.
-->

---

# SQL Injection (2)

**This doesn't work very often:**

```sql
SELECT * FROM users
WHERE user=''; DROP DATABASE app -- commented'
^<- user-injected input ->^
```

- SQL servers' standard `query()` functions only execute **one single statement**!
- There are `multi_query()`-like functions, but they're **seldom used**!

---

# SQL Injection (3)

**Error Reporting Abuse:**

```sql
SELECT * FROM users WHERE user =
'asdf' OR 1/(select password from users) --'
```

**Boolean statements:**

```sql
SELECT * FROM users WHERE user='' OR user LIKE '%admin%'
```

**Time-based attacks:**

```sql
SELECT * FROM users WHERE user='' OR
IF(user LIKE '%adm%'), SLEEP(10), 'false')'
```

<!--
Boolean/time-based: exfiltrate data bit by bit without touching the normal code path.
-->

---

# Code Injection (File Upload)

- A site allows image submissions with **minimal verification**
- The hacker uploads `image.gif.php` with malicious code
- Find out the path to the image and request it:

```
GET /uploads/image_9876.gif.php
```

- Server executes our script (if badly configured)!
- **Remote Code Execution** :(

---

# Code Injection (2)

**Multipart file upload with path traversal bug:**

```
Content-Disposition: form-data; name="../../index.php"

<?php die('PWNED')
```

- Uploader overwrites `index.php` via a `../` in the filename
- A real-world listing (from the notes) shows such uploads alongside normal site files

---

# Preventing Injection

- **Do not trust tutorials / ChatGPT** [7]
- **Always sanitize user input!**
- Try not to use `exec()` / `eval()`
- For SQL, use **prepared statements**:

```php
$stmt = $mysqli->prepare("INSERT INTO table (name) VALUES (?)");
$stmt->bind_param("s", $id); // "s" for string
$stmt->execute();
```

---

# Application-Specific Vectors

**Broken authentication systems** [8]:

- Predictable / insecure session IDs
- Unencrypted passwords [9]

**Authorization vulnerabilities:**

- Improper access verification
  - Example: `/delete_user.php?id=5368`
- Direct object reference: `/admin/list_users.php`

**Vulnerable frameworks / plugins** (e.g. WordPress)

<!--
delete_user.php?id=5368: anyone who guesses/knows an ID can act on it.
-->

---

# Server Misconfiguration [9]

- Again: **do not trust tutorials & ChatGPT**
- **Nginx & PHP FastCGI** configuration vulnerability [10]
- **Exposed files** (e.g. password files, backups) / directory listings
- **Bad permissions**
- **Debugging enabled in production**
- **System software vulnerabilities:**
  - e.g. **ShellShock** (BASH vulnerability) [11]

---

# Pwned Websites

- [**Haveibeenpwned.com**](https://haveibeenpwned.com) — account breach checker
- **Yahoo!** (2012 — SQL injection, 2013, 2014 — forged cookies)
  - **3 billion accounts exposed!**
- **LinkedIn** — hacked 2012, exposed 2016, 2021 Dark Web DB sale
- **Adobe** (2013, 2019): broken encryption :|
- **Dropbox** (2012): SHA1 and salted passwords ;)

**The 2013 Adobe breach:** 153M emails, encrypted passwords and hints leaked. Adobe misused block-mode 3DES — passwords with the **same hint hashed to the same value** (e.g. "OBVIOUS" → identical hash for all users).

<!--
Identical hints produced identical ciphertexts — the "greatest crossword puzzle in the world."
-->

---

# Pwned Websites (2)

- **Equifax** (2017): credit reporting agency
- **Starwood / Marriott** (2018, 500 million guests)
- **Twitter** (2018): user passwords were logged in plaintext
- **MyFitnessPal** (2018): user diet data, securely hashed passwords
- **Facebook** (2019): user data leaks (146 gigabytes)
- **Twitch** (2021): source code stolen ;)
- **Graff** (2021): jewellery — data on high-profile clients (Trump, Beckham, Oprah)
- **23andMe** (2023): USA DNA testing...

<!--
Even "correct" crypto didn't help: MyFitnessPal hashed fine but leaked health data.
-->

---
layout: section
---

# Client-side / Browser Security

---

# Client-side Security

- Client-side scripting (JavaScript)
- Isolated execution, resource policies
- AJAX

**Websites affecting client-side security:**

- **Cross-site scripting (XSS)**
- **Cross-site request forgery (CSRF)**
- **Tracking & advertisements**

**Browser vulnerabilities:**

- Legacy plugins: **ActiveX, Java, Flash**

---

# JavaScript

- The most popular **ECMAScript** implementation [12]
- Used for webpage scripting (dynamic content, animations)
- **Document Object Model**
- Can also be used for **server scripting** (NodeJS)
- **Sandboxed execution** (e.g. cannot: read user's files, run external programs)
- Modern web applications rendered entirely in JavaScript: **Angular, React, Polymer** etc.

---

# XSS Attack [15]

- **Cross-Site Scripting** / client-side code injection
- E.g.: a messaging board that allows HTML rich text:
  - Someone posts:
    - "I just wanted to say hello!"
    - `<script>pwnThisSucker();</script>`
- If the target website doesn't **filter this**, the code will execute on **any visitor's browser**
- Code can **steal data**, infect victims using a browser exploit, etc.

<!--
XSS = injection, but on the client side and inside trusted origins.
-->

---

# XSS Prevention

- **Escape HTML** before rendering
  - Convert `<` to `&lt;`, `>` to `&gt;`, quotes to `&quot;`, etc.
- Use a **template engine** that does this
- If rich text is required, use a **whitelist-based HTML processor** to sanitize:
  - Strip out dangerous tags like `script`, `embed`, `iframe`, etc.
  - **WARNING:** don't do this unless you know what you're doing!
- Use a **library designed to do this** (e.g. [htmlpurifier.org](http://htmlpurifier.org))

---

# AJAX [13]

- **Asynchronous JavaScript and XML**
- **XMLHttpRequest** — API for issuing background HTTP requests
- Used to build modern, responsive applications
- **XHR re-sends cookies for the requested domain!**

```js
var xhr = new XMLHttpRequest();
xhr.open('get', 'ajax.php');
xhr.onreadystatechange = function() { /*...*/ };
xhr.send(null);
```

---

# Same / Cross Origin Policies [14]

- **Same Origin** = Same **protocol** + **domain** + **port**
- Example: `http://domain.com` vs `https://www.domain.com` (different origins)
- Used to prevent **cross-domain data stealing**
- For example, a user enters `malicious.com`:
  - Malicious.com makes a request for `facebook.com`
  - The request **is** made, but the **response is discarded**
- **Does not prevent information leakage!**
- **CORS** — Cross-Origin Resource Sharing

---

# CORS

- **CORS — Cross-Origin Resource Sharing**
- The target server sends special response headers:

```
Access-Control-Allow-Origin: https://*example.com
```

- If the requester's domain matches this **ACL**, the browser accepts it
- Otherwise, the XHR receives an **error** and the response text is **discarded**

---

# CSRF [16]

- **Cross-Site Request Forgery**
- A malicious website **tricks the browser / user** into accessing a cross-origin URL
- Example (on `malicious.com`):

```html
<img src="https://www.facebook.com/post/?msg=PWNED!"/>
```

- **Defenses:**
  - Don't execute **critical actions on GET requests!**
  - Use **CSRF tokens**
  - Check headers (**Referer**, **X-Requested-With**, etc.)

<!--
Cookies are re-sent automatically (see AJAX) — that's why the forged request "works."
-->

---

# Browser Privacy [17]

- Websites can **track the user across multiple domains!**
  - **Cookies**
  - **Invisible objects or scripts** that do remote requests
    (e.g. Google AdSense, Google Analytics, Facebook)
- **Browser fingerprinting** [19]
- Test yourselves using EFF's [**Panopticlick**](https://panopticlick.eff.org/) [18]
- Tracking servers can become **attack vectors!**
- Extensions that block such requests [20]

---

# Browser Vulnerabilities

- Browsers are a **complex piece of software**
- May have vulnerabilities that allow attackers to **escape sandboxing**
- **Attack vectors:**
  - Malicious websites
  - Code injection on trusted websites (e.g. **XSS**)
  - Browser plugins: **Flash, Java, ActiveX**, etc.

**2015:** Adobe Flash had **96 vulnerabilities** [21]!

**2016:** [22]

- **Flash** most featured in **exploit kits**
- Internet Explorer second place

**Exploit kits:** Angler, RIG, GrandSoft, etc.

---

# Browser Vulnerabilities (3)

**Pwn2Own** — security competition for hacking browsers

**2016 results [23]:**

- 4 bugs in Internet Explorer 11
- 3 bugs in Mozilla Firefox
- 3 bugs in Adobe Reader
- 3 bugs in Adobe Flash
- 2 bugs in Apple Safari
- 1 bug in Google Chrome

**2018 [27]:**

- 5 Apple Safari bugs
- 4 Microsoft Edge bugs
- 1 bug in Mozilla Firefox
- 1 bug in Google Chrome (unsuccessful exploitation)

**2021:** Apple Safari exploit, Zoom Messenger, Chrome & MS Edge

---

# Secure Browsers

If you want a secure browser:

- **Don't use Microsoft's Internet ExploDer!**
- **Block all plugins** by default
- **Always use the latest version** of a browser

**Modern browsers employ multi-process sandboxing:**

- One process per tab with no access to the user's system
- Coordinate with a main browser process
- **Chromium** uses **namespaces + seccomp** on Linux! [24]

---

# OWASP [25]

**The Open Web Application Security Project**

**OWASP Top 10 for 2021** (preview [26]):

<v-clicks>

1. Broken Access Control
2. Cryptographic Failures
3. Injection (SQL, XSS, etc.)
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable and Outdated Components
7. Identification and Authentication Failures
8. Software and Data Integrity Failures
9. Security Logging and Monitoring Failures
10. Server-Side Request Forgery

</v-clicks>

[owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/)

---

# References (1)

- [1] HTTP: [tools.ietf.org/html/rfc2616](https://tools.ietf.org/html/rfc2616)
- [2] Murdoch, S.J. "Hardened stateless session cookies." Int'l Workshop on Security Protocols, Springer, 2008
- [3] TLS 1.2: [tools.ietf.org/html/rfc5246](https://tools.ietf.org/html/rfc5246) (2008)
- [4] TLS attacks: [cloudinsidr.com](https://www.cloudinsidr.com/content/known-attack-vectors-against-tls-implementation-vulnerabilities/)
- [5] CGI: [tools.ietf.org/html/rfc3875](https://tools.ietf.org/html/rfc3875)
- [6] Clarke-Salt, J. *SQL Injection Attacks and Defense*. Elsevier, 2009

---

# References (2)

- [7] Flawed Tutorials: [arxiv.org/pdf/1704.02786.pdf](https://arxiv.org/pdf/1704.02786.pdf)
- [8] Session Fixation: [acros.si](http://www.acros.si/papers/session_fixation.pdf)
- [9] [fishbowl.pastiche.org](https://fishbowl.pastiche.org/archives/docs/PasswordRecovery.pdf) · [PCMag](http://www.pcmag.com/article2/0,2817,11525,00.asp)
- [10] Common Nginx + PHP Misconfiguration: [bit.ly/1kAK8xu](http://bit.ly/1kAK8xu)
- [11] ShellShock: [securityfocus.com/bid/70103](http://www.securityfocus.com/bid/70103)
- [12] ECMA-262: [ecma-international.org](http://www.ecma-international.org/publications/standards/Ecma-262.htm)
- [13] XMLHttpRequest: [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest)

---

# References (3)

- [14] Same-Origin Policy: [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
- [15] [Happy 10th birthday, cross-site scripting](https://blogs.msdn.microsoft.com/dross/2009/12/15/happy-10th-birthday-cross-site-scripting/)
- [16] [nccgroup CSRF paper](https://www.nccgroup.trust/globalassets/our-research/us/whitepapers/csrf_paper.pdf)
- [17] [IEEE Xplore](http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6234427)
- [18] Panopticlick: [panopticlick.eff.org](https://panopticlick.eff.org/)
- [19] How unique is your browser?: [kabijo.de](https://kabijo.de/files/13/14/5641571611600.pdf)
- [20] [lifehacker.com](http://lifehacker.com/the-best-browser-extensions-that-protect-your-privacy-479408034)
- [21] [heimdalsecurity.com](https://heimdalsecurity.com/blog/adobe-flash-vulnerabilities-security-risks/)

---

# References (4)

- [22] [recordedfuture.com/top-vulnerabilities-2016](https://www.recordedfuture.com/top-vulnerabilities-2016/)
- [23] [Pwn2Own 2016](https://venturebeat.com/2016/03/18/pwn2own-2016-chrome-edge-and-safari-hacked-460k-awarded-in-total/)
- [24] [Chromium Linux sandboxing](https://chromium.googlesource.com/chromium/src/+/master/docs/linux_sandboxing.md)
- [25] [owasp.org](https://www.owasp.org/)
- [26] [OWASP Top 10](https://owasp.org/Top10/)
- [27] [Pwn2Own 2018 day two](https://www.thezdi.com/blog/2018/3/15/pwn2own-2018-day-two-results-and-master-of-pwn)

---
layout: end
class: text-center
---

# Thank you

**Further reading:**
OWASP Top 10 — [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten/)

[ocw.cs.pub.ro/courses/isc](https://ocw.cs.pub.ro/courses/isc)
