# 🦇 NIGHT HUNTER



<p align="center">

  <img src="public/night-hunter-logo.jpeg" alt="Night Hunter Logo" width="160" style="border-radius: 50%;" />

</p>



<p align="center">

  <strong>Next-Generation Defensive Security & Threat Intelligence Command Center</strong><br />

  <em>Auditing · Target Reconnaissance · Network Intelligence · Phishing Detection</em>

</p>



<p align="center">

  <a href="https://night-hunter-f2w4.onrender.com"><img src="https://img.shields.io/badge/Live_Cloud_App-Online-4ade80?style=for-the-badge&logo=render" alt="Live Cloud Demo" /></a>

  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License: MIT" /></a>

  <a href="#"><img src="https://img.shields.io/badge/Platforms-Windows%20%7C%20Linux%20%7C%20Android-8b5cf6?style=for-the-badge" alt="Platforms" /></a>

  <a href="#"><img src="https://img.shields.io/badge/Python-3.10%2B-ffd480?style=for-the-badge&logo=python" alt="Python 3.10+" /></a>

</p>



---



## ⚡ Overview



**Night Hunter** is an all-in-one defensive security workbench built for cybersecurity researchers, ethical hackers, system administrators, and developers. It consolidates multiple critical security disciplines—web vulnerability auditing, local LAN & Nmap device reconnaissance, phishing heuristics, credential strength auditing, and cryptographic hashing—into an intuitive, modern command center.



Night Hunter operates in two complementary modes:

1. **Desktop / Cloud Graphical Workspace**: A fast cyberpunk UI built with React & Vite.

2. **Terminal CLI Engine**: A command-line toolkit tailored for headless Linux servers, Kali Linux, and Android Termux environments.



🌐 **Official Live Web Application:** [night-hunter-f2w4.onrender.com](https://night-hunter-f2w4.onrender.com)  

📘 **Complete setup and user guide:** [USER_GUIDE.md](USER_GUIDE.md)



---



## 🚀 Quick Start (Run from Source)



```bash
# 1. Clone the repository
git clone https://github.com/ArnabHalder-CS/Night-Hunter.git
cd Night-Hunter

# 2. Install Python dependencies
pip install -r requirement.txt

# 3. Launch CLI Mode
python main.py

# 4. OR Launch Web Dashboard
waitress-serve --port=5000 api.server:app
# Open http://localhost:5000 in your browser
```



---



## 💎 Why Night Hunter? (Built for Real Security Operations)



| Feature | The Old Way (Fragmented Tools) | The Night Hunter Advantage |

|---|---|---|

| **🎯 Accuracy** | Simulated progress bars & toy data | **Real active scanning** via native sockets & Nmap with OS fingerprinting (runs best locally) |

| **⚡ Workflow** | Juggling 5 terminal windows (Nmap, DevTools, CyberChef) | **Unified Single Pane of Glass** combining Web, LAN, Phishing, Passwords & Crypto |

| **🛡️ Phishing Safety** | Risky remote page fetching that can execute malware | **Zero-Risk Passive Inspection** identifying homoglyphs & brand spoofs without connecting |

| **💻 Portability** | Complex Python venvs, pip breakages & missing C tools | **Single-file `.exe` on Windows**, 1-command installer on Kali, or Android Termux on the go |

| **📑 Reporting** | Hours spent writing manual markdown & taking screenshots | **1-Click Multi-Format Reports** in client-ready HTML, machine-readable JSON, & TXT |



---



## 🛡️ Core Modules & Capabilities



### 1. 🌐 Web Security Intelligence & Scanner Hub

* **Built-in Web Vulnerability Audit**: Header inspection, server banners, insecure HTTP methods (PUT/DELETE/TRACE), and sensitive file disclosure (.env, .git, robots.txt).

* **Local Scanner Hub Integration**: Orchestrate native CLI engines directly from the dashboard:

  * **Nikto**: Web server misconfiguration and known-vulnerability audit.

  * **Nuclei**: Fast, template-based vulnerability assessment.

  * **OpenVAS / Greenbone**: Comprehensive network vulnerability scanning via `gvm-cli`.



### 2. 🎣 Phishing Intelligence & Spoofing Station (Flagship)

* **URL Risk & Heuristics Engine**: Passive evaluation calculating 0-100 risk score, risk level, entropy, and threat indicators.

* **Homoglyph & Brand Spoof Lab**: Interactive Unicode lookalike detector uncovering Cyrillic/Greek character substitution (e.g. `pаypal.com`) and Punycode (`xn--...`).

* **Email & SMS Social Engineering Triage**: Extracts embedded links, flags urgency triggers (Account Suspension, Financial Threats, Credential Verification), and audits all discovered links.

* **Immediate Containment Playbook**: Tactical DNS sinkholing, abuse reporting, and global threat feed submission steps.



### 3. 🧮 Crypto Analyst & Key Station (Flagship)

* **Simultaneous Multi-Hash Engine**: Generates 10+ standard digests simultaneously (MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512, SHA3-256, SHA3-512, BLAKE2b, BLAKE2s) with live match verification.

* **Hash Format Identifier & Analyst**: Analyzes unknown hashes by length, character set, and Shannon entropy to identify candidates (MD5, SHA-1, SHA-256, Bcrypt, Argon2, Linux shadow crypt) with confidence and security status.

* **Multi-Format Encoders**: Base64, Hexadecimal, URL (RFC 3986), and ROT13 with quick swap.

* **CSPRNG Key Station**: Kernel-entropy AES-128, AES-256, Base64URL API bearer tokens, and UUIDv4 generation.

* **HMAC Signer**: Keyed-hash authentication (HMAC-SHA256, HMAC-SHA512).



### 4. 📡 Network Security & Nmap Reconnaissance

* **Verified Local Nmap**: OS fingerprinting, UDP service scans (`-sU`), and named XML profiles.

* **LAN Device Discovery**: Host discovery and live port states with service/product versions.



### 5. 🔑 Password Security & Credential Audit

* **Entropy & Pattern Analysis**: Real-time evaluation against common dictionary passwords, keyboard walks, and character diversity.

* **Cryptographic Token Generator**: Local CSPRNG passphrase and secret generator.



### 6. 📑 Security Reporting

* **Multi-Format Export**: Generates defensive audit reports in JSON, TXT, or styled HTML formats.

* **Audit Logs**: Tracks past scan activities locally on your machine.



---



## 🚀 Quick Start & Installation



### Option 1: Windows Setup

1. Open PowerShell or Command Prompt:
   ash
   git clone https://github.com/ArnabHalder-CS/Night-Hunter.git
   cd Night-Hunter
   pip install -r requirement.txt
   python main.py
   2. Or double-click start_night_hunter.bat to launch the local web dashboard.

---

### Option 2: Linux (Kali Linux, Ubuntu, Debian, Arch)

ash
git clone https://github.com/ArnabHalder-CS/Night-Hunter.git
cd Night-Hunter
bash install.sh
./run.sh

---

### Option 3: Android (Termux)

ash
git clone https://github.com/ArnabHalder-CS/Night-Hunter.git
cd Night-Hunter
bash termux-install.sh
python main.py

---

### Option 4: Run Directly from Source



```bash

# Clone the repository

git clone https://github.com/ArnabHalder-CS/Night-Hunter.git

cd Night-Hunter



# Install Python requirements

pip install -r requirement.txt



# Start backend server

python api/server.py



# (Optional) Run CLI version directly

python main.py

```



---



## 🔒 Verification, Trust & Policies



To verify downloaded binaries against tamper-proof checksums:

* Checksum registry: [SHA256SUMS](SHA256SUMS)

* [Privacy Policy](PRIVACY.md)

* [Security Policy & Responsible Disclosure](SECURITY.md)

* [Distribution & Package Notes](DISTRIBUTION.md)



---



## 💻 Tech Stack & Architecture



| Layer | Technology |

|---|---|

| **Frontend** | React 19, Vite, Tailwind-style modular CSS, Lucide Icons |

| **Backend API** | Python 3, Flask, Flask-CORS |

| **Reconnaissance Engine** | Socket network primitives, Nmap integration, Scapy heuristics |

| **Packaging** | PyInstaller (Single-file Windows executable), Shell installers |

| **Deployment** | Render Cloud PaaS (Dockerized multi-stage build) |



---



## ⚖️ Legal Disclaimer & Limitation of Liability



> [!CAUTION]

> **PLEASE READ CAREFULLY BEFORE USING THIS SOFTWARE**



This software, **Night Hunter**, is designed, developed, and distributed solely for **educational, defensive, authorized system auditing, and security research purposes**.



1. **Authorized Usage Only**: You must only use Night Hunter on networks, hosts, devices, and websites that you own or where you have received **explicit, prior written permission** from the system owner or network administrator.

2. **Prohibited Activities**: Scanning, auditing, stress-testing, or reconnaissance conducted against third-party systems without prior authorization is illegal and violates computer crime laws, including the **United States Computer Fraud and Abuse Act (CFAA)**, the **UK Computer Misuse Act**, the **Indian Information Technology Act (IT Act 2000)**, and equivalent international cybersecurity legislation.

3. **Limitation of Liability & Author Indemnification**: 

   - **Under no circumstances shall the author and developer, Arnab Halder, or any project contributors, be held liable, issued legal notices, or held responsible for any direct, indirect, incidental, punitive, or consequential damages, legal repercussions, financial losses, system downtime, or criminal charges arising from the use, misuse, abuse, or deployment of this software.**

   - **The author, Arnab Halder, does not condone, promote, or support malicious hacking, unauthorized intrusion, or cyber attacks of any kind.**

   - **The end user assumes 100% full legal, civil, and criminal responsibility for their own actions and operations conducted using this software.**

4. **"AS-IS" Warranty Disclaimer**: This software is provided strictly on an "AS IS" and "AS AVAILABLE" basis, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.



---



## 🤝 Contributing



Contributions, feature suggestions, and security research improvements are welcome!



1. Fork the repository (`git fork`)

2. Create your feature branch (`git checkout -b feature/AmazingSecurityModule`)

3. Commit your changes (`git commit -m 'feat: add enhanced recon rule'`)

4. Push to the branch (`git push origin feature/AmazingSecurityModule`)

5. Open a **Pull Request**



---



## 📜 License



Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more details.



---



<p align="center">

  Crafted with care by <a href="https://github.com/ArnabHalder-CS"><strong>Arnab Halder</strong></a> and community contributors.<br />

  <em>Stay ethical. Defend your perimeter. Protect the web.</em>

</p>

