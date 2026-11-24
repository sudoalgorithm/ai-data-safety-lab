# Installing Presidio on a Windows laptop

Step by step, for Windows 10 and 11. About 20 minutes, most of it the one-time download. **You do not need admin rights** for uv or Presidio, and you do not need to install Python yourself.

Everything runs on your laptop. Presidio sends nothing anywhere.

## Step 1: Open PowerShell

Press **Start**, type **PowerShell**, press **Enter**. (Windows Terminal is fine too.) Do **not** choose "Run as administrator".

Make the window understand Arabic and other Unicode text. Run this once per window, or see [Make UTF-8 permanent](#make-utf-8-permanent) below:

```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = "1"
```

## Step 2: Install uv

uv downloads the right Python and Presidio for you.

**Option A: winget** (built into Windows 11 and recent Windows 10):

```powershell
winget install --id=astral-sh.uv -e
```

**Option B: if winget is blocked** on your laptop:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

This installs into your user folder (`%USERPROFILE%\.local\bin`), so no admin rights are needed.

**Close PowerShell and open a new window**, so it picks up the new command. Then check:

```powershell
uv --version
```

You should see something like `uv 0.x.y`. If you get *"uv is not recognized"*, see [Troubleshooting](#troubleshooting).

## Step 3: Get the lab

**With git** (if `git --version` works):

```powershell
cd $HOME\Documents
git clone https://github.com/sudoalgorithm/ai-data-safety-lab.git
cd ai-data-safety-lab
```

**Without git:**

1. Open https://github.com/sudoalgorithm/ai-data-safety-lab
2. Click the green **Code** button, then **Download ZIP**.
3. Right-click the ZIP in Downloads, choose **Extract All…**, and extract to `Documents`.
4. In PowerShell:

   ```powershell
   cd $HOME\Documents\ai-data-safety-lab-main
   ```

## Step 4: First run (downloads Presidio)

```powershell
uv run presidio\mask.py samples\whatsapp-message.txt
```

The first run downloads Python, Presidio and the English language model: **about 600 MB, 3 to 10 minutes** depending on the network. It is cached afterwards, and later runs take a few seconds.

**Expected result:** the names, Iqama, mobile, card and email are replaced by labels such as `<PERSON>` and `<SA_NATIONAL_ID>`. The last line, in Arabic, is **not** masked. That is expected; [Lab 2](labs/02-mask-word.md) explains why.

## Step 5: Check the other tools

```powershell
uv run presidio\show_mask.py samples\stakeholder-notes.md
uv run presidio\mask_docx.py samples\complaint-escalation-report.docx --outdir work
start work\complaint-escalation-report.found.docx
```

The last command opens the result in Word, with everything Presidio found highlighted in red.

## Step 6: Put Presidio in front of your AI tool

Installing Presidio does not protect anything by itself. Set it up so it runs **before** text reaches Copilot or Claude Code: [USE-WITH-AI-TOOLS.md](USE-WITH-AI-TOOLS.md).

The quickest habit on Windows: copy text, then run

```powershell
uv run presidio\mask_clipboard.py
```

and paste. The clipboard now holds the masked version.

## Make UTF-8 permanent

So you don't have to repeat Step 1 every time:

1. Press **Start**, type **environment variables**, open **Edit environment variables for your account**.
2. Under *User variables*, click **New…**
3. Name: `PYTHONUTF8`, Value: `1`. Click **OK**.
4. Open a new PowerShell window.

## Behind the office proxy

If the first run fails with a timeout or SSL error, set the proxy for this window (ask IT for the address):

```powershell
$env:HTTPS_PROXY = "http://proxy.example:8080"
$env:HTTP_PROXY  = "http://proxy.example:8080"
uv run presidio\mask.py samples\whatsapp-message.txt
```

If the proxy inspects SSL traffic and you see certificate errors, add:

```powershell
$env:UV_NATIVE_TLS = "true"
```

This makes uv trust the certificates installed in Windows, which usually include the company's.

Still blocked? Do the first run once on another network (home or phone hotspot). Everything is cached afterwards and works offline.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `uv is not recognized…` | Close **all** PowerShell windows and open a new one. Still failing: sign out of Windows and back in. Or run it by its full path: `& "$env:USERPROFILE\.local\bin\uv.exe" --version` |
| `running scripts is disabled on this system` | Use the exact Option B command above; `-ExecutionPolicy ByPass` applies to that one command only. |
| Arabic shows as `?????` or boxes | Run Step 1 in this window, or make UTF-8 permanent. In old *Windows PowerShell 5* consoles, install **Windows Terminal** from the Microsoft Store for proper Arabic display. The masked files are correct even if the console shows boxes. |
| `UnicodeDecodeError` or `UnicodeEncodeError` | `$env:PYTHONUTF8 = "1"`, then run again. |
| `No interpreter found for Python >=3.10,<3.13` | `uv python install 3.12`, then run again. |
| Download is very slow or stops | Proxy settings above. A partial download resumes on the next run. |
| Antivirus blocks or quarantines a file during download | Ask IT to allow `%USERPROFILE%\AppData\Local\uv` (the uv cache folder). |
| `Permission denied` writing to `work\` | You extracted the ZIP somewhere read-only, such as `C:\Program Files`. Move the folder to `Documents`. |
| Word says the file is locked | Close the `.found.docx` or `.masked.docx` in Word, then run the command again. |

Next: [Lab 1](labs/01-mask-text.md), or [put Presidio in front of your AI tool](USE-WITH-AI-TOOLS.md).
