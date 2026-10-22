import { useEffect, useState } from "react";
import {
  AlertTriangle,
  ArrowUpRight,
  Check,
  ChevronDown,
  Cpu,
  Download,
  FileText,
  Globe2,
  KeyRound,
  Laptop,
  Network,
  RefreshCw,
  ShieldCheck,
  Smartphone,
  Sparkles,
  Terminal,
  Play,
  X,
  Zap,
} from "lucide-react";
import "./LandingPage.css";

const releaseBase = "https://night-hunter-0br7.onrender.com/#downloads";

const downloads = [
  { icon: Laptop, name: "Windows Portable (.zip)", detail: "Zero warnings · Pre-bundled with start_night_hunter.bat · Extract & run", href: "/downloads/night-hunter-windows.zip", action: "Download .zip (Recommended)" },
  { icon: Laptop, name: "Windows Standalone (.exe)", detail: "Single-click executable · Launches local browser dashboard automatically", href: "/downloads/NightHunter.exe", action: "Download .exe" },
  { icon: Terminal, name: "Linux (Kali / Ubuntu / Debian / Mint)", detail: "Full Web UI Dashboard & CLI · Extract & ./run.sh or bash install.sh", href: "/downloads/night-hunter-linux.tar.gz", action: "Download for Linux (.tar.gz)" },
  { icon: Smartphone, name: "Termux (Android)", detail: "Mobile Nmap & CLI Security Recon · Extract & bash install-termux.sh", href: "/downloads/night-hunter-termux.zip", action: "Download for Termux" },
  { icon: FileText, name: "Complete Setup Guide", detail: "Step-by-step install, troubleshooting & false-positive guide", href: "https://github.com/ArnabHalder-CS/Night-Hunter/blob/main/USER_GUIDE.md", action: "View User Guide" },
];

export default function LandingPage() {
  useEffect(() => {
    document.title = "Night Hunter - Defensive Security Platform | Nighthunter";
  }, []);

  return (
    <div className="landing-root">
      <header className="landing-nav">
        <a className="landing-brand" href="#top" aria-label="Night Hunter home">
          <img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" />
          <span>NIGHT <b>HUNTER</b></span>
        </a>
        <nav>
          <a href="/app" style={{ color: "#fa37c3", fontWeight: 700 }}>Live App</a>
          <a href="#features">Platform</a>
          <a href="#downloads">Downloads</a>
          <a href="#how-it-works">How to Use</a>
        </nav>
        <a className="nav-app-link" href="/app">Launch Live App <ArrowUpRight size={15} /></a>
      </header>

      <main id="top">
        <section className="premium-hero">
          <div className="hero-orbit orbit-one" />
          <div className="hero-orbit orbit-two" />
          <div className="hero-grid-lines" />
          <div className="hero-copy">
            <p className="landing-eyebrow"><span /> DEFENSIVE SECURITY PLATFORM · V1.7.0</p>
            <h1>See the threat.<br /><em>Own the response.</em></h1>
            <p className="hero-description">A focused security workspace for authorized analysis, target device reconnaissance, and defensive auditing across your devices.</p>
            <div className="hero-actions">
              <a className="hero-primary" href="/app">Launch Live Cloud App <Play size={17} /></a>
              <a className="hero-secondary" href="#downloads">Download Offline Tool <Download size={17} /></a>
            </div>
            <div className="hero-proof">
              <span><Check size={14} /> Windows, Linux &amp; Android</span>
              <span><Check size={14} /> Built for authorized testing</span>
              <span><Check size={14} /> Nmap-style targeted recon</span>
            </div>
          </div>
          <div className="hero-mark" aria-hidden="true">
            <div className="mark-scan" />
            <img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" />
            <div className="mark-caption">NIGHT HUNTER <span>01 / DEFENSIVE OPS</span></div>
          </div>
          <p className="hero-scroll">SCROLL TO EXPLORE <ChevronDown size={15} /></p>
        </section>

        <section className="statement-section" id="features">
          <p className="landing-eyebrow"><span /> THE NIGHT HUNTER PLATFORM</p>
          <div className="statement-heading">
            <h2>One command center.<br />A clearer security picture.</h2>
            <p>Designed for people who need a refined place to inspect systems, understand findings, and act with confidence.</p>
          </div>
          <div className="feature-columns">
            <article><Globe2 /><h3>Scanner Hub &amp; Web Audit</h3><p>Built-in web audit with local orchestration for Nikto, Nuclei, and OpenVAS/GVM.</p></article>
            <article><ShieldCheck /><h3>Phishing Intelligence Lab</h3><p>Heuristic risk engine, Unicode Homoglyph &amp; Punycode lab, and email/SMS link triage.</p></article>
            <article><KeyRound /><h3>Crypto Analyst Suite</h3><p>10+ simultaneous hash digests, unknown hash format identifier, CSPRNG keys &amp; HMAC.</p></article>
            <article><Network /><h3>Nmap Network Recon</h3><p>Scan target devices on your LAN for OS models, device names, and TCP/UDP ports.</p></article>
          </div>
        </section>

        {/* WHY NIGHT HUNTER - VALUE SHOWCASE */}
        <section className="why-hunter-section">
          <div className="why-hunter-header">
            <p className="landing-eyebrow"><span /> WHY ETHICAL HACKERS &amp; SYSADMINS CHOOSE NIGHT HUNTER</p>
            <h2>Stop Juggling Broken Tools.<br /><em>Defend Your Perimeter Smarter.</em></h2>
            <p className="why-hunter-subtitle">
              Most security tools do one thing in isolation or output fake toy data. Night Hunter gives you genuine low-level reconnaissance, passive threat analysis, and zero-setup deployment.
            </p>
          </div>

          <div className="why-hunter-grid">
            <article className="why-card highlight-card">
              <div className="why-icon-wrap" style={{ color: "#fa37c3", background: "rgba(250, 55, 195, 0.12)" }}>
                <Cpu size={24} />
              </div>
              <span className="why-badge">REAL HARDWARE SCANNING</span>
              <h3>100% Real Engines — Zero Fake Mock Data</h3>
              <p>
                Unlike toy tools that display simulated progress bars, Night Hunter executes real socket operations and native <strong>Nmap 7.99</strong> commands under the hood. It accurately fingerprints exact OS versions, discovers active UDP services (<code>-sU</code>), and tests live TLS 1.3 handshakes.
              </p>
            </article>

            <article className="why-card">
              <div className="why-icon-wrap" style={{ color: "#79ffa8", background: "rgba(121, 255, 168, 0.12)" }}>
                <Zap size={24} />
              </div>
              <span className="why-badge">UNIFIED DEFENSE</span>
              <h3>Single Pane of Glass Defense</h3>
              <p>
                Quit opening 5 separate terminal windows for Nmap, CyberChef, browser devtools, and Python scripts. Audit web application headers, scan local LAN subnets, inspect phishing threats, and compute hashes from one unified cyberpunk dashboard.
              </p>
            </article>

            <article className="why-card">
              <div className="why-icon-wrap" style={{ color: "#ffd480", background: "rgba(255, 212, 128, 0.12)" }}>
                <ShieldCheck size={24} />
              </div>
              <span className="why-badge">SAFE BY DESIGN</span>
              <h3>Zero-Risk Passive Phishing Inspection</h3>
              <p>
                Investigate reported phishing links without executing malware or alerting the attacker. Night Hunter's heuristic parser flags IDN homoglyphs, deceptive redirects, and brand spoofing 100% passively without downloading remote payloads.
              </p>
            </article>

            <article className="why-card">
              <div className="why-icon-wrap" style={{ color: "#38bdf8", background: "rgba(56, 189, 248, 0.12)" }}>
                <Laptop size={24} />
              </div>
              <span className="why-badge">ZERO SETUP</span>
              <h3>True Tri-Platform Portability</h3>
              <p>
                No Python virtualenv hell or dependency conflicts. Run the portable <strong>NightHunter.exe</strong> directly on Windows with one click, run headless on Kali Linux with one terminal command, or audit on the go using Android Termux.
              </p>
            </article>

            <article className="why-card">
              <div className="why-icon-wrap" style={{ color: "#c084fc", background: "rgba(192, 132, 252, 0.12)" }}>
                <FileText size={24} />
              </div>
              <span className="why-badge">AUDIT READY</span>
              <h3>Instant Client-Ready Reports (HTML · JSON · TXT)</h3>
              <p>
                Turn technical findings into polished, visual HTML executive reports with charts, or export clean JSON for automated SIEM and CI/CD pipelines. Never write audit documentation by hand again.
              </p>
            </article>
          </div>
        </section>

        <section className="downloads-section" id="downloads">
          <div className="downloads-title">
            <p className="landing-eyebrow"><span /> LATEST STABLE RELEASE (V1.7.0)</p>
            <h2>Choose your<br /><em>environment.</em></h2>
          </div>
          <div className="download-list">
            {downloads.map(({ icon: Icon, name, detail, href, action }) => (
              <a className="download-row" href={href} key={name}>
                <span className="download-icon"><Icon size={23} /></span>
                <span><strong>{name}</strong><small>{detail}</small></span>
                <span className="download-action">{action} <ArrowUpRight size={18} /></span>
              </a>
            ))}
          </div>
        </section>



        <section className="install-section" id="how-it-works">
          <div>
            <p className="landing-eyebrow"><span /> COMPLETE USER GUIDELINE</p>
            <h2>Installation &amp;<br />Troubleshooting</h2>
            <div style={{ marginTop: '20px', padding: '16px', borderRadius: '6px', background: 'rgba(154, 85, 255, 0.1)', border: '1px solid rgba(154, 85, 255, 0.3)', color: '#d5c6e6', fontSize: '13px', lineHeight: '1.6' }}>
              <strong style={{ color: '#fff', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                <ShieldCheck size={16} color="#4ade80" /> 100% Safe &amp; Open Source
              </strong>
              Night Hunter runs entirely locally on your machine with no hidden telemetry or external tracking. All source code is publicly auditable on GitHub.
            </div>
          </div>
          <ol>
            <li>
              <b>WINDOWS</b>
              <span>
                <strong>Windows 10 / 11 Setup &amp; Browser Safety Note</strong>
                <small>• <b>Option A (Zero Warnings · Recommended):</b> Download <b>Windows Portable (.zip)</b>, extract the folder, and double-click <code>start_night_hunter.bat</code>.</small>
                <small>• <b>Option B (Single File):</b> Download <code>NightHunter.exe</code> and double-click to launch.</small>
                <small style={{ marginTop: '8px', background: 'rgba(255, 170, 0, 0.08)', padding: '10px 14px', borderRadius: '6px', borderLeft: '3px solid #ffd280', color: '#ffd280', display: 'block', lineHeight: '1.6' }}>
                  <b style={{ color: '#fff' }}>Why Chrome or Defender flags "Virus detected" / "Dangerous file":</b><br />
                  This is a standard <em>False Positive</em> common to all open-source security tools compiled with Python. Night Hunter includes low-level socket scanners and is not signed with an expensive ($500/year) Microsoft enterprise certificate.
                  <br />&bull; <b>In Google Chrome:</b> Press <kbd style={{ background: '#222', padding: '1px 5px', borderRadius: '3px', color: '#fff' }}>Ctrl + J</kbd> (Downloads) &rarr; Click <b>"Download suspicious file"</b> or <b>"Keep anyway"</b>.
                  <br />&bull; <b>In Windows SmartScreen:</b> Click <b>"More info"</b> &rarr; Click <b>"Run anyway"</b>.
                </small>
                <small style={{ color: '#dd9dff', marginTop: '6px' }}>&#10003; The local engine starts and automatically opens your dashboard at <code>http://127.0.0.1:5000</code>.</small>
              </span>
            </li>
            <li>
              <b>LINUX (KALI / UBUNTU / DEBIAN)</b>
              <span>
                <strong>Quick Start (Two Ways to Run):</strong>
                <small>• <b>Method 1 (Instant / No Install):</b> Extract archive and run: <code>tar -xzf night-hunter-linux.tar.gz &amp;&amp; cd night-hunter-linux &amp;&amp; ./run.sh</code></small>
                <small>• <b>Method 2 (System-Wide Install):</b> Run: <code>bash install.sh</code>. Installs Night Hunter globally, creates terminal command <code>NightHunter</code>, and adds a launcher icon to your Kali Application Menu!</small>
                <small style={{ color: '#7ff0ca', marginTop: '6px', display: 'block' }}>&#10003; Automatically boots the local engine and opens the graphical Web Dashboard in your browser at <code>http://127.0.0.1:5000</code>. (Add <code>--cli</code> for headless terminal mode).</small>
              </span>
            </li>
            <li>
              <b>TERMUX</b>
              <span>
                <strong>Android Setup via Termux</strong>
                <small>1. Download <code>night-hunter-termux.zip</code> on your Android device.</small>
                <small>2. In Termux, navigate to downloads: <code>cd ~/storage/downloads &amp;&amp; unzip night-hunter-termux.zip</code></small>
                <small>3. Run installer: <code>cd night-hunter-termux &amp;&amp; bash termux-install.sh</code></small>
                <small>4. Start anytime by typing: <code>NightHunter</code></small>
              </span>
            </li>
          </ol>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="landing-brand"><img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" /><span>NIGHT <b>HUNTER</b></span></div>
        <p>Defensive tooling for authorized security testing.</p>
        <a href="#downloads">Download Night Hunter v1.7.0 <Download size={15} /></a>
      </footer>
    </div>
  );
}
