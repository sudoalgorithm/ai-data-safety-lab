# Lab 4: Which colour?

**Goal:** classify material before you use AI on it. **Time:** 10 minutes. No commands, just thinking. Do it in pairs if you can.

| Colour | Means | You may |
| --- | --- | --- |
| 🟢 **Green** | FPT internal, public, or synthetic | Use AI freely, standard settings |
| 🟡 **Amber** | Client material **without** personal data, and the contract and client allow AI outside the country | Mask, check, use approved tools with amber settings |
| 🔴 **Red** | Personal data, secrets, classified data, or anything that must stay in the country | No cloud AI. Local or in-country model, or no AI |

When unsure, take the higher colour and ask your delivery manager.

## Classify these

1. An FPT BRD template
2. A client's Spring Boot service, no personal data, and the contract allows AI processing outside the country
3. A production log file from a client system
4. A screenshot of the client's mobile app showing real customers' names
5. A test plan you wrote for the DemoTel practice project
6. A client's source code, and the contract says nothing about AI
7. The masked version of Layla's notes from Lab 1, before you fixed the missed names
8. A Terraform state file from a client's production environment
9. A client's architecture diagram with no IP addresses or credentials, AI allowed by contract
10. A spreadsheet of staff salaries for a project budget

<details>
<summary>Answers</summary>

1. 🟢 Green: FPT's own material.
2. 🟡 Amber: client material, no personal data, AI allowed. Remove secrets, use approved settings.
3. 🔴 Red: logs contain customer data, IDs and often tokens.
4. 🔴 Red: real people. Use synthetic data in the design instead.
5. 🟢 Green: synthetic.
6. 🔴 Red until the delivery manager confirms. **Silence in a contract is not permission.** This is the most common real case.
7. 🔴 Red: two names and an email were still in it. Masked is not the same as safe until you have read it.
8. 🔴 Red: state files contain secrets and resource details.
9. 🟡 Amber.
10. 🔴 Red: salaries are personal data.

</details>

Next: [Lab 5: The Claude Code guard](05-claude-code-guard.md) (optional, for Claude Code users)
