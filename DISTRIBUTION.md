# Night Hunter downloads

The website Downloads page should link to these release assets:

- `NightHunter.exe` — Windows dashboard edition; it opens Night Hunter in the default browser.
- `night-hunter-linux.tar.gz` — install with `bash install.sh`, then run `NightHunter`.
- `night-hunter-termux.zip` — extract in Termux, run `bash install-termux.sh`, then run `NightHunter`.

## Build the release assets

Windows: run `build-windows-exe.bat`. The output is `dist/NightHunter.exe`.

Linux: run `bash build-linux-package.sh`. The output is `releases/night-hunter-linux.tar.gz`.

Termux archive: run `bash build-termux-package.sh`. The output is `releases/night-hunter-termux.zip`.

Upload all three outputs to a GitHub Release. Copy each direct release URL into the website Downloads page.
