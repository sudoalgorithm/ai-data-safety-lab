# Lab 1: Mask a text file

**Goal:** mask DemoTel's workshop notes and find what Presidio missed. **Time:** 10 minutes.

**The story:** Layla, a business analyst, has six pages of notes from a client workshop and a BRD due on Thursday. She wants to paste them into Copilot. The notes contain a customer's name, his mobile, a national ID, an IBAN and an email.

## Steps

1. Look at the raw notes first:

   ```bash
   cat samples/stakeholder-notes.md
   ```

   Find every piece of personal data yourself before Presidio does. Write them down.

2. Run the session's view:

   ```bash
   uv run presidio/show_mask.py samples/stakeholder-notes.md --out work/stakeholder-notes.masked.md
   ```

   You see three things:
   - **Before:** the notes with every finding highlighted in red.
   - **The table:** what it found, the type, how sure it is, and whether it came from Presidio or from our GCC recognisers.
   - **After:** the masked text, saved to `work/stakeholder-notes.masked.md`.

3. Compare with your list.

## Questions

1. Which items did Presidio catch that you also found?
2. **What did it miss?** Look at the start of each bullet, and at the email address.
3. Why might `crm.lead@demotel.example` be missed, when a `@gmail.com` address is caught? (Hint: look at the ending.)
4. Is the masked file safe to paste into an AI tool now? What would you fix first?

<details>
<summary>Answers</summary>

1. The customer's name, his mobile number, the Emirates ID, the IBAN, and the two names in brackets.
2. The first names **Huda** and **Omar** at the start of lines: a first name on its own, with no surname, is not recognised. And the **email** address.
3. `.example` is not a real internet domain, so the email check does not accept it. Real addresses are caught. In real work, made-up or internal formats are exactly what slip through.
4. Not yet. Fix the two first names and the email (by hand, or with a deny list in [Lab 3](03-fix-the-misses.md)), read it again, and only then use it, with approved tools.

</details>

**Takeaway:** Presidio does the boring part. You still read every line.

Next: [Lab 2: Mask a Word document](02-mask-word.md)
