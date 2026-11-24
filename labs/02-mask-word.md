# Lab 2: Mask a Word document

**Goal:** mask a real `.docx` without breaking its layout, and see where Presidio struggles. **Time:** 10 minutes.

## Steps

1. Open `samples/complaint-escalation-report.docx` in Word. It is a two-page DemoTel complaint escalation report: customer details, a contact history, a related Saudi account, a note in Arabic, and a refund approval.

2. Mask it:

   ```bash
   uv run presidio/mask_docx.py samples/complaint-escalation-report.docx --outdir work
   ```

   The terminal lists every finding with its confidence. Two files appear in `work/`:

   | File | What it shows |
   | --- | --- |
   | `complaint-escalation-report.found.docx` | The original with everything Presidio detected **highlighted in red** |
   | `complaint-escalation-report.masked.docx` | The same document, same tables, with labels such as `<PERSON>` and `<IBAN_CODE>` |

3. Open the original and the `.found.docx` side by side.

## Questions

1. Look at every section. **What is NOT red that should be?**
2. Look at section 5, the note in Arabic. What happened there?
3. Find two places where Presidio highlighted something that is **not** personal data.
4. The IBAN appears twice, once with spaces and once without. Were both caught?

<details>
<summary>Answers</summary>

1. The customer's **Arabic name** in section 5, `خالد المنصوري`.
2. The language model reads English. On Arabic text it is guessing: it missed the real name and wrongly marked `استرداد المبلغ` ("refund of the amount") as a person. It did catch the phone number written in Arabic digits, but only at 40% confidence, right on the threshold.
3. The table labels **Email** and **Emirates** (from "Emirates ID"), and **DemoTel** in the header, were marked as a person or a place. Harmless here, but proof that it does not understand the text.
4. Yes. Presidio's IBAN check validates the number, with or without spaces.

</details>

**Takeaway:** treat Arabic free text as **red** until we add an Arabic model. Check Word documents in the `.found.docx` view: anything not highlighted was not masked.

Next: [Lab 3: Fix the misses](03-fix-the-misses.md)
