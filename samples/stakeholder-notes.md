# Stakeholder workshop notes (unmasked, synthetic)

> **Synthetic data for the masking exercise.** Every name and number below is invented. In real work, notes like these are 🔴 red until masked. Use this file to practise: follow [Lab 1](../labs/01-mask-text.md).

**Date:** Sunday, workshop 1. **Attendees:** Customer-care director (Huda Al-Rashid), call-centre supervisor (Omar Saeed), compliance officer, IT CRM lead, FPT BA.

- Huda: the biggest pain is repeat calls. A customer, e.g. Khalid Nasser on +971 50 987 6543, called five times about the same billing error last month and each agent started from scratch.
- Omar: agents need to see every previous complaint for the customer on one screen when the call comes in. Today they search the CRM by mobile number and then check a shared Excel file.
- Omar: complaint categories today are billing, network, device, sales, and "other". "Other" is 30% of everything, so the categories are not useful.
- Compliance: the regulator report needs counts by category, channel, and resolution time, plus every complaint over 15 working days with the reason. Today it takes two people three days each month to compile.
- Compliance: we must not show the full national ID on screen; last four digits only. Example in the old system: 784-1985-7654321-2 displayed in full, which was an audit finding.
- IT: the CRM has an API but it is rate-limited to 50 requests per second. The SMS gateway is shared with marketing.
- Huda: customers should get an SMS with a reference number when the complaint is logged and when it is resolved. Arabic by default, English if the customer's profile says so.
- Omar: supervisors want an alert when a complaint is 2 working days from breaching the SLA.
- Disagreement: Huda wants social-media complaints in phase 1; IT says the social team's tool has no API. Not decided.
- Action: IT CRM lead to confirm whether the CRM can store a complaint reference (email: crm.lead@demotel.example).
- Refund example raised: refunds above 500 QAR need supervisor approval; customer IBAN QA58DOHB00001234567890ABCDEFG was quoted on the call in full, which should not happen.
