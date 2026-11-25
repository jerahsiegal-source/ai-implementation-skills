# deslop run: 2026-11-25

Runner: claude, model: default.

| | deslop | plain Claude |
|---|---|---|
| AI samples: score before | 50.32 | 50.32 |
| AI samples: score after | 96.11 | 71 |
| AI samples: high hits left | 0 | 2 |
| Human samples: score after | 96.57 | 91.64 |
| Human samples: similarity to original | 0.98 | 0.54 |
| Rewrites that broke a number, URL or code | 0 | 5 |
| Numbers invented | 0 | 1 |
| Numbers lost | 0 | 11 |
| [NEEDS SPECIFIC] markers, AI samples | 62 | 0 |
| [NEEDS SPECIFIC] markers, human samples | 3 | 0 |
| Tokens per run (mean) | 161208 | 40936.39 |
| Seconds per run (mean) | 19.78 | 9.98 |

| Sample | Context | Before | deslop | plain | Similarity (deslop) | Markers | Pass 2 similarity |
|---|---|---|---|---|---|---|---|
| a01-resume-pm | resume | 2 | 100 | 3 | 0.696 | 20 | 1.0 |
| a02-resume-data | resume | 57 | 92 | 40 | 0.858 | 1 | 1.0 |
| a03-email-coverletter-ux | email | 33 | 96 | 88 | 0.897 | 7 | 1.0 |
| a04-social-launch | social | 38 | 100 | 62 | 0.93 | 0 | 1.0 |
| a05-social-lesson | social | 73 | 100 | 100 | 0.953 | 1 | 1.0 |
| a06-report-support-q3 | report | 92 | 92 | 100 | 1.0 | 0 | 1.0 |
| a07-report-billing-status | report | 100 | 100 | 100 | 0.98 | 1 | 1.0 |
| a08-email-kickoff-followup | email | 2 | 100 | 14 | 0.7 | 10 | 1.0 |
| a09-email-dashboard-delay | email | 79 | 100 | 79 | 0.907 | 3 | 1.0 |
| a10-docs-tidycsv-readme | docs | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| a11-web-notewise-landing | web | 64 | 88 | 48 | 0.902 | 2 | 1.0 |
| a12-web-bakery-about | web | 94 | 94 | 83 | 1.0 | 0 | 1.0 |
| a13-general-security-blog | general | 56 | 93 | 94 | 0.739 | 3 | 1.0 |
| a14-resume-marketing-classic | resume | 1 | 79 | 45 | 0.538 | 1 | 1.0 |
| a15-social-manager-classic | social | 0 | 100 | 69 | 0.417 | 2 | 1.0 |
| a16-report-fourday-classic | report | 33 | 100 | 92 | 0.4 | 2 | 1.0 |
| a17-email-coverletter-classic | email | 28 | 100 | 43 | 0.481 | 6 | 1.0 |
| a18-web-ledgerline-classic | web | 28 | 92 | 89 | 0.506 | 2 | 1.0 |
| a19-report-freight-facts | report | 76 | 100 | 100 | 0.294 | 1 | 1.0 |
| h01-report-onboarding | report | 92 | 97 | 100 | 0.993 | 0 | 1.0 |
| h02-docs-site-tests | docs | 97 | 97 | 91 | 1.0 | 0 | 1.0 |
| h03-web-cloudgov-faq | web | 83 | 97 | 89 | 0.931 | 1 | 1.0 |
| h04-docs-oauth-proxy | docs | 94 | 100 | 97 | 0.996 | 0 | 1.0 |
| h05-general-new-ten | general | 91 | 91 | 96 | 1.0 | 0 | 1.0 |
| h06-report-https | report | 47 | 97 | 87 | 0.956 | 1 | 1.0 |
| h07-email-va-enrollment | email | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| h08-email-va-claim | email | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| h09-social-parks-day | social | 94 | 94 | 93 | 1.0 | 0 | 1.0 |
| h10-docs-express-readme | docs | 82 | 86 | 91 | 0.997 | 0 | 1.0 |
| h11-report-gao-review | report | 94 | 100 | 100 | 0.997 | 0 | 1.0 |
| h12-general-emoji-docs | general | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| h13-general-estonia | general | 66 | 93 | 93 | 0.953 | 0 | 0.973 |
| h14-resume-sample | resume | 64 | 100 | 46 | 0.926 | 1 | 1.0 |

## Blind judge (AI samples, both orders)

Wins that held in both orders: deslop 8, plain Claude 9, split or tie 2.

| Mean score (1-10) | deslop | plain Claude |
|---|---|---|
| human | 6.2 | 8.0 |
| specific | 7.3 | 6.4 |
| faithful | 8.6 | 7.9 |
