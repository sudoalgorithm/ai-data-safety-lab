# Lab 3: Fix the misses

**Goal:** make Presidio catch what it missed in Labs 1 and 2, and understand the threshold. **Time:** 15 minutes.

## Part A: a deny list

A deny list is a file of names or words that must **always** be masked. It is the quickest fix for names the model does not recognise: first names on their own, Arabic names, project code names, a client's own staff.

1. Create `work/my-names.txt` with one name per line:

   ```text
   # first names the model missed in Lab 1
   Huda
   Omar
   # Arabic names it cannot read (Lab 2)
   خالد
   المنصوري
   ```

2. Run Lab 1 again with the list:

   ```bash
   uv run presidio/show_mask.py samples/stakeholder-notes.md --deny work/my-names.txt
   ```

   Are `Huda` and `Omar` now masked everywhere?

3. Run Lab 2 again with the list:

   ```bash
   uv run presidio/mask_docx.py samples/complaint-escalation-report.docx --outdir work --deny work/my-names.txt
   ```

   Open the new `.found.docx`. Is the Arabic name red now?

## Part B: the threshold

Every finding has a confidence score. Only findings **above the threshold** are masked. Our scripts use **0.4** (40%).

1. Try a stricter threshold, which masks less:

   ```bash
   uv run presidio/show_mask.py samples/whatsapp-message.txt --threshold 0.7
   ```

   Which items disappeared from the table?

2. Try a looser one, which masks more:

   ```bash
   uv run presidio/show_mask.py samples/whatsapp-message.txt --threshold 0.2
   ```

   Did anything new appear? Is it really personal data?

3. Context words matter. Compare these two:

   ```bash
   echo "Order 28412345678 shipped" > work/a.txt
   echo "Customer QID 28412345678" > work/b.txt
   uv run presidio/show_mask.py work/a.txt
   uv run presidio/show_mask.py work/b.txt
   ```

   Why is the same number masked in one file and not the other?

<details>
<summary>Answers</summary>

- **Part A:** yes. The deny list catches `Huda`, `Omar` and the Arabic name. It is a blunt tool: it masks the word everywhere, even when it is not a person. Keep one list per project and review it.
- **Part B.1:** at 0.7, items scored below 70% drop out, for example the Saudi ID and Qatar QID (65%) and the `+974` number (40%). They stay in the text. That is the danger of a strict threshold.
- **Part B.2:** on this short sample, nothing new appears. On longer documents, try `mask_docx.py` with `--threshold 0.2`: more borderline guesses appear, and some are false alarms.
- **Part B.3:** an 11-digit number on its own scores only 30% as a Qatar ID, below the threshold, so it is not masked. The word **QID** next to it raises the score to 65%, so it is. Our GCC recognisers use context words like *QID*, *Iqama*, *civil* and *mobile* for exactly this reason: plain digit patterns would otherwise mask every order number. (Context words must be single words: Presidio compares them one token at a time.)

</details>

**Takeaway:** 0.4 is a balance between missing data and masking too much. Fix known gaps with a deny list, and keep reading the result.

Next: [Lab 4: Which colour?](04-which-colour.md)
