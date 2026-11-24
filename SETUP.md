# Setup

About 15 minutes, most of it the one-time download. Everything runs on your own laptop: Presidio sends nothing anywhere.

## 1. Install uv

[uv](https://docs.astral.sh/uv/) installs Python and Presidio for you. You do not need to install Python yourself.

**macOS**

```bash
brew install uv
```

No Homebrew? Use `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Windows (PowerShell)**

```powershell
winget install --id=astral-sh.uv -e
```

Or: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

**Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Close and reopen the terminal, then check:

```bash
uv --version
```

## 2. Get the lab

```bash
git clone https://github.com/sudoalgorithm/ai-data-safety-lab.git
cd ai-data-safety-lab
```

No git? On the GitHub page click **Code → Download ZIP**, unzip it, and open a terminal in that folder.

## 3. First run (downloads Presidio)

```bash
uv run presidio/mask.py samples/whatsapp-message.txt
```

The first run downloads Presidio and its English language model, **about 600 MB, 3 to 5 minutes**. Later runs take a few seconds.

You should see placeholders such as `<PERSON>`, `<SA_NATIONAL_ID>`, `<GCC_PHONE>`, `<CREDIT_CARD>` and `<EMAIL_ADDRESS>`. The last line, in Arabic, is **not** masked: that is expected, and [Lab 2](labs/02-mask-word.md) explains why.

On Windows, the commands are the same. Backslashes also work: `uv run presidio\mask.py samples\whatsapp-message.txt`

## 4. You are ready

Start [Lab 1](labs/01-mask-text.md).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `uv: command not found` | Close and reopen the terminal. On Windows, sign out and in again. |
| Download fails or times out behind the office proxy | Set the proxy first: `export HTTPS_PROXY=http://proxy:port` (macOS / Linux) or `$env:HTTPS_PROXY="http://proxy:port"` (PowerShell). Or run the first download on another network once; it is cached afterwards. |
| `No interpreter found for Python >=3.10,<3.13` | Run `uv python install 3.12`, then try again. |
| Arabic text shows as boxes in the terminal | It is a font issue in the terminal only. The files themselves are fine. Use [Lab 2](labs/02-mask-word.md) and open the Word output. |
| Very slow every time | Each command loads the language model (a few seconds). That is normal. |
| Still stuck | Ask in the programme's Teams chat, or come to office hours. |
