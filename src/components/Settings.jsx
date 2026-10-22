import { useState } from "react";
import { Check, ChevronDown, ImagePlus, Info, Languages, Palette, RotateCcw, Settings as SettingsIcon, Sparkles } from "lucide-react";
import { applyTheme, DEFAULT_THEME, readTheme, THEME_KEY } from "../theme";

const palettes = [
  { name: "Neon Pink", hex: "#ff3bcf", values: { accent: "#ff3bcf", violet: "#8b5cf6", cyan: "#28d7ff", success: "#54f5b9" } },
  { name: "Royal Purple", hex: "#8b5cf6", values: { accent: "#8b5cf6", violet: "#6338d9", cyan: "#55b8ff", success: "#61e3b1" } },
  { name: "Cyber Blue", hex: "#06b6d4", values: { accent: "#06b6d4", violet: "#3478f6", cyan: "#4dd9ff", success: "#44e1bb" } },
  { name: "Mint Green", hex: "#22d3ae", values: { accent: "#22d3ae", violet: "#5b8bff", cyan: "#3ee5ce", success: "#7af2be" } },
  { name: "Dark Red", hex: "#ef4444", values: { accent: "#ef4444", violet: "#a53d8c", cyan: "#f58b78", success: "#ffbd70" } },
];
const languages = [["en", "English"], ["hi", "Hindi"], ["bn", "Bengali"], ["es", "Spanish"], ["fr", "French"], ["de", "German"], ["ar", "Arabic"], ["ja", "Japanese"]];

export default function Settings() {
  const [settings, setSettings] = useState(readTheme);
  const [message, setMessage] = useState("");
  function update(next) { setSettings(next); applyTheme(next); }
  function selectPalette(values) { update({ ...settings, ...values }); setMessage("Theme preview updated. Save to keep it."); }
  function chooseWallpaper(event) {
    const image = event.target.files?.[0]; if (!image) return;
    if (image.size > 1_500_000) { setMessage("Choose an image below 1.5 MB so it can be saved safely in this browser."); return; }
    const reader = new FileReader(); reader.onload = () => { update({ ...settings, wallpaper: reader.result }); setMessage("Wallpaper preview updated. Save to keep it."); }; reader.readAsDataURL(image);
  }
  function save(event) { event.preventDefault(); localStorage.setItem(THEME_KEY, JSON.stringify(settings)); setMessage("Personalization saved in this browser."); }
  function reset() { update({ ...DEFAULT_THEME }); localStorage.removeItem(THEME_KEY); setMessage("Restored the default Night Hunter theme."); }
  const selected = palettes.find((palette) => palette.values.accent === settings.accent)?.name;
  return <section className="reference-settings-page">
    <div className="reference-settings-main">
      <header className="settings-hero"><SettingsIcon size={39} /><div><h2>Settings</h2><p>Customize your experience and make Night Hunter work your way.</p></div></header>
      <form onSubmit={save} className="reference-settings-form">
        <section className="reference-settings-card"><div className="settings-card-title"><Palette /><div><h3>Four-colour theme</h3><p>Choose a quick theme, then adjust individual colours below.</p></div></div><div className="theme-presets">{palettes.map((palette) => <button className={`theme-preset ${selected === palette.name ? "selected" : ""}`} type="button" key={palette.name} onClick={() => selectPalette(palette.values)}><span className="theme-swatch" style={{ background: palette.hex }} />{selected === palette.name && <Check className="theme-check" size={16} />}<strong>{palette.name}</strong><small>{palette.hex.toUpperCase()}</small></button>)}</div><div className="fine-tune">{[["accent", "Accent"], ["violet", "Violet"], ["cyan", "Cyan"], ["success", "Success"]].map(([field, label]) => <label key={field}>{label}<input type="color" value={settings[field]} onChange={(event) => update({ ...settings, [field]: event.target.value })} /></label>)}</div></section>
        <section className="reference-settings-card"><div className="settings-card-title"><ImagePlus /><div><h3>Dashboard wallpaper</h3><p>Choose your own local image for the app background. It stays in this browser only.</p></div></div><div className="wallpaper-row"><label className="reference-wallpaper-upload"><ImagePlus size={25} /><strong>Browse image</strong><small>JPG, PNG or WEBP · Max size 1.5 MB</small><input type="file" accept="image/*" onChange={chooseWallpaper} /></label><div className={`wallpaper-preview ${settings.wallpaper ? "has-image" : ""}`} style={settings.wallpaper ? { backgroundImage: `url("${settings.wallpaper}")` } : undefined}>{!settings.wallpaper && <><Sparkles /><span>Your wallpaper preview</span></>}{settings.wallpaper && <button type="button" onClick={() => update({ ...settings, wallpaper: "" })}>Remove</button>}</div></div></section>
        <section className="reference-settings-card language-card"><div className="settings-card-title"><Languages /><div><h3>Interface language</h3><p>Choose your preferred language for the app.</p></div></div><label className="reference-select"><select value={settings.language} onChange={(event) => update({ ...settings, language: event.target.value })}>{languages.map(([code, name]) => <option value={code} key={code}>{name}</option>)}</select><ChevronDown size={17} /></label><p className="language-note"><Info size={15} />Language preference is saved. Full translations are not bundled yet, so the interface remains English.</p></section>
        <div className="reference-actions"><button className="reference-save" type="submit"><Check size={17} />SAVE PERSONALIZATION</button><button className="reference-reset" type="button" onClick={reset}><RotateCcw size={17} />RESET</button>{message && <span>{message}</span>}</div>
      </form>
    </div>
    <aside className={`reference-side-art ${settings.wallpaper ? "has-image" : ""}`} style={settings.wallpaper ? { backgroundImage: `linear-gradient(rgba(6,8,20,.42), rgba(6,8,20,.78)), url("${settings.wallpaper}")` } : undefined}><div><em>Control<br />Analyze<br />Stay Ahead</em><span>NIGHT HUNTER</span></div></aside>
  </section>;
}
