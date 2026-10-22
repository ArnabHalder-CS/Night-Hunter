export const THEME_KEY = "night-hunter-settings";
export const DEFAULT_THEME = {
  accent: "#ff3bcf",
  violet: "#8b5cf6",
  cyan: "#27d6ff",
  success: "#54f5b9",
  wallpaper: "",
  language: "en",
};

export function readTheme() {
  try { return { ...DEFAULT_THEME, ...JSON.parse(localStorage.getItem(THEME_KEY) || "{}") }; }
  catch { return { ...DEFAULT_THEME }; }
}

export function applyTheme(settings) {
  const root = document.documentElement;
  root.style.setProperty("--nh-accent", settings.accent);
  root.style.setProperty("--nh-violet", settings.violet);
  root.style.setProperty("--nh-cyan", settings.cyan);
  root.style.setProperty("--nh-success", settings.success);
  root.style.setProperty("--nh-wallpaper", settings.wallpaper ? `url("${settings.wallpaper}")` : "none");
  root.lang = settings.language || "en";
  window.dispatchEvent(new CustomEvent("night-hunter-language", { detail: settings.language || "en" }));
}
