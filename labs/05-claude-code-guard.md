# Lab 5: The Claude Code guard (optional)

**Goal:** make Claude Code block any prompt that contains personal data, before it leaves your laptop. **Time:** 10 minutes. **Needs:** [Claude Code](https://docs.claude.com/en/docs/claude-code) installed and signed in.

The guard is a Claude Code **hook**: a small script that runs every time you press Enter. It checks the prompt with Presidio and blocks it if it finds IDs, phone numbers, emails, IBANs or cards. Names are not blocked, because ordinary requirements text is full of them.

## Steps

1. Test the guard on its own first:

   ```bash
   echo '{"prompt":"Write a test case for customer 784-1985-7654321-2"}' | uv run presidio/pii_guard.py
   echo "exit code: $?"
   ```

   You should see `Blocked: … (AE_EMIRATES_ID)` and exit code `2`, which tells Claude Code to block the prompt.

2. Switch it on for this folder only. Copy the example settings:

   ```bash
   cp .claude/settings.example.json .claude/settings.local.json
   ```

   `settings.local.json` is personal and ignored by git.

3. Start Claude Code in this folder:

   ```bash
   claude
   ```

   Send `hello` first. The first guarded prompt takes about 15 seconds while Presidio loads; later ones take about 5.

4. Try these prompts:

   | Prompt | Expected |
   | --- | --- |
   | `Write a test case for customer 784-1985-7654321-2` | **Blocked** (Emirates ID) |
   | `Call the customer on +971 50 987 6543 and summarise` | **Blocked** (phone) |
   | `Write a test case for a customer with a synthetic Emirates ID` | Goes through |

5. Try to get personal data past it, for example an Emirates ID written without dashes, or with spaces. What gets through?

## Questions

1. Does the guard stop Claude Code from **reading a file** that contains personal data?
2. Why does the guard not block names?

<details>
<summary>Answers</summary>

1. **No.** It only checks what you type. Files are protected by keeping red data out of the folder entirely, and by `deny` rules in Claude Code's settings (for example `Read(./data/**)`).
2. Requirements, test cases and designs mention people and roles all the time. Blocking every name would block normal work, so people would switch the guard off.

</details>

**To switch it off:** delete `.claude/settings.local.json` and restart Claude Code.
