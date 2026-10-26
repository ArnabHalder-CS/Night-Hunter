import { useEffect, useState } from "react";



import {

  LayoutDashboard,

  Globe,

  LockKeyhole,

  Network,

  ShieldAlert,

  KeyRound,

  FileText,

  Settings,

  Bell,

  Activity,

  Terminal,

  ArrowUpRight,

  ChevronRight,

  Play,

  RotateCcw,

  Sparkles,

  AlertTriangle,

  Download,

  RefreshCw,

  Zap,

  X,

  Check,

} from "lucide-react";



import "./App.css";

import WebSecurity from "./components/WebSecurity";

import PasswordSecurity from "./components/PasswordSecurity";

import NetworkSecurity from "./components/NetworkSecurity";

import NmapWorkspace from "./components/NmapWorkspace";

import PhishingAnalyzer from "./components/PhishingAnalyzer";

import Cryptography from "./components/Cryptography";

import Reports from "./components/Reports";

import SettingsPage from "./components/Settings";

// ServicePicker removed - direct module workspace access

import { applyTheme, readTheme } from "./theme";



const translations = {

  en: { dashboard:"Dashboard", web:"Web Security", password:"Password Security", network:"Network Perimeter Recon", phishing:"Phishing Analyzer", crypto:"Cryptography", reports:"Reports", settings:"Settings", modules:"SECURITY MODULES", preferences:"Preferences", online:"SYSTEM ONLINE", welcome:"Welcome back", mission:"Your security. Our mission.", monitor:"LIVE THREAT MONITOR", activity:"Recent Activity", securityModules:"Security Modules", launch:"Launch" },

  hi: { dashboard:"डैशबोर्ड", web:"वेब सुरक्षा", password:"पासवर्ड सुरक्षा", network:"नेटवर्क स्पीड एवं क्षमता", phishing:"फ़िशिंग विश्लेषक", crypto:"क्रिप्टोग्राफी", reports:"रिपोर्ट", settings:"सेटिंग्स", modules:"सुरक्षा मॉड्यूल", preferences:"पसंद", online:"सिस्टम ऑनलाइन", welcome:"वापसी पर स्वागत है", mission:"आपकी सुरक्षा। हमारा मिशन।", monitor:"लाइव थ्रेट मॉनिटर", activity:"हाल की गतिविधि", securityModules:"सुरक्षा मॉड्यूल", launch:"खोलें" },

  bn: { dashboard:"ড্যাশবোর্ড", web:"ওয়েব সিকিউরিটি", password:"পাসওয়ার্ড সিকিউরিটি", network:"নেটওয়ার্ক স্পিড ও স্ট্রেংথ", phishing:"ফিশিং বিশ্লেষক", crypto:"ক্রিপ্টোগ্রাফি", reports:"রিপোর্ট", settings:"সেটিংস", modules:"সিকিউরিটি মডিউল", preferences:"পছন্দ", online:"সিস্টেম অনলাইন", welcome:"ফিরে আসার জন্য স্বাগতম", mission:"আপনার নিরাপত্তা। আমাদের লক্ষ্য।", monitor:"লাইভ থ্রেট মনিটর", activity:"সাম্প্রতিক কার্যকলাপ", securityModules:"সিকিউরিটি মডিউল", launch:"চালু করুন" },

  es: { dashboard:"Panel", web:"Seguridad web", password:"Seguridad de contraseña", network:"Seguridad de red", phishing:"Analizador de phishing", crypto:"Criptografía", reports:"Historial", settings:"Ajustes", modules:"MÓDULOS DE SEGURIDAD", preferences:"Preferencias", online:"SISTEMA EN LÍNEA", welcome:"Bienvenido de nuevo", mission:"Tu seguridad. Nuestra misión.", monitor:"MONITOR DE AMENAZAS", activity:"Actividad reciente", securityModules:"Módulos de seguridad", launch:"Abrir" },

};





const isLocal =

  typeof window !== "undefined" &&

  (window.location.hostname === "localhost" ||

   window.location.hostname === "127.0.0.1" ||

   window.location.hostname === "0.0.0.0");





function App() {



  const [activePage, setActivePage] = useState("Dashboard");

  const [language, setLanguage] = useState(() => readTheme().language || "en");

  const [terminalLines, setTerminalLines] = useState([

    "[+] NIGHT HUNTER core initialized.",

    "[+] Security modules loaded.",

    "[+] Report engine loaded.",

    "[+] System ready."

  ]);

  const [showNotifications, setShowNotifications] = useState(false);

  const [hasUnreadNotification, setHasUnreadNotification] = useState(false);



  useEffect(() => {

    applyTheme(readTheme());

    const updateLanguage = (event) => setLanguage(event.detail || "en");

    window.addEventListener("night-hunter-language", updateLanguage);

    return () => window.removeEventListener("night-hunter-language", updateLanguage);

  }, []);



  const t = translations[language] || translations.en;





  const modules = [

    {

      name: "Phishing Analyzer",
      label: t.phishing,
      description: "Heuristic Risk Scoring | Homoglyph Detection | Link Triage",

      icon: ShieldAlert,

    },

    {

      name: "Cryptography",
      label: t.crypto,
      description: "Multi-Hash Engine | Format Identifier | CSPRNG Keys",

      icon: KeyRound,

    },

    {

      name: "Web Security",
      label: t.web,
      description: "Domain Intelligence | DNS | SSL/TLS | Server Technology",

      icon: Globe,

    },

    {

      name: "Network Security",
      label: t.network,
      description: "Gateway Recon | Outbound Firewall Audit | Network Posture Score",

      icon: Network,

    },

    {

      name: "Password Security",

      label: t.password,

      description: "Local Entropy · Breach Prevention · Generator",

      icon: LockKeyhole,

    },

    {

      name: "Reports",

      label: t.reports,

      description: "Audit Logs · XML/JSON · Report Engine",

      icon: FileText,

    },

  ];





  function openPage(page) {

    setActivePage(page);

    setTerminalLines((oldLines) => [

      ...oldLines,

      `[>] Navigated to ${page}.`,

      `[+] Operational environment ready.`

    ]);

  }





  function launchModule(moduleName) {

    setActivePage(moduleName);

    setTerminalLines((oldLines) => [

      ...oldLines,

      `[>] Launching ${moduleName} workspace...`,

      `[+] Operational environment ready.`

    ]);

  }





  function resetDashboard() {

    setActivePage("Dashboard");



    setTerminalLines([

      "[+] NIGHT HUNTER core initialized.",

      "[+] Security modules loaded.",

      "[+] Report engine loaded.",

      "[+] System ready."

    ]);

  }



  function renderPageContent() {



    if (activePage === "Dashboard") {

      return <Dashboard />;

    }

    if (activePage === "Phishing Analyzer") {

      return <PhishingAnalyzer />;

    }

    if (activePage === "Cryptography") {

      return <Cryptography />;

    }

    if (activePage === "Web Security") {

      return <WebSecurity />;

    }

    if (activePage === "Network Security") {

      return <NetworkSecurity />;

    }

    if (activePage === "Password Security") {

      return <PasswordSecurity />;

    }

    if (activePage === "Reports") {

      return <Reports />;

    }

    if (activePage === "Settings") {

      return <SettingsPage />;

    }





    const selectedModule = modules.find(

      (module) => module.name === activePage

    );





    if (selectedModule) {



      const Icon = selectedModule.icon;



      return (

        <div className="module-page">



          <div className="module-page-header">



            <div>



              <p className="eyebrow">

                NIGHT HUNTER SECURITY MODULE

              </p>



              <h2>

                {selectedModule.name}

              </h2>



              <p className="subtitle">

                {selectedModule.description}

              </p>



            </div>



            <div className="large-module-icon">

              <Icon size={38} />

            </div>



          </div>





          <div className="module-action-grid">



            <div className="action-panel">



              <div className="action-icon">

                <Play size={20} />

              </div>



              <h3>

                Start Module

              </h3>



              <p>

                Launch the {selectedModule.name} engine from the NIGHT HUNTER interface.

              </p>



              <button

                className="primary-action"

                onClick={() => {

                  setTerminalLines((oldLines) => [

                    ...oldLines,

                    `[>] ${selectedModule.name} started.`,

                    `[+] Waiting for target input...`

                  ]);

                }}

              >

                Start

                <ArrowUpRight size={16} />

              </button>



            </div>





            <div className="action-panel">



              <div className="action-icon blue">

                <Terminal size={20} />

              </div>



              <h3>

                Module Terminal

              </h3>



              <p>

                View module activity and backend execution output.

              </p>



              <button

                className="secondary-action"

                onClick={() => {

                  setTerminalLines((oldLines) => [

                    ...oldLines,

                    `[+] ${selectedModule.name} terminal opened.`

                  ]);

                }}

              >

                Open Terminal

              </button>



            </div>





            <div className="action-panel">



              <div className="action-icon pink">

                <FileText size={20} />

              </div>



              <h3>

                Reports

              </h3>



              <p>

                Security reports generated by this module will appear here.

              </p>



              <button

                className="secondary-action"

                onClick={() => openPage("Reports")}

              >

                View Reports

              </button>



            </div>



          </div>





          <div className="module-terminal">



            <div className="panel-header">



              <div>

                <span className="panel-kicker">

                  MODULE CONSOLE

                </span>



                <h3>

                  {selectedModule.name}

                </h3>

              </div>



              <Activity size={18} />



            </div>



            <div className="terminal-body">



              {terminalLines.slice(-8).map((line, index) => (

                <p key={`${line}-${index}`}>

                  {line}

                </p>

              ))}



              <p className="terminal-cursor">

                _

              </p>



            </div>



          </div>





          <button

            className="back-button"

            onClick={resetDashboard}

          >

            <ChevronRight size={16} />

            Back to Dashboard

          </button>



        </div>

      );

    }





    return null;

  }





  function Dashboard() {



    return (

      <section className="dashboard">



        <div className="welcome-row">



          <div>



            <p className="eyebrow">

              SECURITY OPERATIONS CENTER

            </p>



            <h2>

              {t.welcome},{" "}

              <span>Night Hunter</span>

            </h2>



            <p className="subtitle">

              {t.mission}

            </p>



          </div>



          <div className="version">

            NIGHT HUNTER <strong>v1.6.2</strong>

          </div>



        </div>





        <div className="stats-grid">



          <div className="stat-card">

            <span>MODULES</span>

            <strong>6</strong>

            <small>Security modules</small>

          </div>



          <div className="stat-card">

            <span>TOOLS</span>

            <strong>ON DEMAND</strong>

            <small>Service workspaces</small>

          </div>



          <div className="stat-card">

            <span>FINDINGS</span>

            <strong>PER SCAN</strong>

            <small>Measured findings only</small>

          </div>



          <div className="stat-card">

            <span>STATUS</span>

            <strong className="online-text">

              ONLINE

            </strong>

            <small>Core engine active</small>

          </div>



        </div>





        <div className="hero-grid">



          <div className="threat-visual">



            <div className="visual-label">

              <Activity size={16} />

              {t.monitor}

            </div>



            <div className="dashboard-logo-display">

              <img src="/night-hunter-logo.jpeg" alt="Night Hunter logo" />

              <span>DEFENSIVE SECURITY PLATFORM</span>

            </div>



            <div className="visual-footer">

              <span>

                TARGET ANALYSIS

              </span>



              <strong>

                SECURITY ENGINE ACTIVE

              </strong>

            </div>



          </div>





          <div className="threat-feed">



            <div className="panel-header">



              <div>

                <span className="panel-kicker">

                  SYSTEM READINESS

                </span>



                <h3>

                  Runtime status

                </h3>

              </div>



              <span className="live-badge">

                LOCAL

              </span>



            </div>





            <div className="feed-item">



              <span className="feed-dot pink"></span>



              <div>

                <strong>

                  Workspace ready

                </strong>



                <small>

                  Choose a service to begin

                </small>

              </div>



              <time>

                now

              </time>



            </div>





            <div className="feed-item">



              <span className="feed-dot blue"></span>



              <div>

                <strong>

                  Evidence-first reporting

                </strong>



                <small>

                  Results are created only after a completed check

                </small>

              </div>



              <time>

                now

              </time>



            </div>





            <div className="feed-item">



              <span className="feed-dot violet"></span>



              <div>

                <strong>

                  Capability-aware results

                </strong>



                <small>

                  Unavailable checks are shown instead of inferred

                </small>

              </div>



              <time>

                now

              </time>



            </div>



          </div>



        </div>





        <div className="section-heading">



          <div>



            <p className="eyebrow">

              NIGHT HUNTER ENGINE

            </p>



            <h3>

              {t.securityModules}

            </h3>



          </div>



          <button

            className="view-button"

            onClick={() => openPage("Web Security")}

          >

            Open Web Security

            <ArrowUpRight size={16} />

          </button>



        </div>





        <div className="module-grid">



          {modules.map((module) => {



            const Icon = module.icon;



            return (

              <div

                className="module-card"

                key={module.name}

              >



                <div className="module-icon">

                  <Icon size={23} />

                </div>



                <h3>

                  {module.label}

                </h3>



                <p>

                  {module.description}

                </p>



                <button

                  className="launch-button"

                  onClick={() => launchModule(module.name)}

                >

                  {t.launch}

                  <ArrowUpRight size={16} />

                </button>



              </div>

            );



          })}



        </div>





        <div className="bottom-grid">





          <div className="terminal-panel">



            <div className="panel-header">



              <div>



                <span className="panel-kicker">

                  TERMINAL

                </span>



                <h3>

                  NIGHT HUNTER CLI

                </h3>



              </div>



              <Terminal size={18} />



            </div>





            <div className="terminal-body">



              {terminalLines.slice(-8).map((line, index) => (

                <p key={`${line}-${index}`}>

                  {line}

                </p>

              ))}



              <p className="terminal-cursor">

                _

              </p>



            </div>



          </div>





        </div>



      </section>

    );

  }





  return (

    <div className="night-hunter">

      <header className="app-header">

        <button className="header-brand" type="button" onClick={resetDashboard}>

          <img className="header-logo-image" src="/night-hunter-logo.jpeg" alt="Night Hunter" />

          <span><strong>NIGHT <b>HUNTER</b></strong><small>SCAN&nbsp;&nbsp;/&nbsp;&nbsp;ANALYZE&nbsp;&nbsp;/&nbsp;&nbsp;DEFEND</small></span>

        </button>

        <div className="header-actions">

          <div className="system-status">

            <span></span>

            {isLocal ? "LOCAL ENGINE" : "CLOUD SERVER ONLINE"}

          </div>

          <a href="/landing" className="nav-site-link">Website &amp; Docs</a>



          {/* NOTIFICATION BELL */}

          <div className="notification-bell-container">

            <button

              className={`icon-button ${hasUnreadNotification ? "has-unread-notif" : ""}`}

              onClick={() => {

                setShowNotifications((prev) => !prev);

                setHasUnreadNotification(false);

              }}

              aria-label="System Notifications"

              title="System Notifications"

            >

              <Bell size={19} />

              {hasUnreadNotification && <span className="notification-pulse-dot" />}

            </button>



            {showNotifications && (

              <div className="notification-dropdown-panel" role="region" aria-label="Notifications list">

                <div className="notif-dropdown-header">

                  <div className="notif-header-title">

                    <Bell size={15} color="#fa37c3" />

                    <strong>SYSTEM NOTIFICATIONS</strong>

                  </div>

                  <button

                    className="notif-close-btn"

                    onClick={() => setShowNotifications(false)}

                    aria-label="Close"

                  >

                    <X size={15} />

                  </button>

                </div>



                <div className="notif-dropdown-body">

                  <div className="notif-card-update">

                    <div className="notif-badge-row">

                      <span className="notif-pill" style={{ background: "rgba(34, 197, 94, 0.15)", color: "#4ade80", borderColor: "rgba(34, 197, 94, 0.4)" }}>

                        <Check size={11} /> SYSTEM OPERATIONAL (v1.7.0)

                      </span>

                      <span className="notif-time-tag">Active</span>

                    </div>



                    <h4>Night Hunter Defensive Engine v1.7.0</h4>

                    <p className="notif-description">

                      {isLocal

                        ? "Running locally with complete device scanning and network hardware access. All security modules are fully operational."

                        : "Night Hunter v1.7.0 is running on the public dashboard. The installed application runs all local scanning features on the user's device."}

                    </p>



                    <div className="notif-changelog">

                      <p><strong>Active capabilities:</strong></p>

                      <ul>

                        <li><strong>🎯 Local Nmap Recon:</strong> OS and MAC data are shown only when locally measured.</li>

                        <li><strong>📡 UDP Inspection:</strong> Unavailable or indeterminate UDP checks are never counted as open services.</li>

                        <li><strong>🛡️ Passive Link Analysis:</strong> The hosted analyzer assesses URL signals without opening the destination page.</li>

                        <li><strong>⚠️ Evidence labels:</strong> Measured, heuristic, and unavailable capabilities are clearly separated.</li>

                      </ul>

                    </div>



                    <div className="notif-actions">

                      {isLocal ? (

                        <a

                          href="https://night-hunter-0br7.onrender.com/app"

                          className="notif-btn-switch-server"

                          onClick={() => setShowNotifications(false)}

                        >

                          <Zap size={14} /> Open Live Cloud Dashboard &rarr;

                        </a>

                      ) : (

                        <a

                          href="/landing#downloads"

                          className="notif-btn-download"

                        >

                          <Download size={13} /> Offline Packages (v1.7.0)

                        </a>

                      )}

                    </div>

                  </div>

                </div>

              </div>

            )}

          </div>



          <button className="icon-button" onClick={() => openPage("Settings")} aria-label="Open settings"><Settings size={19} /></button>

        </div>

      </header>

      <div className="app-workspace">





      {/* SIDEBAR */}



      <aside className="sidebar">



        <nav className="navigation">



          <div className="nav-section-title">

            MAIN

          </div>





          <button

            className={`nav-item ${

              activePage === "Dashboard"

                ? "active"

                : ""

            }`}

            onClick={() => openPage("Dashboard")}

          >



            <LayoutDashboard size={19} />



            <span>

              {t.dashboard}

            </span>



          </button>





          <div className="nav-section-title">

            {t.modules}

          </div>





          {modules.map((module) => {



            const Icon = module.icon;



            return (

              <button

                className={`nav-item ${

                  activePage === module.name

                    ? "active"

                    : ""

                }`}

                key={module.name}

                onClick={() => openPage(module.name)}

              >



                <Icon size={19} />



                <div>



                  <span>

                    {module.label}

                  </span>



                  <small>

                    {module.description}

                  </small>



                </div>



              </button>

            );



          })}





          <button

            className={`nav-item ${

              activePage === "Settings"

                ? "active"

                : ""

            }`}

            onClick={() => openPage("Settings")}

          >



            <Settings size={19} />



            <div>



              <span>

                {t.settings}

              </span>



              <small>

                {t.preferences}

              </small>



            </div>



          </button>



        </nav>





        <div className="sidebar-footer">



          <div className="footer-status">



            <span className="status-dot"></span>



            SYSTEM ONLINE



          </div>



          <p>

            Night Hunter v1.6.2

          </p>



        </div>



      </aside>





      {/* MAIN */}



      <main className="main-content">





        {renderPageContent()}



      </main>



      </div>

    </div>

  );

}





export default App;

