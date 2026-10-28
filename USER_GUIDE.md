# Night Hunter user guide

Night Hunter is a defensive-security workbench for systems, websites, and networks that you own or have explicit permission to assess. It has two modes:

- **Cloud dashboard** — use in a browser for phishing analysis, cryptography utilities, reports, and the built-in web audit.
- **Local installation** — use on Windows, Linux, or Termux for device-local capabilities such as Nmap, Nikto, Nuclei, and OpenVAS/Greenbone.

> Only scan targets you own or are authorised to test. Do not use Night Hunter for denial-of-service activity, credential theft, or unauthorised scanning.

## 1. Choose how to use it

| What you need | Best option |
|---|---|
| Analyse a suspicious URL, email, SMS, OTP scam, or hash | Cloud dashboard or local app |
| Use the premium dashboard on Windows | Windows portable package or source install |
| Use Nmap, Nikto, Nuclei, or OpenVAS | Linux local installation recommended |
| Use command-line tools on Android | Termux package |
| Keep the app available from any phone/browser | Cloud dashboard |

The public dashboard is: <https://night-hunter-0br7.onrender.com>

## 2. Cloud dashboard

Open the link above and select **Open Dashboard** / **App**.

### What works in cloud mode

- Phishing URL risk inspection
- Scam message, email, SMS, fake support, delivery and OTP-request triage
- Homoglyph / brand-lookalike checks
- Cryptography lab: hashes, hash identification, Base64/Base32/Hex/Binary/URL transforms, ROT13, Caesar, JWT inspection, HMAC and secure key material
- Reports and history saved by the service
- Night Hunter’s authorised web audit

### Cloud mode limits

Nikto, Nuclei, Nmap, and OpenVAS are **not** executed by Render. They require a scanner installed on the operator's own device or authorised network. The dashboard displays their true availability; it never fabricates a result.

Render's free tier may take a short time to wake after inactivity.

## 3. Windows installation

### Portable package

1. Download `night-hunter-windows.zip` from the project Releases page.
2. Extract it to a normal folder, for example `Documents\NightHunter`.
3. Double-click `start_night_hunter.bat`.
4. The browser opens `http://127.0.0.1:5000/app`.

### From source

Install Python 3.10+ and Node.js 20+ first. In PowerShell:

```powershell
git clone https://github.com/ArnabHalder-CS/Night-Hunter.git
cd Night-Hunter
python -m pip install -r requirement.txt
npm install
npm run build
python -m waitress --listen=127.0.0.1:5000 api.server:app
```

Then browse to `http://127.0.0.1:5000/app`.

Windows supports the core dashboard and built-in audit. For Nikto and OpenVAS, use a Linux machine, VM, or WSL environment. Nuclei can run on Windows if it is installed and added to PATH.

## 4. Linux installation

### Option A: Instant Run (No installation required)

```bash
tar -xzf night-hunter-linux.tar.gz
cd night-hunter-linux
./run.sh
```
This automatically sets up Python dependencies and launches the full graphical Web Dashboard in your browser at `http://127.0.0.1:5000`.

### Option B: System-Wide Install

```bash
tar -xzf night-hunter-linux.tar.gz
cd night-hunter-linux
bash install.sh
NightHunter
```

- Launches the Web Dashboard by default and opens your browser.
- Runs anywhere on your system by typing `NightHunter`.
- Creates a desktop shortcut in your Kali Application Menu.
- Use `NightHunter --cli` if running in an SSH or headless terminal.

## 5. Android Termux installation

1. Install Termux from a trusted source such as F-Droid.
2. Download `night-hunter-termux.zip` from Releases.
3. In Termux run:

```bash
termux-setup-storage
cd ~/storage/downloads
unzip night-hunter-termux.zip
cd night-hunter-termux
bash termux-install.sh
NightHunter
```

Termux supports the CLI and installed local tools such as Nmap. Full Greenbone/OpenVAS is generally too resource-heavy for a phone; use Linux for that.

## 6. Module guide

### Phishing Analyzer

**URL Risk Inspector**: paste a complete URL. Night Hunter performs a passive structural review without loading the target page in your browser.

**Homoglyph & Brand Lab**: paste a domain such as `paypaI.example` to detect mixed Unicode characters and lookalike brands.

**Scam Message Analyzer**: paste a full email, SMS, WhatsApp text, OTP request, fake delivery note, investment/crypto message, or support chat. The result shows:

- local heuristic score and risk level
- warning categories such as OTP requests, urgency, payment lures, impersonation, delivery lures, or crypto scams
- extracted links for separate passive inspection
- safe next actions

The score is a warning aid, not proof that a sender is fraudulent.

### Cryptography

| Tool | Purpose |
|---|---|
| Multi-hash | Creates common MD5, SHA, SHA-3 and BLAKE2 digests for integrity comparison |
| Hash identifier | Suggests possible algorithms from a digest format; it cannot recover a password |
| Transforms | Base64, Base32, Hex, Binary, URL, ROT13 and educational Caesar transformations |
| JWT inspector | Reads a token header/payload only; it **does not verify** its signature |
| CSPRNG keys | Generates random key material/tokens locally |
| HMAC | Creates keyed SHA-256 or SHA-512 message digests |

Encoding is not encryption. ROT13 and Caesar are educational transforms and must not be used to protect sensitive information.

### Web Security

Tick the authorisation checkbox, enter a complete `https://` or `http://` URL, and select **Start Scan**. The built-in authorised audit checks headers, TLS, cookies, HTTP methods, public endpoints, technology signals and safe reflection indicators.

Validate every finding manually before reporting it or changing a system.

### Network Security

Use this only from a local installation. The Nmap workspace shows installed profiles and streams real results as they arrive. Cloud mode intentionally does not run local network scans.

## 7. Advanced scanner hub

The Web Security page shows each integration's real status.

### Nikto

Install Nikto and confirm `nikto` is available in PATH. Night Hunter then enables **RUN NIKTO**. It runs with conservative local settings and displays native output.

### Nuclei

Install Nuclei from the official ProjectDiscovery release and ensure `nuclei` is in PATH. Use only trusted templates and update them through the official tool. Night Hunter parses returned findings but coverage depends on templates installed locally.

### OpenVAS / Greenbone

OpenVAS runs through a local Greenbone service on Linux. Install Greenbone/OpenVAS and the official `gvm-tools` package, complete its initial feed/setup process, and make sure this command works first:

```bash
gvm-cli socket --xml "<get_version/>"
```

Then enable the Night Hunter connector for the current terminal:

```bash
export NIGHT_HUNTER_GVM_ENABLED=1
```

Start Night Hunter from that same terminal. When the Web Security page shows **OpenVAS / Greenbone — Available**, select your authorised target, tick the authorisation checkbox, and choose **RUN OPENVAS**.

Night Hunter creates a target and a Greenbone **Full and Fast** task, then returns the task/report IDs. Monitor scan progress and the complete report in the Greenbone UI. Greenbone credentials remain in your `gvm-tools` configuration; do not add passwords or API keys to this repository.

For a permanent environment variable on Linux, add the export line to `~/.bashrc`, then run `source ~/.bashrc`.

## 8. Troubleshooting

| Problem | What to do |
|---|---|
| Page looks old after deployment | Press `Ctrl + F5`, then wait for Render deployment to finish |
| “Local tools off” in cloud app | Expected: use a local installation for Nikto/Nuclei/OpenVAS/Nmap |
| Scanner says unavailable | Install the tool and reopen Night Hunter; check its executable is in PATH |
| OpenVAS unavailable | Confirm Greenbone is running, `gvm-cli socket --xml "<get_version/>"` works, and `NIGHT_HUNTER_GVM_ENABLED=1` is set |
| Scan fails before it starts | Enter a complete URL and tick the authorisation checkbox |
| `NightHunter: command not found` | Restart the terminal, source `~/.bashrc`, or run the path printed by the installer |

## 9. Responsible use

Never paste credentials, recovery phrases, private keys, or private customer data into a shared/public deployment. Use the local app for sensitive material. Only scan systems and data for which you have explicit permission.
