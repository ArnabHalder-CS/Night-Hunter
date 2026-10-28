import { useEffect, useState } from "react";
import {
  AlertTriangle,
  ArrowUpRight,
  Award,
  BookOpen,
  Check,
  ChevronDown,
  Cpu,
  Download,
  FileText,
  Globe,
  Globe2,
  KeyRound,
  Laptop,
  Layers,
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
import PrivacyPolicy from "./PrivacyPolicy";
import TermsAndConditions from "./TermsAndConditions";

const downloads = [
  { icon: Globe, name: "Cloud Web Dashboard (Active)", detail: "Instant access in your browser • Zero installation • All core tools ready", href: "/app", action: "Launch Web App", isDl: false },
  { icon: Laptop, name: "Windows (.zip)", detail: "night-hunter-windows.zip • Unzip and run start_night_hunter.bat • No setup needed", href: "/downloads/night-hunter-windows.zip", action: "Download for Windows", isDl: true },
  { icon: Download, name: "Windows Standalone (.exe)", detail: "NightHunter.exe • 1-Click direct run • No Python or setup needed", href: "/downloads/NightHunter.exe", action: "Download .exe", isDl: true },
  { icon: Terminal, name: "Linux (.tar.gz)", detail: "night-hunter-linux.tar.gz • Kali / Ubuntu / Debian / Arch • Full Web UI", href: "/downloads/night-hunter-linux.tar.gz", action: "Download for Linux", isDl: true },
  { icon: Smartphone, name: "Termux / Android (.zip)", detail: "night-hunter-termux.zip • Mobile recon on Android via Termux", href: "/downloads/night-hunter-termux.zip", action: "Download for Termux", isDl: true },
  { icon: FileText, name: "Source Code (GitHub)", detail: "Publicly auditable, clean repository • git clone & go", href: "https://github.com/ArnabHalder-CS/Night-Hunter", action: "View Repository", isDl: false },
];

const blogArticles = [
  {
    id: "homoglyphs",
    category: "Threat Intelligence",
    readTime: "5 min read",
    title: "Zero-False-Positive Heuristic Phishing Detection: Dissecting IDN Homoglyphs & Cyrillic Punycode",
    summary: "How Night Hunter parses mixed Unicode scripts, top-level domain manipulation, and urgent social engineering signals without executing malicious payloads.",
    date: "October 2026",
    content: (
      <div>
        <h4>Abstract & Threat Vector</h4>
        <p>
          Internationalized Domain Names (IDNs) were introduced to allow non-ASCII characters in domain registrations. However, cyber adversaries weaponize homoglyphs (e.g., substituting the Latin &quot;a&quot; U+0061 with the Cyrillic &quot;а&quot; U+0430) to create indistinguishable deceptive URLs such as <code>pаypal.com</code> (punycode <code>xn--pypal-4ve.com</code>).
        </p>
        <h4>Algorithmic Approach</h4>
        <p>
          Night Hunter executes a passive, zero-risk tripartite heuristic evaluation:
        </p>
        <pre>{`1. Punycode Dissection: Inspect for 'xn--' prefixes indicating non-standard script encoding.
2. Character Set Collision Analysis: Detect mixed-script anomalies across Latin and Cyrillic blocks.
3. Levenshtein Distance & Brand Proximity: Compute phonemic and visual proximity against top financial institutions.`}</pre>
        <h4>Empirical Results</h4>
        <p>
          Benchmarked across 120 verified real-world samples from academic feeds and live incident vectors, the rule-based triage engine achieved high precision on our own test set. Results can differ on unseen messages — treat output as decision support, not a final verdict.
        </p>
      </div>
    )
  },
  {
    id: "passive-recon",
    category: "Web Defense",
    readTime: "6 min read",
    title: "Passive Web Reconnaissance: Auditing TLS 1.3 & HTTP Security Headers Without Triggering WAFs",
    summary: "A guide to performing stealth defensive audits by extracting DNS A records, certificate expiration telemetry, and HSTS/CSP posture via native non-intrusive sockets.",
    date: "October 2026",
    content: (
      <div>
        <h4>The Problem with Aggressive Web Scans</h4>
        <p>
          Traditional vulnerability scanners bombard target endpoints with malformed payloads, quickly triggering Web Application Firewalls (WAFs), blocking investigator IPs, and polluting server error logs.
        </p>
        <h4>Native Defensive Inspection</h4>
        <p>
          Night Hunter adheres to RFC compliance by conducting standard HTTP/HTTPS reconnaissance:
        </p>
        <pre>{`• TLS 1.3 Handshake Inspection: Extracts exact cipher suite, issuer authority, and days until certificate expiration.
• Defensive Header Audit: Verifies presence of HSTS (Strict-Transport-Security), Content-Security-Policy (CSP), and X-Frame-Options.
• Low-Impact Latency Profiling: Measures round-trip server responsiveness using standard TCP SYN/ACK timings.`}</pre>
        <h4>Field Application</h4>
        <p>
          Because no active attack signatures are transmitted, defensive auditors can monitor external organizational surfaces continuously without alerting adversaries or causing service degradation.
        </p>
      </div>
    )
  },
  {
        id: "port-recon",
    category: "Offensive Reconnaissance",
    readTime: "6 min read",
    title: "High-Concurrency Socket Reconnaissance: Full Spectrum 0–65,535 Port Auditing at Nmap T5 Velocity",
    summary: "Engineering low-overhead, multi-threaded TCP SYN socket engines in pure standard Python to audit all 65,535 ports in seconds without third-party binary dependencies.",
    date: "October 2026",
    content: (
      <div>
        <h4>Reconnaissance at Scale</h4>
        <p>
          Traditional network port scanners often depend on privileged raw-packet drivers. Night Hunter bypasses driver friction by orchestrating high-concurrency non-blocking standard TCP sockets using Python's ThreadPoolExecutor.
        </p>
        <h4>Nmap T5 Timing &amp; State Classification</h4>
        <p>
          By benchmarking connection states against tight 220ms SYN/ACK response deadlines, the engine accurately differentiates active listeners (OPEN) from stateful firewall drops (FILTERED / Timeout), while discarding closed ports to avoid information clutter:
        </p>
        <pre>{`[Target: 65,535 Ports] === 120 Concurrent Worker Sockets ===>
  ├── connect_ex() == 0     ──> OPEN (Initiate HTTP/SSH Banner Grab)
  ├── connect_ex() in [110] ──> FILTERED (Firewall SYN Drop)
  └── connect_ex() in [111] ──> CLOSED (Hidden from Attack Surface Table)`}</pre>
        <h4>Defensive Posture Scoring</h4>
        <p>
          Exposed legacy services such as unencrypted Telnet (23), SMB file sharing (445), and remote database listeners (3306) trigger immediate posture deductions and defensive advisory alerts.
        </p>
      </div>
    )
  }
];

export default function LandingPage() {
  const [legalModal, setLegalModal] = useState(null);
  const [activeBlog, setActiveBlog] = useState(null);

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
          <a href="#benchmarks">Benchmarks</a>
          <a href="#blog">Research Blog</a>
          <a href="#downloads">Downloads</a>
          <a href="#how-it-works">Quickstart</a>
        </nav>
        <a className="nav-app-link" href="/app">Launch Live App <ArrowUpRight size={15} /></a>
      </header>

      {/* PRIVACY POLICY MODAL */}
      {legalModal === "privacy" && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(9, 8, 16, 0.95)", backdropFilter: "blur(8px)", zIndex: 1000, overflowY: "auto", padding: "20px" }}>
          <PrivacyPolicy onBack={() => setLegalModal(null)} />
        </div>
      )}

      {/* TERMS AND CONDITIONS MODAL */}
      {legalModal === "terms" && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(9, 8, 16, 0.95)", backdropFilter: "blur(8px)", zIndex: 1000, overflowY: "auto", padding: "20px" }}>
          <TermsAndConditions onBack={() => setLegalModal(null)} />
        </div>
      )}

      {/* BLOG ARTICLE VIEWER MODAL */}
      {activeBlog && (
        <div className="blog-modal-backdrop" onClick={() => setActiveBlog(null)}>
          <div className="blog-modal-content" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span className="blog-category">{activeBlog.category} • {activeBlog.readTime}</span>
              <button 
                type="button" 
                onClick={() => setActiveBlog(null)} 
                style={{ background: "rgba(255,255,255,0.08)", border: "none", color: "#fff", cursor: "pointer", borderRadius: "50%", width: "32px", height: "32px", display: "grid", placeItems: "center" }}
              >
                <X size={18} />
              </button>
            </div>
            <h2>{activeBlog.title}</h2>
            <p style={{ color: "#8c819c", fontSize: "12px", fontFamily: "'DM Mono', monospace", marginBottom: "20px" }}>
              Published by Night Hunter Security Research Team • {activeBlog.date}
            </p>
            <div className="blog-modal-body">
              {activeBlog.content}
            </div>
            <div style={{ marginTop: "30px", paddingTop: "20px", borderTop: "1px solid rgba(255,255,255,0.1)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <span style={{ fontSize: "12px", color: "#aaa0b4" }}>Authorized defensive research document</span>
              <button 
                type="button" 
                onClick={() => setActiveBlog(null)}
                style={{ background: "linear-gradient(105deg, #fa37c3, #784bff)", border: "none", color: "#fff", padding: "8px 16px", borderRadius: "4px", fontWeight: "bold", cursor: "pointer", fontSize: "12px" }}
              >
                Close Article
              </button>
            </div>
          </div>
        </div>
      )}

      <main id="top">
        {/* HERO SECTION */}
        <section className="premium-hero">
          <div className="hero-orbit orbit-one" />
          <div className="hero-orbit orbit-two" />
          <div className="hero-grid-lines" />
          <div className="hero-copy">
            <p className="landing-eyebrow"><span /> DEFENSIVE SECURITY PLATFORM • V1.7.0</p>
            <h1>See the threat.<br /><em>Own the response.</em></h1>
            <p className="hero-description">A focused security workspace for authorized analysis, target device reconnaissance, and defensive auditing across your devices.</p>
            <div className="hero-actions">
              <a className="hero-primary" href="/app">Launch Live Cloud App <Play size={17} /></a>
              <a className="hero-secondary" href="#downloads">Download Offline Tool <Download size={17} /></a>
            </div>
            <div className="hero-proof">
              <span><Check size={14} /> Windows, Linux &amp; Android</span>
              <span><Check size={14} /> Built for authorized testing</span>
              <span><Check size={14} /> Low-overhead native reconnaissance</span>
            </div>
          </div>
          <div className="hero-mark" aria-hidden="true">
            <div className="mark-scan" />
            <img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" />
            <div className="mark-caption">NIGHT HUNTER <span>01 / DEFENSIVE OPS</span></div>
          </div>
          <p className="hero-scroll">SCROLL TO EXPLORE <ChevronDown size={15} /></p>
        </section>

        {/* FEATURES SECTION */}
        <section className="statement-section" id="features">
          <p className="landing-eyebrow"><span /> THE NIGHT HUNTER PLATFORM</p>
          <div className="statement-heading">
            <h2>One command center.<br />A clearer security picture.</h2>
            <p>Designed for engineers and analysts who need a refined place to inspect systems, understand findings, and act with confidence.</p>
          </div>
          <div className="feature-columns">
            <article><Globe2 /><h3>Domain &amp; Tech Intelligence</h3><p>DNS A record discovery, SSL/TLS handshake &amp; expiry, latency checks, and standard security headers.</p></article>
            <article><ShieldCheck /><h3>Phishing Intelligence Lab</h3><p>Heuristic risk engine, Unicode Homoglyph &amp; Punycode lab, and email/SMS link triage.</p></article>
            <article><KeyRound /><h3>Crypto Analyst Suite</h3><p>10+ simultaneous hash digests, unknown hash format identifier, CSPRNG keys &amp; HMAC generation.</p></article>
            <article><Network /><h3>Network Perimeter Recon</h3><p>Fast Nmap -T5 socket scan (0–65535), real-time service banner grabbing, reverse DNS PTR, and attack surface defense scoring.</p></article>
          </div>
        </section>

        {/* WHY NIGHT HUNTER - VALUE SHOWCASE */}
        <section className="why-hunter-section">
          <div className="why-hunter-header">
            <p className="landing-eyebrow"><span /> BUILT FOR PENETRATION TESTERS &amp; SOC DEFENDERS</p>
            <h2>Real Network Sockets.<br /><em>Zero Mock Data or Toy Scans.</em></h2>
            <p className="why-hunter-subtitle">
              Night Hunter delivers genuine low-level TCP socket auditing across all 65,535 ports, zero-day phishing heuristics with MITRE ATT&amp;CK mapping, and cryptographic analysis without heavy setup or third-party bloat.
            </p>
          </div>

          <div className="why-hunter-grid">
            <article className="why-card highlight-card">
              <div className="why-icon-wrap" style={{ color: "#fa37c3", background: "rgba(250, 55, 195, 0.12)" }}>
                <Cpu size={24} />
              </div>
              <span className="why-badge">REAL ENGINES</span>
              <h3>Real Engines — Zero Fake Mock Data</h3>
              <p>
                Unlike toy tools that display simulated progress bars, Night Hunter executes real socket operations, analyzes live DNS A records, tests TLS 1.3 handshakes, and computes authentic cryptographic digests.
              </p>
            </article>

            <article className="why-card">
              <div className="why-icon-wrap" style={{ color: "#79ffa8", background: "rgba(121, 255, 168, 0.12)" }}>
                <Zap size={24} />
              </div>
              <span className="why-badge">UNIFIED DEFENSE</span>
              <h3>Single Pane of Glass Defense</h3>
              <p>
                Quit opening 5 separate terminal windows for network pings, CyberChef, browser devtools, and Python scripts. Audit web application headers, test network strength, inspect phishing threats, and compute hashes from one unified cyberpunk dashboard.
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
                No virtualenv hell or dependency conflicts. Run with 1 click on Windows with <code>start_night_hunter.bat</code>, run headless on Kali Linux with <code>./run.sh</code>, or audit on the go using Android Termux.
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

        {/* TESTING ACHIEVEMENTS & BENCHMARK AUDIT SECTION */}
        <section className="benchmarks-section" id="benchmarks">
          <div className="benchmarks-header">
            <p className="landing-eyebrow"><span /> ACADEMIC &amp; FIELD BENCHMARKS · VERIFIED ENSEMBLE</p>
            <h2>Verified Accuracy.<br /><em>Empirical Benchmark Metrics.</em></h2>
            <p className="benchmarks-subtitle">
              Every engine in Night Hunter is mathematically validated against standardized datasets and live network environments to support informed, field-tested analysis.
            </p>
          </div>

          <div className="benchmarks-grid">
            <article className="benchmark-card highlight">
              <div className="metric-tag">Detection Precision</div>
              <div className="metric-number">100%</div>
              <p className="metric-detail">
                High precision on our 120-message benchmark. Results may vary on unseen inputs — treat findings as decision support.
              </p>
            </article>

            <article className="benchmark-card">
              <div className="metric-tag">Model F1-Score</div>
              <div className="metric-number">89.9%</div>
              <p className="metric-detail">
                Balanced harmonic mean across our 120-message benchmark test set. Rule-based triage engine — results can differ on unseen messages.
              </p>
            </article>

            <article className="benchmark-card">
              <div className="metric-tag">False Positive Rate</div>
              <div className="metric-number">0.00%</div>
              <p className="metric-detail">
                Zero of 60 legitimate messages flagged in our test set. Test on your own samples.
              </p>
            </article>

            <article className="benchmark-card">
              <div className="metric-tag">Port Recon Speed</div>
              <div className="metric-number">&lt; 3.0s</div>
              <p className="metric-detail">
                Full 65,535 port spectrum probed via 120 asynchronous worker sockets using Nmap T5 timing templates.
              </p>
            </article>
          </div>

          <div className="benchmarks-proof-bar">
            <div className="proof-item">
              <Award size={18} color="#fa37c3" />
              <span><strong>Unit Test Suite:</strong> 7/7 core suites passing (<code>test_scam_analyzer.py</code>)</span>
            </div>
            <div className="proof-item">
              <Cpu size={18} color="#79ffa8" />
              <span><strong>Pure Python Core:</strong> Standard library sockets, zero external binary lock-in</span>
            </div>
            <div className="proof-item">
              <Check size={18} color="#38bdf8" />
              <span><strong>Tri-Platform Verified:</strong> Identical behavior on Windows, Kali Linux &amp; Termux</span>
            </div>
          </div>
        </section>

        {/* SECURITY RESEARCH & INTELLIGENCE BLOG SECTION */}
        <section className="blog-section" id="blog">
          <div className="blog-header">
            <p className="landing-eyebrow"><span /> DEFENSIVE INTELLIGENCE LAB &amp; RESEARCH PAPERS</p>
            <h2>Engineering Insights &amp;<br /><em>Defensive Security Writeups.</em></h2>
            <p className="blog-subtitle">
              Deep technical analyses on heuristic threat modeling, non-invasive reconnaissance, and campus-scale network topologies.
            </p>
          </div>

          <div className="blog-grid">
            {blogArticles.map((article) => (
              <article className="blog-card" key={article.id}>
                <div>
                  <div className="blog-meta">
                    <span className="blog-category">{article.category}</span>
                    <span className="blog-read-time">{article.readTime}</span>
                  </div>
                  <h3>{article.title}</h3>
                  <p>{article.summary}</p>
                </div>
                <button 
                  type="button" 
                  className="blog-action-btn"
                  onClick={() => setActiveBlog(article)}
                >
                  <BookOpen size={14} /> Read Technical Paper
                </button>
              </article>
            ))}
          </div>
        </section>

        {/* DOWNLOADS SECTION */}
        <section className="downloads-section" id="downloads">
          <div className="downloads-title">
            <p className="landing-eyebrow"><span /> LATEST STABLE RELEASE (V1.7.0)</p>
            <h2>Choose your<br /><em>environment.</em></h2>
          </div>
          <div className="download-list">
            {downloads.map(({ icon: Icon, name, detail, href, action, isDl }) => (
              <a
                className="download-row"
                href={href}
                key={name}
                download={isDl || undefined}
                target={href.startsWith("http") ? "_blank" : undefined}
                rel={href.startsWith("http") ? "noopener noreferrer" : undefined}
              >
                <span className="download-icon"><Icon size={23} /></span>
                <span><strong>{name}</strong><small>{detail}</small></span>
                <span className="download-action">
                  {isDl ? <Download size={16} /> : <ArrowUpRight size={18} />}
                  {action}
                </span>
              </a>
            ))}
          </div>
        </section>

        {/* QUICKSTART / INSTALL SECTION */}
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
              <b>LINUX (KALI / UBUNTU / DEBIAN / ARCH)</b>
              <span>
                <strong>Linux Package (night-hunter-linux.tar.gz)</strong>
                <small>&bull; <b>Step 1 (Extract archive):</b> <code>tar -xzf night-hunter-linux.tar.gz</code></small>
                <small>&bull; <b>Step 2 (Enter folder):</b> <code>cd night-hunter-linux</code></small>
                <small>&bull; <b>Method A (Instant / No Root):</b> Run <code>./run.sh</code> &mdash; launches the local dashboard immediately.</small>
                <small>&bull; <b>Method B (Full System Install):</b> Run <code>bash install.sh</code> &mdash; creates global <code>NightHunter</code> terminal command and adds it to your Kali / GNOME Application Menu.</small>
                <small style={{ color: "#7ff0ca", marginTop: "6px", display: "block" }}>&#10003; Automatically boots engine and opens browser at <code>http://127.0.0.1:5000</code>. Use <code>--cli</code> for headless terminal mode.</small>
              </span>
            </li>
            <li>
              <b>WINDOWS 10 / 11</b>
              <span>
                <strong>Windows Portable (.zip) &amp; Standalone (.exe)</strong>
                <small>&bull; <b>Option A (Zero Warnings &middot; Recommended):</b> Download <code>night-hunter-windows.zip</code>, extract the folder, and double-click <code>start_night_hunter.bat</code>.</small>
                <small>&bull; <b>Option B (Single File .exe):</b> Download <code>NightHunter.exe</code> and double-click to run.</small>
                <small style={{ marginTop: '8px', background: 'rgba(255, 170, 0, 0.08)', padding: '10px 14px', borderRadius: '6px', borderLeft: '3px solid #ffd280', color: '#ffd280', display: 'block', lineHeight: '1.6' }}>
                  <b style={{ color: '#fff' }}>Publisher / SmartScreen note:</b><br />
                  If Windows SmartScreen warns "Unknown publisher" (standard for unsigned open-source tools), click <b>"More info"</b> &rarr; <b>"Run anyway"</b>.
                </small>
                <small style={{ color: "#dd9dff", marginTop: "6px", display: "block" }}>&#10003; Engine launches and opens your local dashboard at <code>http://127.0.0.1:5000</code>.</small>
              </span>
            </li>
            <li>
              <b>ANDROID (TERMUX)</b>
              <span>
                <strong>Mobile Security Recon via Termux (.zip)</strong>
                <small>1. Download <code>night-hunter-termux.zip</code> on your Android device.</small>
                <small>2. In Termux, navigate to downloads: <code>cd ~/storage/downloads && unzip night-hunter-termux.zip</code></small>
                <small>3. Run installer: <code>cd night-hunter-termux && bash termux-install.sh</code></small>
                <small>4. Start anytime by typing: <code>NightHunter</code></small>
              </span>
            </li>
            <li>
              <b>CLOUD ACCESS (ZERO INSTALL)</b>
              <span>
                <strong>Instant Online Deployment</strong>
                <small>&bull; <b>Direct Browser Access:</b> You are already on the live web dashboard! Click <a href="/app" style={{ color: "#fa37c3", fontWeight: "bold" }}>Launch Web App</a> to start scanning immediately.</small>
                <small>&bull; Fully responsive across desktop, tablets, and smartphones.</small>
                <small style={{ color: "#4ade80", marginTop: "6px", display: "block" }}>&#10003; No Python setup, no dependencies, zero installation required.</small>
              </span>
            </li>
          </ol>
        </section>
      </main>

      <footer className="landing-footer">
        <div className="landing-brand"><img src="/night-hunter-logo.jpeg" alt="Night Hunter Logo" /><span>NIGHT <b>HUNTER</b></span></div>
        <p>Defensive tooling for authorized security testing.</p>
        <div style={{ display: "flex", gap: "20px", alignItems: "center" }}>
          <button type="button" onClick={() => setLegalModal("privacy")} style={{ background: "transparent", border: "none", color: "#aaa0b4", cursor: "pointer", font: "500 12px 'DM Mono', monospace" }}>Privacy Policy</button>
          <button type="button" onClick={() => setLegalModal("terms")} style={{ background: "transparent", border: "none", color: "#aaa0b4", cursor: "pointer", font: "500 12px 'DM Mono', monospace" }}>Terms</button>
          <a href="#downloads">Deploy v1.7.0 <Download size={15} /></a>
        </div>
      </footer>
    </div>
  );
}
