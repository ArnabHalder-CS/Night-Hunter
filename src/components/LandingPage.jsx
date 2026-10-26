import { useEffect, useState } from "react";
import {
  ArrowUpRight,
  Check,
  Cpu,
  Download,
  FileText,
  Globe2,
  KeyRound,
  Laptop,
  Network,
  ShieldCheck,
  Smartphone,
  Terminal,
  Play,
  Zap,
  Globe,
  FileCode,
  Lock,
  Layers,
  ArrowRight
} from "lucide-react";
import "./LandingPage.css";
import PrivacyPolicy from "./PrivacyPolicy";
import TermsAndConditions from "./TermsAndConditions";

const downloads = [
  { 
    icon: Globe, 
    name: "Web Cloud Dashboard", 
    detail: "Direct browser access. No installation or dependencies required.", 
    href: "/app", 
    action: "Launch Web App" 
  },
  { 
    icon: Laptop, 
    name: "Python Local Execution (Windows, Linux, macOS)", 
    detail: "Run from clean Python 3.10+ source with standard packages. Zero false positives.", 
    href: "#how-it-works", 
    action: "View Commands" 
  },
  { 
    icon: Terminal, 
    name: "Linux Terminal Engine (Kali, Ubuntu, Debian)", 
    detail: "Headless CLI and local web server. Clone from GitHub and run directly.", 
    href: "#how-it-works", 
    action: "View Linux Setup" 
  },
  { 
    icon: Smartphone, 
    name: "Android Mobile Recon (Termux)", 
    detail: "Run portable network and domain intelligence directly inside Termux.", 
    href: "#how-it-works", 
    action: "View Termux Commands" 
  },
  { 
    icon: FileCode, 
    name: "GitHub Repository", 
    detail: "Public, auditable source code with issue tracking and releases.", 
    href: "https://github.com/ArnabHalder-CS/Night-Hunter", 
    action: "View on GitHub" 
  },
];

export default function LandingPage() {
  const [modalView, setModalView] = useState(null); // "privacy" | "terms" | "domain" | null

  useEffect(() => {
    document.title = "Night Hunter - Defensive Security Platform";
  }, []);

  return (
    <div className="landing-root">
      {/* HEADER NAVIGATION */}
      <header className="landing-nav">
        <a className="landing-brand" href="#top" aria-label="Night Hunter home">
          <img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" />
          <span>NIGHT <b>HUNTER</b></span>
        </a>
        <nav>
          <a href="/app" style={{ color: "#38bdf8", fontWeight: 600 }}>Web App</a>
          <a href="#features">Modules</a>
          <a href="#downloads">Deployment</a>
          <a href="#how-it-works">Setup</a>
          <button 
            type="button" 
            onClick={() => setModalView("domain")} 
            style={{ background: "transparent", border: "none", color: "#94a3b8", cursor: "pointer", font: "inherit", padding: 0 }}
          >
            Custom Domain
          </button>
        </nav>
        <a className="nav-app-link" href="/app">
          Launch App <ArrowUpRight size={14} />
        </a>
      </header>

      {/* MODAL VIEW OVERLAYS */}
      {modalView === "privacy" && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(9, 10, 15, 0.95)", zIndex: 100, overflowY: "auto", padding: "20px" }}>
          <PrivacyPolicy onBack={() => setModalView(null)} />
        </div>
      )}

      {modalView === "terms" && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(9, 10, 15, 0.95)", zIndex: 100, overflowY: "auto", padding: "20px" }}>
          <TermsAndConditions onBack={() => setModalView(null)} />
        </div>
      )}

      {modalView === "domain" && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(9, 10, 15, 0.95)", zIndex: 100, overflowY: "auto", padding: "40px 20px" }}>
          <div style={{ maxWidth: "700px", margin: "0 auto", background: "#12151e", border: "1px solid #232838", borderRadius: "6px", padding: "32px" }}>
            <h2 style={{ fontSize: "22px", color: "#ffffff", marginTop: 0 }}>Custom Domain Configuration</h2>
            <p style={{ color: "#94a3b8", fontSize: "14px", lineHeight: "1.6" }}>
              Night Hunter can be attached to any custom domain (e.g. <code>nighthunter.yourdomain.com</code>) via Render Cloud:
            </p>
            <ol style={{ color: "#cbd5e1", fontSize: "14px", lineHeight: "1.8", paddingLeft: "20px" }}>
              <li>Open your <strong>Render Dashboard</strong> and navigate to your <strong>night-hunter</strong> Web Service.</li>
              <li>Go to <strong>Settings</strong> &gt; <strong>Custom Domains</strong> &gt; click <strong>Add Custom Domain</strong>.</li>
              <li>Enter your domain (e.g. <code>security.yourdomain.com</code>).</li>
              <li>In your DNS provider (Cloudflare, Namecheap, Route53, GoDaddy), add a <strong>CNAME</strong> record:
                <pre style={{ background: "#1e293b", padding: "10px", borderRadius: "4px", color: "#38bdf8", overflowX: "auto" }}>
CNAME   security   night-hunter-0br7.onrender.com
                </pre>
              </li>
              <li>Render will automatically verify DNS propagation and issue a free Let's Encrypt SSL/TLS certificate.</li>
            </ol>
            <button 
              type="button" 
              onClick={() => setModalView(null)}
              style={{ marginTop: "20px", background: "#0284c7", border: "none", color: "#fff", padding: "8px 18px", borderRadius: "4px", cursor: "pointer", fontWeight: "600" }}
            >
              Close Window
            </button>
          </div>
        </div>
      )}

      <main id="top">
        {/* HERO SECTION */}
        <section className="premium-hero">
          <div className="hero-copy">
            <p className="landing-eyebrow">Defensive Security Workbench | Release 1.7</p>
            <h1>Defensive Security &amp; Systems Intelligence</h1>
            <p className="hero-description">
              An open-source security engineering platform providing domain intelligence, network speed and connectivity diagnostics, heuristic phishing triage, and cryptographic utilities.
            </p>
            <div className="hero-actions">
              <a className="hero-primary" href="/app">
                Launch Live App <Play size={14} />
              </a>
              <a className="hero-secondary" href="https://github.com/ArnabHalder-CS/Night-Hunter" target="_blank" rel="noopener noreferrer">
                View Source Code <ArrowUpRight size={14} />
              </a>
            </div>
            <div className="hero-proof">
              <span><Check size={14} /> Cross-platform: Linux, Windows, macOS</span>
              <span><Check size={14} /> Authorized diagnostics only</span>
              <span><Check size={14} /> 100% auditable open source</span>
            </div>
          </div>
          <div className="hero-mark">
            <img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" />
            <div className="mark-caption">
              NIGHT HUNTER PLATFORM
              <div style={{ color: "#38bdf8", fontSize: "10px", marginTop: "4px" }}>DEFENSIVE SYSTEMS WORKBENCH</div>
            </div>
          </div>
        </section>

        {/* CORE MODULES */}
        <section className="statement-section" id="features">
          <div className="statement-heading">
            <p className="landing-eyebrow">Security Capabilities</p>
            <h2>Integrated Security Modules</h2>
            <p>Direct diagnostics and defensive utilities without third-party tracking or bloated dependencies.</p>
          </div>
          <div className="feature-columns">
            <article>
              <Globe2 size={24} />
              <h3>Domain &amp; Tech Intelligence</h3>
              <p>DNS resolution, HTTP latency benchmarks, SSL/TLS certificate validation, server banner identification, and defensive security header audits.</p>
            </article>
            <article>
              <Network size={24} />
              <h3>Network Speed &amp; Connectivity</h3>
              <p>Host status verification, latency measurement (RTT), jitter estimation, throughput speed checks, and basic service reachability.</p>
            </article>
            <article>
              <ShieldCheck size={24} />
              <h3>Phishing Threat Intelligence</h3>
              <p>Heuristic URL evaluation, Unicode Homoglyph identification, email/SMS link triage, and actionable incident response playbooks.</p>
            </article>
            <article>
              <KeyRound size={24} />
              <h3>Cryptographic Utilities</h3>
              <p>Simultaneous generation of standard hash digests (SHA-256, SHA-512, BLAKE2b), text encoders, JWT token inspection, and CSPRNG key generation.</p>
            </article>
          </div>
        </section>

        {/* PLATFORM SPECIFICATIONS */}
        <section className="why-hunter-section">
          <div className="why-hunter-header">
            <p className="landing-eyebrow">Engineering Specifications</p>
            <h2>Built for Technical Accuracy</h2>
            <p className="why-hunter-subtitle">
              Engineered to perform direct network and protocol queries cleanly across local and cloud environments.
            </p>
          </div>

          <div className="why-hunter-grid">
            <article className="why-card">
              <span className="why-badge">REAL PROTOCOL CHECKS</span>
              <h3>Authentic System Diagnostics</h3>
              <p>
                Executes native Python socket connections, HTTP/S requests, and standard cryptographic algorithms. All metrics represent measured network responses.
              </p>
            </article>

            <article className="why-card">
              <span className="why-badge">UNIFIED INTERFACE</span>
              <h3>Centralized Defensive Console</h3>
              <p>
                Consolidates domain reconnaissance, network diagnostics, phishing link inspection, and hash verification into a single technical dashboard.
              </p>
            </article>

            <article className="why-card">
              <span className="why-badge">PASSIVE TRIAGE</span>
              <h3>Passive Phishing Analysis</h3>
              <p>
                Inspects suspicious links and messages using lexical analysis, domain structure, and brand patterns without executing remote code or alerting attackers.
              </p>
            </article>

            <article className="why-card">
              <span className="why-badge">CROSS-PLATFORM</span>
              <h3>Broad Operating System Support</h3>
              <p>
                Runs identically on Windows, Linux, and Android (Termux). The standard codebase uses cross-platform Python libraries without operating system locking.
              </p>
            </article>
          </div>
        </section>

        {/* RUN AND DEPLOYMENT OPTIONS */}
        <section className="downloads-section" id="downloads">
          <div className="downloads-title">
            <p className="landing-eyebrow">Deployment &amp; Execution</p>
            <h2>Choose Your Execution Method</h2>
          </div>
          <div className="download-list">
            {downloads.map(({ icon: Icon, name, detail, href, action }) => (
              <a className="download-row" href={href} key={name}>
                <span className="download-icon"><Icon size={20} /></span>
                <span>
                  <strong>{name}</strong>
                  <small>{detail}</small>
                </span>
                <span className="download-action">{action} <ArrowRight size={14} /></span>
              </a>
            ))}
          </div>
        </section>

        {/* HOW TO RUN INSTRUCTIONS */}
        <section className="install-section" id="how-it-works">
          <h2>Execution Instructions</h2>
          <ol>
            <li>
              <b>CLOUD ACCESS (BROWSER READY)</b>
              <span>
                <strong>Instant Online Deployment</strong>
                <small>Night Hunter is hosted as a cloud web service on Render. Click <a href="/app" style={{ color: "#38bdf8", fontWeight: "600" }}>Launch Web App</a> to begin running diagnostics immediately from any modern browser.</small>
              </span>
            </li>
            <li>
              <b>PYTHON LOCAL EXECUTION (WINDOWS, LINUX, MACOS)</b>
              <span>
                <strong>Run Locally from Clean Source</strong>
                <small>1. Clone repository: <code>git clone https://github.com/ArnabHalder-CS/Night-Hunter.git</code></small>
                <small>2. Navigate into folder: <code>cd Night-Hunter</code></small>
                <small>3. Install dependencies: <code>pip install -r requirement.txt</code></small>
                <small>4. Start server: <code>python main.py</code></small>
                <small>Opens your web dashboard at: <code>http://127.0.0.1:5000</code></small>
              </span>
            </li>
            <li>
              <b>ANDROID RECON (TERMUX)</b>
              <span>
                <strong>Run via Terminal on Android</strong>
                <small>1. Install requirements in Termux: <code>pkg update && pkg install git python</code></small>
                <small>2. Clone repository: <code>git clone https://github.com/ArnabHalder-CS/Night-Hunter.git</code></small>
                <small>3. Launch: <code>cd Night-Hunter && python main.py</code></small>
              </span>
            </li>
          </ol>
        </section>
      </main>

      {/* FOOTER */}
      <footer className="landing-footer">
        <div>
          <span>Night Hunter Defensive Security Platform</span>
          <p style={{ margin: "4px 0 0 0", color: "#64748b", fontSize: "12px" }}>
            Open-source defensive tooling for authorized security diagnostics.
          </p>
        </div>
        <div className="footer-links">
          <button type="button" onClick={() => setModalView("privacy")}>Privacy Policy</button>
          <button type="button" onClick={() => setModalView("terms")}>Terms and Conditions</button>
          <button type="button" onClick={() => setModalView("domain")}>Custom Domain</button>
          <a href="https://github.com/ArnabHalder-CS/Night-Hunter" target="_blank" rel="noopener noreferrer">GitHub</a>
        </div>
      </footer>
    </div>
  );
}
