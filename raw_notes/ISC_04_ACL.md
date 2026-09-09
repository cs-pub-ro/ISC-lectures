## [Introduction to Computer Security Lecture Slides](https://ocw.cs.pub.ro/courses/isc)

© 2024 by Mihai Chiroiu &amp; Florin Stancu

is licensed under Attribution-NonCommercial-ShareAlike 4.0 International

<!-- image -->

## Authorization, Access Control, Operating System Security

<!-- image -->

## Access control

<!-- image -->

<!-- image -->

<!-- image -->

## Examples of Access Control

- Social Networks: access to personal information.
- Web Browsers: access only to a website (same origin policy).
- Operating  Systems:  one  user  cannot  arbitrarily  access/kill  another user's files/processes.
- CPU Memory Protection: code in one region (e.g., Ring 3), cannot access the data in another more privileged region (e.g. Ring 0).
- Firewalls:  If  a  packet  matches  with  certain  conditions,  it  will  be dropped.

<!-- image -->

## PEI Model [1]

<!-- image -->

<!-- image -->

## Vocabulary

- Basic abstractions:
- Subjects
- Objects
- Rights
- A subject is an entity who wishes to access a certain object , which is a resource (e.g., a file or a network packet). The different modes of access (e.g., reading, writing) are called permissions .

<!-- image -->

## Vocabulary - Users and Principals

<!-- image -->

A Principal is an User authenticated in a context Principals - Unit of Access Control and Authorization

<!-- image -->

## Vocabulary - Users and Principals

## Principals

<!-- image -->

: the user can emit principals with downgraded privileges

<!-- image -->

Example

## Vocabulary - Principals and subjects

<!-- image -->

A subject is a program executing on behalf of a principal

<!-- image -->

## Vocabulary

- The relation between Users and Principals is One-To-Many
- Allows  accountability  of  user's  actions,  use  least  privileges  required  for  a task
- E.g., service accounts / API keys (authentication w/o password)
- For  simplicity,  a  principal  and  subject  can  be  treated  as  identical concepts.

<!-- image -->

## Vocabulary - Objects

- An  object  is  anything  on  which  a  subject  can  perform operations (mediated by rights)
- Usually objects are passive, for example:
- File
- Directory (or Folder)
- Memory segment
- But,  subjects  (e.g.,  processes)  can  also  be  objects,  with specific operations
- kill
- suspend
- resume

<!-- image -->

## Access control models

<!-- image -->

## Access control enforcement

- Discretionary  access  controls  (DAC) -  the  access  of  objects  (or subjects) can be propagated from one subject to another. Possession  of  an  access  right  by  a  subject  is  sufficient  to  allow access to the object.
- Mandatory  access  controls  (MAC) -  the  access  of  subjects  to objects is based on a system-wide policies (based on security labels) that can be changed only by the administrator.
- Role-Based Access Control (RBAC) - can be configured as both MAC or DAC, access to objects is based on roles.

<!-- image -->

## Access control enforcement

- Attribute-Based Access Control (ABAC) - properties of an object are used when usage decision are made .
- Usage Control (UCON) - generalization of access control to include authorization,  obligations,  conditions  (e.g.,  quotas),  continuity  and mutability of attributes.

<!-- image -->

## Discretionary access controls

<!-- image -->

## DAC

- No precise definition.
- Basically, DAC allows access rights to be propagated at subject's discretion
- often has the notion of owner of an object
- used in UNIX, Windows, etc.

<!-- image -->

## Formal rule representation

- Let S be the set of all subjects, O the set of all objects, and P the set of all permissions. The description of access control can be given by a set A ⊆ S × O × P .
- When new permissions  are  added,  triplets  are  added  to  A;  when they are removed (revoked), triplets are deleted.

<!-- image -->

## Matrix Representation

- An access control matrix is a matrix (Ms,o) whose rows are subjects and  columns  are  objects.  Element  (Ms,o) ⊆ P is the  set  of permissions that subject S is authorized for object o.

Objects (and Subjects)

|          | catalog.csv   |    | cat-anonim.txt   | /dev/kmem   | /sbin/sudo   | PID 1001   |
|----------|---------------|----|------------------|-------------|--------------|------------|
| Subjects | Root          | rw | rwx              | -           | rwx          | kill       |
|          | mihai         | rw | rw               | -           | rx           | kill       |
|          | student       | -  | r                | -           | rx           | -          |
|          | guest         | -  | -                | -           | -            | -          |

<!-- image -->

## Access Control Lists (ACL)

- An access control list is a set {Ao | o ∈ O},  one element for each object . The elements of the list are the pairs (s, p) of subjects s who have permission p to that object.

## catalog.csv

root: rw

mihai: rw

| cat-anonim.txt   |
|------------------|
| root: rw         |
| mihai: rw        |
| student: r       |

<!-- image -->

| /sbin/sudo   |
|--------------|
| root: rwx    |
| mihai: rx    |
| student: r   |

## Classic POSIX Model

- Objects : files; Permissions : R, W, X + specials (SUID/SGID/sticky)
- Subjects : users, groups, others
- Stored as bit masks (written in base 8 - octal) on inodes
- Bit mask: 111|101|100 =&gt; octal 754
- Modern OSes support Full Access Control Lists
- multiple subjects!

```
➜ ls -l /usr/bin/ping -rwxr-xr-- 1 root admin 92K Jan 18 08:05 /usr/bin/ping
```

<!-- image -->

## Capability Lists

- Alternate  access  control  implementation:  each  user  stores  a  list  of his/hers capabilities instead of objects' storing ACLs.
- Storing capabilities means giving to each subject tokens which give them access to the permissions they are entitled

|         | catalog.csv   | cat-anonim.txt   | /dev/kmem   | /sbin/sudo   | PID 1001   |
|---------|---------------|------------------|-------------|--------------|------------|
| Root    | rw            | rw               | rw          | rwx          | kill       |
| mihai   | rw            | rw               | -           | rx           | kill       |
| student | -             | r                | -           | rx           | -          |
| guest   | -             | -                | -           | -            | -          |

<!-- image -->

## Capability examples

- Posix API descriptors:

```
int fd = open("/etc/passwd", O_RDWR); Code flow: fork() -> setuidgid() -> exec()
```

-&gt; new process inherits fd (the authorization 'token')

- Linux: per-process capabilities
- Windows : Security Identifier (SID) on Active Directory

<!-- image -->

## ACL vs. Capabilities

- ACL require authentication of subjects
- Capabilities  do  not  require  authentication  of  subjects,  but  do require  unforgeability  and  control  of  propagation  of  capabilities. Usually implemented through cryptography.
- The Confused Deputy Problem [1986]
- E.g.:  Cross-Site Scripting / Forgery (XSS / CSRF), setuid privilege escalation (e.g., sudo)
- Solution: bundle resource access together with capability

<!-- image -->

## DAC Problems

- The  underlying  philosophy  of  DAC  is  that  subjects  can  determine who has access to their objects
- There  is  a  difference,  though,  between  trusting  a  person  and  trusting  a program
- The copies of a file are not controlled
- Trojan Horse attack [1970]
- Solution: use MAC ☺

<!-- image -->

<!-- image -->

## Trojan Horse attack

<!-- image -->

<!-- image -->

## Buggy software can become Trojan Horses

- When a subject (e.g., buggy software) is exploited, it executes the code / intention of the attacker, while using the privileges of the user who started it!
- This means that DAC-only systems cannot be trusted with classified information!

<!-- image -->

## Principle of Least Privilege

- Each subject should have only necessary privileges!
- Privilege elevation / dropping
- Unix: setuid() / setgid() family of system calls
- Example POSIX scenario:
- Only root can open ports &lt;= 1024
- Web server (e.g., apache2) starts as root
- Opens log files, sockets etc. when root then drops all root privileges (user changes to www-data )!
- Modern alternative : Linux capabilities ( CAP\_NET\_BIND\_SERVICE )
- Better yet: DAC + Mandatory Access Control!

<!-- image -->

## Mandatory access controls

<!-- image -->

## Mandatory Access Control

- Assigning access rights based on regulations by a central authority
- Implemented using a 'reference monitor'
- Small Trusted Computing Base (TCB) [John Rushby, 1981, OSP]
- Kernel &lt; Hypervisor &lt; Hardware
- TOCTTOU (Time Of Check To Time of Use) problem:
- authority checks access to an object
- unknowingly to him, attacker replaces object with another one
- privileged subject operates on attacker controlled object!

<!-- image -->

## MAC implementations

- Type Enforcement (e.g.: SELinux)
- Subjects =&gt; grouped in domains ( labels )
- Objects =&gt; grouped in types ( another / same kind of labels )
- Domain-Domain + Domain-Type permissions
- If a MAC rule fails =&gt; DAC not checked, access denied!

```
# TE rule: allow passwd_t shadow_t : file {read, write … } # ls -Z /etc/shadow -r----  root   root  system_u:object_r:shadow_t  shadow # ps -aZ gigel:user_r:passwd_t   16532 pts/0 00:00:00 passwd
```

<!-- image -->

## Modeling Access Control

- Multi-level security (MLS)
- Bell-LaPadula (BLP)
- Biba Model
- Chinese Wall

<!-- image -->

## Multi-level security (MLS)

- The  capability  of  a  computer  system  to  carry  information  with different sensitivities Top Secret
- Bell-LaPadula (BLP) Model [1973]
- Biba Model

<!-- image -->

<!-- image -->

## BLP Model

- Aims to capture confidentiality (read) requirements only
- Modelled as transitions through a set of states, starting from an initial state.
- State = Object, access matrix, current access information
- State transition rules describe how a system can go from one state to another
- Each object has a classification level
- Each subject s has a security clearance

<!-- image -->

## BLP Model

- A state is secure if:
- A) Simple Security Property (SS): no subject may read data at a higher level
- ·
- B) The *(Star)-Property (SP): no subject may write data at a lower level (due to the fear of Trojan Horse / information leaks)
- A system is secure if and only if every reachable state is secure.

<!-- image -->

## BLP Problems

- No communication (e.g., acknowledges) from High to Low
- Not all system components can be enforced by BLP, e.g., memory management must have access to all levels
- Called 'trusted subjects' (part of TCB)
- Can overwrite high and more important files
- Prevent overwrites unless same level!

<!-- image -->

## BLP Problems

- Covert channels cannot be blocked by star-property

<!-- image -->

<!-- image -->

## Biba Model

- Integrity is also very important
- Each subject (process) has an integrity level; Each object has an integrity level ; Integrity levels are totally ordered
- NO read down; NO write up
- BLP upside down
- The integrity of an object is the lowest level of all the objects that contributed to its creation

<!-- image -->

## Biba Model

- Used by Windows
- E.g., A Internet Explorer Browser can download a file (created with a low  integrity  level)  and  read  everything  in  the  system.  It  cannot write to a higher level object.

<!-- image -->

## Chinese Wall (Brewer and Nash model) [1989]

<!-- image -->

<!-- image -->

<!-- image -->

## Chinese Wall

- S can read O only if
- O is in the same company dataset as some object previously read by S (i.e., O is within the wall) or
- O belongs to a conflict of interest class within which S has not read any object (i.e., O is in the open)
- S can write O only if
- S can read O by the simple security rule and
- no object can be read which is in a different company dataset to the one for which write access is request

<!-- image -->

## Role-Based Access Control

Group-based access control

<!-- image -->

## Role-Based Access Control

- In the real world, security policies are dynamic.
- E.g., a user promotes at his job, therefore his rights must change (deleted, added, etc.)
- RBACs are more flexible: can simulate MAC &amp; DAC!

<!-- image -->

<!-- image -->

## Roles as policy

- A role brings together
- a collection of users
- a collection of permissions
- These collections can be modified independently
- A user can be a member of many roles
- Each role can have many users as Each role can have many users as members
- Roles may be hierarchical

<!-- image -->

## Role-Based Access Control

<!-- image -->

<!-- image -->

## RBAC Shortcomings

- Role granularity may lead to role explosion
- Role design and engineering is difficult and expensive
- Assignment of users/permissions to roles is cumbersome
- Adjustment based on local/global situational factors is difficult

<!-- image -->

## Authorization Implementations

<!-- image -->

## OAuth

- Open Authorization, not Authentication!
- Users delegate API access to third party services without giving password!
- e.g. give Google Calendar API access to task management app
- JSON Web Token (JWT) - may contain subject IDs + capability lists
- Authorization flow: client / server-side
- OpenID Connect: OAuth popular choice for SSO authentication !
- Obtain token with read-only access to Google API endpoint returning your email address =&gt; third-party service identifies you!

<!-- image -->

## Writing Authorization Code

- Tons of conditionals?
- Solution: use language features &amp; authorization frameworks

```
if is_admin or (can_read(obj.parent) and can_write(obj)) ...
```

```
@authorize.create(Article) def create_article(name): # implementation here @authorize.read def read_article(article): # implementation here
```

<!-- image -->

## Best Practices

- Design during early requirements phase
- Model as subjects, objects and permissions
- Use an appropriate policy model (DAC, RBAC, ABAC etc.)
- Use middleware / framework if available
- If not, create your own! DO NOT copy-paste duplicate code!
- Implement resource limits / quotas
- Sanitize/normalize user input !!!

```
requested_file.startswith("/home/user/share/") requested_file = "/home/user/share/../../../etc/shadow"
```

<!-- image -->

## The Human Factor

<!-- image -->

## Security and humans

- Security policies must be in place … and must be followed.
- Regardless of how strong (and expensive) your secure deployment is:
- Humans can still write their passwords on post-it notes
- Humans can still give their passwords to anyone they trust
- Humans can still open tempting attachments …

<!-- image -->

## Social engineering

- Non-technical intrusion
- Involves tricking people to break security policies
- Manipulation
- Relies on false confidence
- Everyone trusts someone
- Authority is usually trusted by default
- Non-technical people don't want to admit their lack of expertise
- They ask fewer questions.
- Most people are eager to help.
- When the attacker poses as a fellow employee in need.

<!-- image -->

## Social engineering

- People are not aware of the value of the information they possess.
- Vanity, authority, eavesdropping - they all work.
- When successful, social engineering bypasses ANY kind of security.

<!-- image -->

<!-- image -->

## Types of phishing

- By used technology
- Smishing (SMS)
- Vishing (Voice)
- Email phishing
- Angler phishing (via social networks)
- By target
- Watering Hole Phishing (people visiting a certain website)
- Spear phishing (a specific organization)
- Whaling (C-level from a specific organization)

<!-- image -->

## Resources

- [1] [http://www.profsandhu.com/confrnc/asiaccs/asiaccs06-pei.pdf](http://www.profsandhu.com/confrnc/asiaccs/asiaccs06-pei.pdf)
- [2] [http://www.cs.cornell.edu/courses/cs5430/2011sp/NL.accessControl.html](http://www.cs.cornell.edu/courses/cs5430/2011sp/NL.accessControl.html)
- [3] [http://cnitarot.github.io/courses/cs526\_Spring\_2015/s2014\_526\_ac.pdf](http://cnitarot.github.io/courses/cs526_Spring_2015/s2014_526_ac.pdf)
- [4] [https://people.cs.rutgers.edu/~pxk/419/notes/access.html](https://people.cs.rutgers.edu/~pxk/419/notes/access.html)

<!-- image -->