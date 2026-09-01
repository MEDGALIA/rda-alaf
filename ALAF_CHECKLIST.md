# ALAF Readiness Checklist

A self-assessment for an organization preparing to give AI agents access to its data.

**How to use it**: one person answers on behalf of the organization, before any agent is granted data access. 

Every item is a **blocker, not a warning:** a `No` means the organization is not ready for that agent, not that it should proceed carefully.

The items follow the order they must be done in: lock down access → clean the data → set the rules → screen at runtime → gate the actions → keep the record → close the outbound path.

---

## (1) Remediate Oversharing

**Question**: Before granting access, have you audited and tightened permissions across **every** mechanism that can grant access to the data the agent will reach?

- [ ] Yes
- [ ] No

**Explanation**: The first step in any AI rollout, and the one Microsoft puts first in its own guidance for Copilot. It means checking who can reach your sensitive data, and cutting off access that shouldn't be there, before the agent can read any of it.

"Permissions" is broader than ACLs and IAM. See [Appendix A](#appendix-a-access-granting-mechanisms-to-audit) for the mechanisms to audit.


---

## (2) Deidentify Data Before Agent Access

**Question**: Have you run a deidentification process over the data the agent will access or ensured it is deidentified?

- [ ] Yes
- [ ] No

**Explanation**: Deidentification finds sensitive information in your data and removes or hides it before agents can reach it. [Microsoft Presidio](https://microsoft.github.io/presidio/) is a widely recommended open-source tool for this.

Run this over the data you already have, before granting access, and again as new data arrives. Item (4) covers what this misses: data that shows up later, or comes from somewhere this run never looked.

---

## (3) Agent Manifesto

**Question**: Have you written an agent manifesto that agents must read before any task involving new data?

- [ ] Yes
- [ ] No

**Explanation**: Put the rules governing your agents in a markdown file, conventionally `AGENTS.md`, and require agents to read it before each new task that touches new data, or more often as needed.

The manifesto must contain your data governance rules and be written in concise, unambiguous language that both humans and agents can follow. Prefer explicit prohibitions ("never write to X") over general principles ("be careful with X"): an agent acts on what a rule literally says, not on what it was meant to convey.

---

## (4) Runtime PII Screening as an Agent Tool

**Question**: Does the agent check every new data source for personal information *before* reading it, and write what it finds somewhere the agent itself cannot read?

- [ ] Yes
- [ ] No

**Explanation**: This check sits between the agent and the data, and runs on every new source, even data already cleaned under item (2). Item (2) covers the data you knew about; this catches what shows up later, or from somewhere you didn't expect.

**The findings must go somewhere the agent cannot read**, for a person to review. An agent that can read its own findings can also repeat, summarize, or act on the very personal information it just flagged, which defeats the point of checking. An agent only reacts with `stop`, if PII found, or `continue`, if PII free.

---

## (5) Human Approval Gate

**Question**: Must a named human approve every consequential agent action before it takes effect, and is that gate impossible for the agent to bypass?

- [ ] Yes
- [ ] No

**Explanation**: Decide what counts as "consequential" before you deploy, not after something goes wrong. It usually includes: changing real data, deleting anything, sending messages outside the organization, spending money, and changing the agent's own permissions or rules.

Two things are required, and the second is the one usually missed:

1. A **named** person is accountable, not "someone on the team".
2. The agent **cannot get around the gate**. It must not be able to approve its own work, turn the gate off, or edit the rules that decide what needs approval.

---

## (6) Provenance and Reversibility

**Question**: For any agent action, can you reconstruct what changed, when, and on whose authority, and undo it?

- [ ] Yes
- [ ] No

**Explanation**: Two separate things, both needed:

- **A record** of what the agent did, which data it touched, and who approved it. It must be clear which changes came from an agent and which came from a person.
- **A way to undo it.** A record that tells you exactly how you were harmed, with no way to reverse it, is an incident report, not a safeguard.

Keeping your data in version control (Git) gives you both: every change is saved with who made it and when, and any earlier version can be restored.

---

## (7) Zero Data Retention

**Question**: If you use a third-party AI API, have you configured it for zero data retention and checked the prompt caching TTL?

- [ ] Yes
- [ ] No

**Explanation**: By default, most providers retain API inputs and outputs for a period (commonly 30 days) for abuse monitoring. Zero data retention turns that off, so your prompts and the data in them are not stored on their servers. It usually has to be requested and approved per account, not just toggled on.

Prompt caching is separate and easy to miss. It stores part of your prompt on the provider's side to make repeat calls cheaper and faster, with its own time-to-live. Zero data retention does not necessarily switch it off, so a cache TTL can keep your data on their servers after you believed retention was disabled. Check both.

This applies to whatever the agent sends, which is why it belongs after items (2) and (4): anything they failed to remove leaves your control the moment it is sent.

---

## Scoring

| Result | Meaning |
|---|---|
| All `Yes` | Ready to give the agent access to your data, with the safeguards above in place. |
| Any `No` | Not ready. Fix the gap before granting access. Watching closely is not a substitute. |

Items (1) and (2) must come first. Once an agent has read data that was left open or uncleaned, it has already read it, and taking the access away afterwards does not undo that.

---

## Appendix A: Glossary of Terms

### Access-granting mechanisms to audit

Referenced from item (1). Check every way access can be granted, including ways that never show up in your main user directory:

| Way access is granted | Examples |
|---|---|
| Roles and groups | Entra ID, Okta, AWS IAM, including access people get through a group inside another group |
| File and folder permissions | SharePoint, OneDrive, Google Drive, S3, network shares |
| **Sharing links** | "Anyone with the link", public links, temporary download links |
| Database permissions | Database roles, and rules limiting access to certain rows or columns |
| Permissions inside an app | Roles set inside a tool that aren't connected to your main user directory |
| Machine logins | API keys, service accounts, tokens, connection strings |
| Access nobody removed | People who left, unused groups, forgotten guest or external accounts |

**Pay particular attention to sharing links.** They give access without changing a file's permissions, so a check that looks only at permissions will report a document as properly restricted while an "anyone with the link" URL makes it readable to whoever has that link. This is one of the most common ways data gets overshared, and the easiest to miss.

**The underlying problem**: an agent can reach whatever the person using it can reach. If a folder of strategy documents, health records, or personal data was left open by mistake, the agent will find it and show it to them, even data they were never meant to see. Files that sat unnoticed for years because nobody clicked that deep may be unprotected.