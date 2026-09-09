## [Introduction to Computer Security Lecture Slides](https://ocw.cs.pub.ro/courses/isc)

© 2024 by Mihai Chiroiu &amp; Florin Stancu

is licensed under Attribution-NonCommercial-ShareAlike 4.0 International

<!-- image -->

## Malicious Software

<!-- image -->

## Objectives

- Definition &amp; classification
- Malware internals
- Malware detection &amp; analysis
- Anti-malware &amp; defense

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

<!-- image -->

## Malware

- 'Little monsters eating your PC's resources'
- Software intentionally designed to cause damage to systems / information.
- Buggy software? NOT really malware :(
- CRWD: 'hold my beer'
- Potentially unwanted applications (grey zone):
- Adware &amp; spyware
- potentially unwanted software: Windows Recall

<!-- image -->

<!-- image -->

## Malware attributes

- Infection / propagation mechanism
- Purpose / functionality
- Affected properties: confidentiality / integrity / availability?
- Stealth &amp; evasion ability
- Persistence
- Command-ability / automatic triggers
- Polymorphism (self-modifying code)

<!-- image -->

## Classification

- By primary distribution method:
- Viruses
- Worms
- Trojan Horses
- Backdoors
- By function: rootkit, adware, RATs, ransomware, miners etc.

<!-- image -->

<!-- image -->

## Virus

- Requires explicit execution / open by user
- Infects &amp; hides inside user's files
- Executable code modification / injection
- File format vectors (macros / scripting / local buffer overflows etc.)
- Spreading media: email attachments, removable drives (e.g., floppy / USB drives), network file sharing etc.

<!-- image -->

<!-- image -->

## Virus Pseudocode (example)

```
infected program entrypoint: start_spreading_thread() call original program entrypoint() resident thread: for (file in scan_disks()): if !check_infection(file): infect(file)
```

<!-- image -->

## Worm

- Automatically spreads remotely via network / application vulnerabilities (mainly, Remote Code Execution)
- Distributed scanning for vulnerable devices:
- early hit lists to bootstrap infection
- local/global IPv4 address generation
- address books for email spreading

<!-- image -->

<!-- image -->

## Early popular viruses

- Creeper / Reaper (1971), RABBIT fork-bomb
- Boot sector viruses (Floppy period):
- Brain (1986) - anti-piracy 'solution';
- Stoned (1987) - fun / hacktivism: 'legalize marijuana'!
- Michelangelo (1991) - destroyed MBR of HDDs, dormant until global effect
- CIH (1998) - highly destructive, erased BIOS flash chips =&gt; hardware unusable!
- Simile (2001) - metamorphic, rebuilds itself [2]
- Windows shortcut viruses
- [Virus Encyclopedia: http://virus.wikidot.com/](http://virus.wikidot.com/)

<!-- image -->

<!-- image -->

## Email-spreading worms

- Macro viruses: Concept, Melissa (1999)
- attachments with macros: 'sexxxy.jpg' / 'naked wife'
- ILOVEYOU (2000) - love letter with .vbs attachment
- Sobig (2003), MyDoom (2004)
- DDoS trigger -&gt; SCO Group &amp; Microsoft
- creators never caught, still active today (:
- Storm Worm (2007)
- '230 dead as storm batters Europe' - spread via clickbaiting
- Koobface (2009 - 2013) - infostealer spread via social apps
- Win32.Antiman.A (2005) ☠

<!-- image -->

## Popular worms (1)

- Morris (1988) - 1st wild worm
- used sendmail vulnerability
- Code Red (2001) - MS IIS vulnerability
- defaced websites, minor
- Blaster / Lovesan (2003)
- DCOM RPC vulnerability stack overflow (:
- SQL Slammer (2003)
- affected Bank of America ATMs
- Daprosy (2009) - autorun worm

<!-- image -->

Welcome to http://www.worm.com! Hacked By Chinese!

<!-- image -->

## Popular worms (2)

- Conficker (2008)
- M$ / NetBIOS exploits (Win 2000 → 7)
- downloaded updates from pseudorandom domains
- Stuxnet (2010)
- Advanced Persistent Threat
- Mainly attacked Iran's SCADA systems, destroyed nuclear centrifuges
- 'most complicated and sophisticated malware at the time'
- Mirai (2016): routers &amp; IoT devices
- Exploit kits: Angler (2015), BlackHole (2010), Nuclear (2016)

<!-- image -->

## Trojan Horse

- User is tricked into opening it
- Targeted: does not propagate automatically
- may be hidden inside exe/docs (like viruses)
- may be installed as late payload by worms!
- Functions: remote access, info stealing (keylogger), botnet zombies, ransomware, backdoor etc.
- Script kiddies: trojan construction kits!

<!-- image -->

<!-- image -->

## RATs

- Remote Admin/Access Tool Trojan
- may have ethical uses (e.g., remote desktop) - if owner consents!
- Usually, installed by social engineering / physical device access
- E.g., spying on your lover(s) - please don't!
- Features:
- Taking full control of the infected machine
- Full file system access (download / upload / execution)
- Online / offline key logging, live webcam / microphone
- Remote shutdown and reboot, disable user input etc.
- Commercial tools / open source projects for building yourself

<!-- image -->

## Historical / popular RATs

- Antiques: Back Orifice / Beast / Sub7 [3] / Houdini
- 'Grey' market: NjRat, MoSucker, ProRAT, DarkHorse, Senna Spy, Pandora etc.
- Open / leaked sources:
- [https://github.com/sin5678/gh0st](https://github.com/sin5678/gh0st)
- [https://github.com/hfiref0x/ZeroAccess](https://github.com/hfiref0x/ZeroAccess)
- [https://github.com/killeven/Poison-Ivy-Reload](https://github.com/killeven/Poison-Ivy-Reload)
- https://github.com/PushpenderIndia/thorse (Python3 :D)
- [https://github.com/UpSetst/SilverRAT-FULL-So urce-Code](https://github.com/UpSetst/SilverRAT-FULL-Source-Code)

<!-- image -->

<!-- image -->

<!-- image -->

## Backdoors / Supply Chain

- Highly targeted:
- Installed at manufacturing / compile time ('supply chain attacks')
- Inserterted via vulnerabilities in a system
- They just 'keep the door open' for future payload execution
- Examples:
- libXZ compile-time auth. bypass for OpenSSH server
- NIST Dual EC DRBG crypto RNG by NSA (speculated)
- Master passwords in Cisco &amp; Juniper routers/firewalls
- Numerous NPM / Python packages, PC/Android/iOS apps (e.g., VLC) etc.

<!-- image -->

## Rootkits

- Actively prevent detection, offer privileged (root) access
- concealment (userspace / kernel / hypervisor / firmware)
- antivirus software manipulation
- persistence (survive reboots)
- stealth network communication / updates
- Usually embeds / combines with a RAT or backdoor
- Benign uses? there are some ;)
- [https://github.com/milabs/awesome-linux-rootkits](https://github.com/milabs/awesome-linux-rootkits)

<!-- image -->

## Execution concealment

- User mode:
- System file hiding (e.g., inside C:\Windows\System32 )
- Library injection (e.g., explorer.exe plugin)
- Binary patching / detour hooks
- Kernel mode:
- kernel modules (run with SYSTEM privileges / modprobe)
- system call table patching
- Firmware-level (SMM rootkits)
- Code obfuscators / packers

<!-- image -->

<!-- image -->

## Command &amp; Control / stealth comm.

- Botnet: command &amp; control
- Centralized -&gt; 'easy' to shutdown
- ■ except for generated DNS
- Peer-2-peer
- Encryption, D-H, asymmetric keys …
- Stealth communication + data exfiltration:
- hide in plain sight
- transported using common protocols: HTTP, DNS, SNMP, ICMP, SNMP, ARP
- Extreme Covert Channels: 1 bit at a time (:

<!-- image -->

<!-- image -->

## Ransomware

- Usually worms, very destructive
- Delete / steal / encrypt user's documents
- Advanced techniques (asymmetric ciphers, timed triggers etc.)
- CryptoLocker (2013), WannaCry (2017), Petya
- Ransomware as a Service (e.g., REvil, Hive)

<!-- image -->

<!-- image -->

## White-hat time! Malware defense?

- Endpoint protection:
- Realtime protection (AVs) / malware scanning tools
- Cloud-based endpoint protection
- Periodic updates &amp; backups !
- Network protection:
- Firewalling (or the extreme: air gapping)
- Cloud-based threat intelligence
- Honeypots
- Malware analysis
- Reverse engineering tools
- Sandboxes

<!-- image -->

<!-- image -->

Security Simplified

## Malware detection

- File/memory integrity checks
- Signature-based scans
- vs new or self-modifying (polymorphic) malware?
- advanced patterns (e.g., regular expressions)
- Behavioral heuristics (e.g., opened files, system calls)
- Machine learning (requires training phase + resource-intensive)
- Network traffic / anomaly detection
- Intrusion Detection / Prevention Systems

<!-- image -->

## Endpoint security tools

- Historical: Symantec Norton, McAfee, 󰐮 Kaspersky, ESET Nod32
- ' Kaspersky deletes itself, installs UltraAV antivirus without warning '
- Microsoft: buys [RO] GeCAD (2003), Windows Defender (2005)
- Actually, Defender was based on prev. acquired GIANT AntiSpyware
- Softwin (1996) -&gt; Bitdefender (2001)
- Cloud threat intelligence: Crowdstrike, Sophos, Cisco AMP / Fortinet / Palo Alto / Check Point etc.
- ^ ^ ^ mostly for Windows (&amp; Mac OS X, probably 🤑 )
- Open source : ClamAV =&gt; Linux support!
- Linux rootkit detectors: chkrootkit, rkhunter, clamav, LMD

<!-- image -->

## Malware datasets &amp; intelligence

- EICAR Anti-Virus Test File - simple test files (not malware)
- Many free malware databases:
- VirusShare, Malware Bazaar, Canadian Institute of Cybersecurity, SOREL-20M, BODMAS, VirusSign etc.
- Multi-scanning: VirusTotal
- AV companies publish latest threats (responsible disclosure!)
- for fame &amp; profit
- also share threat info with each other via partnerships
- Companies crowdsource unknown threats from cloud customers
- 'all for one and one for all'

<!-- image -->

## Malware analysis

- Quick response -&gt; isolation!
- Stealth rootkit? Put RAM into freezer :)
- Sandboxing - execute piece inside a virtual machine to study its behavior
- must make environment undetectable!
- sometimes: simulate entire network of devices to capture malware before production (honeypots)!
- Reverse engineering tools (+ skillz) [4] [5]
- IDA Pro / Ghidra / Binary Ninja / gdb + pwndbg etc.
- Sysinternals (MS) / frida / radare2 / ptrace / eBPF

<!-- image -->

## Bibliography

- [[1] https://people.scs.carleton.ca/~paulv/toolsjewels/TJrev1/ch7-rev1.pdf](https://people.scs.carleton.ca/~paulv/toolsjewels/TJrev1/ch7-rev1.pdf)
- [2] Win32/Simile
- [https://docs.broadcom.com/doc/striking-similarities-metamorphic-virus-code-03-en](https://docs.broadcom.com/doc/striking-similarities-metamorphic-virus-code-03-en)
- [[3] https://medium.com/phrozen/a-malware-retrospective-subseven-d86fed0c88bf](https://medium.com/phrozen/a-malware-retrospective-subseven-d86fed0c88bf)
- [[4] https://www.stationx.net/malware-analysis-tools/](https://www.stationx.net/malware-analysis-tools/)
- [[5] https://github.com/onethawt/reverseengineering-reading-list](https://github.com/onethawt/reverseengineering-reading-list)

<!-- image -->