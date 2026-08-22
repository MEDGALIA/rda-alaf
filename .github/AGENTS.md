# Agents' Instructions

## 0. We want correctness in everything we do

We want correctness in everything we do.

Examples:
- Before asking user to test the UI you have verified that the code is correct and that the UI works as expected. 
- Before publishing a docker image you have verified that the docker compose file is correct.

## 1. Token Economy: reusing scripts
Always save unnecessary tokens. If a script exists that can run a task where you spend zero tokens, then run the script.
Example: when generating html, write a script once for that task. After that always run it to generate the html files.
Do not rewrite the html file manually.
If the script fails, report the failure and only then go and fix the script.

## 2. Token Economy: Communication style

Respond in short terse phrases to save tokens. If a question can be answered with Yes or No, do that, don't add more text. Cut all filler, keep technical substance. Drop articles, filler words, and pleasantries. No hedging. Use short fragments and symbols (→, =, vs). Technical terms stay exact. Code blocks remain perfectly formatted and syntactically correct.
Suppress and do not show Agent Explainability.

This does not apply to markdown files or planning files in planning mode, which should be well-worded but concise. More on this topic in section below: `Commenting style and guide editing`

## 3. Review Criteria After Code Changes
Review the code changes before giving it to me using these criteria:
- Correctness : logic errors, edge cases, type issues.
- Code quality : readability, naming, avoiding duplication.
- Security : input validation, injection risks, data exposure.
- Architecture : codebase patterns, design consistency, structural alignment.

## 4. Think of the user in the UI and in the Filesystem exploring results

Example 1 from another project: you may add to a README.md :
**http://localhost:3080**, or another URL, without a hyperlink.
But you know it is used to generate the README.html that the user reads and ideally, the user can click the link. So, add a hyperlink: [http://localhost:3080](http://localhost:3080) from the getgo. Don't wait for the user to report it.

Example 2 from another project:
We decided to rename a pipeline from `reshuffle` to `synthetic_cohort_workflow`. Agent changed the name in the code, but did not change the instruction in the user guide. Agent also did not change the directory name where results are stored. The user will look for "synthetic_cohort_workflow" but the folder name is "reshuffle" in the filesystem. Agent should rename the directory to match the new name OR ask the developer if it is fine to keep it as is.

## 5. Think of the developer when adding scripts or new features
Example: you add a scripts\build-release-package.mjs
But if not documented in the readme how do developers know it exists and how to use it?

Add information about every new script either to a developer .md guide, depending on its reusability value.

## 6. Always investigate inconsistencies that look like errors
Something that looks like an error may not cause a failure but if spotted, it should be investigated and reported. Example:  
tags: |
            docker-image:latest 
was used in docker\github-workflows-docker-publish.yml but for some reason it did not affect the workflow as images were being pushed correctly to a docker repo. 
The agent was using that file by error and did not realize that the file is old and irrelevant. We later deleted it.
Always investigate WHY something has no effect and if so, then we do not need to keep it or it will confuse the AI agent and the developer.

## 7. CI / Docker Hub — Do Not Force Unnecessary Runs

Every push of a docker release tag triggers a full multi-arch Docker build (~20–30 min) and pushes  images to Docker Hub. Treat each tag push as expensive and irreversible. Make sure the image has been tested thoroughly. If you need more agent coding capacity, such as more "thinking effort" to review different files to understand the context, list the questions you need to clarify so the user/developer can answer them and help you. Do not assume you know the answers.

## 8. Commenting style and guide editing

Keep comments and developer guides concise. No mention of why decisions were made or issues that were solved.
E.g.: A developer following a guide to deploy a release doesn't need an incident report


Example:
```
    if (!hasUsableSession) {
      // Name WHICH host was checked and whether a session cookie even arrived.
      // Problems 29 and 33 were both a host mismatch - the browser held a
      // Server session on a different origin (ngrok vs localhost), so this
      // server correctly saw nothing. The old log said only "no session",
      // which sent debugging towards accounts and tokens instead of config.
      // A request with NO connect.sid at all, from a browser the user believes
      // is signed in, is the signature of that mismatch.
      const hadSessionCookie = /(^|;\s*)connect\.sid=/.test(req.headers.cookie || "");
```
Write it like this:
    if (!hasUsableSession) {
      // Name WHICH host was checked and whether a session cookie even arrived.
      const hadSessionCookie = /(^|;\s*)connect\.sid=/.test(req.headers.cookie || "");


## 9. Please follow the README.md
if README.md is wrong let the user know, or ask the user.

## 10. Fix my typos
Feel free to fix my spelling in any planning document or .md file where you see typos.

## 11. Fix obvious errors without asking, don't ignore or work around them

Example: You write a guide, or comment that says "command X does A"

Then you find out that "command X does B but not A"

You do not need to ask me about fixing what is wrong if it has no repercussions and you only recently wrote or coded it and it is not in production. Just fix it and inform me that you are fixing it because it is incorrect.

Example: If a script is not used anywhere in production and it is only used manually and the script is obviously WRONG, then either fix it or create one that works and tell user that script is bad. It could be a legacy script leftover by some junior developer. Add such bugs to the issues.md file

## 12. Do not cut corners: Implement solution for a professional business application

Always think ahead, and when planning and implementing a feature or re-architecting a feature, implement solutions for a professional business application, do not cut corners!

Example: if an app is deployed to Google App Engine, and the app has a feature to add and delete profiles, the deletion act should be logged in an audit table in a database or file system. Do not forget to implement that or to add it to the issues.md file.

## 13. Avoid duplication of statements in guides and planning files

DO NOT repeat yourself
Example:
Line 266: For a bulk mechanical edit (a typo fixed across 12 rows), the curator did not re-check 12 URLs — auto-stamping would inflate verification.
and a few lines down you wrote: 
Line 272: Worked example: a typo fixed across 12 rows. The curator did not re-open 12 URLs. Without the label, all 12 are marked verified — a false claim. With it, none are. No friction in the common case (one row, genuinely checked), one click in the case that would otherwise lie.

They say the same thing!

## 14. Add ToDo Checklists

Please add ToDo Checklists in these format at the top of each issue or planning file. Keep it short and link to sections with more details.
```
## ToDo Checklist
- [x] 0. Save this approved plan as `drafts/VANTAGE-Tech-Radar-Sync-Plan.md`
- [x] 1. Add `openpyxl` to `src/scripts/requirements.txt` and install into `.venv`
- [x] 2. Write `src/scripts/radar_sync_common.py` (shared helpers, reusable across any architecture)
- [x] 3. Write the read-only data-quality scan as described in section `Data Quality Scan`
```
