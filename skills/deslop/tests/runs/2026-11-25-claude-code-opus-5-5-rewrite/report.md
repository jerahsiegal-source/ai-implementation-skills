# deslop run: 2026-11-25

Runner: claude, model: default.

| | deslop | plain Claude |
|---|---|---|
| AI samples: score before | 48.74 | 48.74 |
| AI samples: score after | 80.89 | 68.58 |
| AI samples: high hits left | 0 | 2 |
| Human samples: score after | None | None |
| Human samples: similarity to original | None | None |
| Rewrites that broke a number, URL or code | 0 | 2 |
| Numbers invented | 0 | 1 |
| Numbers lost | 0 | 5 |
| [NEEDS SPECIFIC] markers, AI samples | 18 | 0 |
| [NEEDS SPECIFIC] markers, human samples | 0 | 0 |
| Tokens per run (mean) | 177400.32 | 40660.89 |
| Seconds per run (mean) | 22.22 | 9.07 |

| Sample | Context | Before | deslop | plain | Similarity (deslop) | Markers | Pass 2 similarity |
|---|---|---|---|---|---|---|---|
| a01-resume-pm | resume | 2 | 2 | 3 | 0.762 | 0 | - |
| a02-resume-data | resume | 57 | 100 | 40 | 0.682 | 3 | - |
| a03-email-coverletter-ux | email | 33 | 88 | 88 | 0.622 | 2 | - |
| a04-social-launch | social | 38 | 100 | 62 | 0.721 | 0 | - |
| a05-social-lesson | social | 73 | 100 | 100 | 0.962 | 1 | - |
| a06-report-support-q3 | report | 92 | 100 | 100 | 0.5 | 0 | - |
| a07-report-billing-status | report | 85 | 85 | 69 | 0.763 | 1 | - |
| a08-email-kickoff-followup | email | 2 | 20 | 14 | 0.579 | 0 | - |
| a09-email-dashboard-delay | email | 79 | 79 | 79 | 0.663 | 0 | - |
| a10-docs-tidycsv-readme | docs | 100 | 100 | 100 | 1.0 | 0 | - |
| a11-web-notewise-landing | web | 53 | 73 | 48 | 0.851 | 0 | - |
| a12-web-bakery-about | web | 94 | 94 | 83 | 1.0 | 0 | - |
| a13-general-security-blog | general | 56 | 100 | 94 | 0.459 | 1 | - |
| a14-resume-marketing-classic | resume | 1 | 100 | 45 | 0.455 | 2 | - |
| a15-social-manager-classic | social | 0 | 100 | 69 | 0.397 | 1 | - |
| a16-report-fourday-classic | report | 33 | 100 | 92 | 0.343 | 1 | - |
| a17-email-coverletter-classic | email | 28 | 50 | 43 | 0.404 | 2 | - |
| a18-web-ledgerline-classic | web | 24 | 46 | 74 | 0.505 | 3 | - |
| a19-report-freight-facts | report | 76 | 100 | 100 | 0.399 | 1 | - |
| h01-report-onboarding | report | 92 | - | 100 | - | - | - |
| h02-docs-site-tests | docs | 97 | - | 91 | - | - | - |
| h03-web-cloudgov-faq | web | 83 | - | 89 | - | - | - |
| h04-docs-oauth-proxy | docs | 94 | - | 97 | - | - | - |
| h05-general-new-ten | general | 91 | - | 96 | - | - | - |
| h06-report-https | report | 47 | - | 87 | - | - | - |
| h07-email-va-enrollment | email | 100 | - | 100 | - | - | - |
| h08-email-va-claim | email | 100 | - | 100 | - | - | - |
| h09-social-parks-day | social | 94 | - | 93 | - | - | - |
| h10-docs-express-readme | docs | 82 | - | 91 | - | - | - |
| h11-report-gao-review | report | 94 | - | 100 | - | - | - |
| h12-general-emoji-docs | general | 100 | - | 100 | - | - | - |
| h13-general-estonia | general | 66 | - | 93 | - | - | - |
| h14-resume-sample | resume | 64 | - | 46 | - | - | - |
