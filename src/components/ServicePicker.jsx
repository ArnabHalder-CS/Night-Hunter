import {
  ArrowLeft,
  ArrowRight,
  Binary,
  FileSearch,
  Fingerprint,
  Globe2,
  KeyRound,
  LockKeyhole,
  Network,
  Radar,
  SearchCheck,
  ServerCog,
  ShieldAlert,
  ShieldCheck,
  Waypoints,
} from "lucide-react";

const serviceCatalog = {
  "Web Security": {
    icon: Globe2,
    summary: "Choose a focused web-security check for an authorized target.",
    services: [
      ["Website Intelligence", "Collect server, DNS, TLS and technology signals.", SearchCheck],
      ["Security Headers", "Review browser-facing security header coverage.", ShieldCheck],
      ["TLS Configuration", "Inspect certificate and HTTPS configuration.", LockKeyhole],
      ["Technology Discovery", "Identify publicly exposed web technologies.", Fingerprint],
      ["Cookie Review", "Check cookie security flags and attributes.", FileSearch],
      ["Endpoint Review", "Review discovered public application endpoints.", Waypoints],
    ],
  },
  "Password Security": {
    icon: LockKeyhole,
    summary: "Choose a local password-strength or cryptographic utility.",
    services: [
      ["Password Strength Audit", "Assess length, complexity and common patterns.", ShieldCheck],
      ["Secure Password Generator", "Generate a strong local password.", KeyRound],
      ["Hash Identifier", "Identify known hash formats without sending secrets.", Fingerprint],
      ["Hash Utility", "Create hashes for approved integrity workflows.", Binary],
      ["Breach-Risk Guidance", "Get local guidance for safer credential practices.", ShieldAlert],
      ["Password Report", "Create a non-sensitive security summary.", FileSearch],
    ],
  },
  "Network Security": {
    icon: Network,
    summary: "Choose a defensive network-inspection service for an authorized host.",
    services: [
      ["Host Inventory", "Nmap top-ports, service detection, OS attempt and route trace.", Radar],
      ["All TCP Ports", "Nmap TCP connect scan of ports 1–65535 with service detection.", ServerCog],
      ["Top UDP Ports", "Nmap UDP service scan of the top 100 ports; results can be indeterminate.", RadioIcon],
      ["OS Fingerprint", "Nmap fingerprint attempt; requires local Nmap and adequate responses.", Fingerprint],
      ["Service Version Scan", "Nmap service/version detection through the local app.", Globe2],
      ["Nmap Evidence Report", "View verified ports, service details and scan profile evidence.", FileSearch],
    ],
  },
  "Phishing Analyzer": {
    icon: ShieldAlert,
    summary: "Choose an approved URL or message-safety analysis workflow.",
    services: [
      ["URL Risk Analysis", "Assess a URL for phishing and impersonation signals.", SearchCheck],
      ["Brand Spoofing Check", "Review potential brand-impersonation indicators.", ShieldAlert],
      ["Domain Intelligence", "Inspect domain-level security context.", Globe2],
      ["Link Reputation Review", "Review URL signals before visiting a link.", ShieldCheck],
      ["Email Safety Triage", "Classify reported email links and sender claims.", FileSearch],
      ["Incident Summary", "Prepare a concise defensive response summary.", FileSearch],
    ],
  },
  Cryptography: {
    icon: KeyRound,
    summary: "Choose a local text transformation or integrity utility.",
    services: [
      ["Text Hashing", "Generate approved message digests locally.", Binary],
      ["Base64 Tools", "Encode or decode Base64 text.", KeyRound],
      ["Hex Tools", "Encode or decode hexadecimal text.", Binary],
      ["URL Encoding", "Encode or decode URL-safe text.", Globe2],
      ["ROT13 Utility", "Transform text with ROT13.", Waypoints],
      ["File Integrity", "Verify expected file hash values.", ShieldCheck],
    ],
  },
};

function RadioIcon(props) {
  return <Radar {...props} />;
}

export function getDefaultService(moduleName) {
  return serviceCatalog[moduleName]?.services[0]?.[0] || "Service";
}

export default function ServicePicker({ moduleName, onBack, onSelect }) {
  const category = serviceCatalog[moduleName];

  if (!category) return null;

  const CategoryIcon = category.icon;

  return (
    <section className="service-picker-page">
      <button type="button" className="service-back" onClick={onBack}>
        <ArrowLeft size={16} /> Back to modules
      </button>

      <div className="service-picker-header">
        <div className="service-picker-icon"><CategoryIcon size={28} /></div>
        <div>
          <p className="eyebrow">NIGHT HUNTER v1.6.2 · SERVICE SELECTOR</p>
          <h2>{moduleName}</h2>
          <p className="subtitle">{category.summary}</p>
        </div>
      </div>

      <div className="service-picker-note">
        <ShieldCheck size={17} />
        <span>Select a work area to continue. A workspace reports only checks it actually executes; unavailable checks remain marked unavailable. Use only with systems, data and networks you own or are authorized to assess.</span>
      </div>

      <div className="service-card-grid">
        {category.services.map(([name, description, Icon]) => (
          <article className="service-card" key={name}>
            <div className="service-card-icon"><Icon size={21} /></div>
            <div>
              <span className="service-card-kicker">DEFENSIVE SERVICE</span>
              <h3>{name}</h3>
              <p>{description}</p>
            </div>
            <button type="button" onClick={() => onSelect(name)}>
              Choose service <ArrowRight size={16} />
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
