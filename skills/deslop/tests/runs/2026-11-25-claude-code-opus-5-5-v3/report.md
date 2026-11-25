# deslop run: 2026-11-25

Runner: claude, model: default.

| | deslop | plain Claude |
|---|---|---|
| AI samples: score before | 50.32 | 50.32 |
| AI samples: score after | 79.53 | 71 |
| AI samples: high hits left | 0 | 2 |
| Human samples: score after | 95.5 | 91.64 |
| Human samples: similarity to original | 0.98 | 0.54 |
| Rewrites that broke a number, URL or code | 0 | 5 |
| Numbers invented | 0 | 1 |
| Numbers lost | 0 | 11 |
| [NEEDS SPECIFIC] markers, AI samples | 17 | 0 |
| [NEEDS SPECIFIC] markers, human samples | 3 | 0 |
| Tokens per run (mean) | 147327.12 | 40936.39 |
| Seconds per run (mean) | 18.68 | 9.98 |

| Sample | Context | Before | deslop | plain | Similarity (deslop) | Markers | Pass 2 similarity |
|---|---|---|---|---|---|---|---|
| a01-resume-pm | resume | 2 | 3 | 3 | 0.91 | 0 | 0.961 |
| a02-resume-data | resume | 57 | 92 | 40 | 0.87 | 2 | 1.0 |
| a03-email-coverletter-ux | email | 33 | 85 | 88 | 0.923 | 3 | 0.98 |
| a04-social-launch | social | 38 | 79 | 62 | 0.783 | 1 | 1.0 |
| a05-social-lesson | social | 73 | 100 | 100 | 0.984 | 0 | 1.0 |
| a06-report-support-q3 | report | 92 | 92 | 100 | 1.0 | 0 | 1.0 |
| a07-report-billing-status | report | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| a08-email-kickoff-followup | email | 2 | 14 | 14 | 0.701 | 0 | 1.0 |
| a09-email-dashboard-delay | email | 79 | 79 | 79 | 0.955 | 0 | 0.937 |
| a10-docs-tidycsv-readme | docs | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| a11-web-notewise-landing | web | 64 | 88 | 48 | 0.937 | 0 | 1.0 |
| a12-web-bakery-about | web | 94 | 94 | 83 | 1.0 | 0 | 1.0 |
| a13-general-security-blog | general | 56 | 66 | 94 | 0.82 | 1 | 1.0 |
| a14-resume-marketing-classic | resume | 1 | 100 | 45 | 0.552 | 2 | 1.0 |
| a15-social-manager-classic | social | 0 | 100 | 69 | 0.372 | 1 | 1.0 |
| a16-report-fourday-classic | report | 33 | 100 | 92 | 0.325 | 2 | 1.0 |
| a17-email-coverletter-classic | email | 28 | 52 | 43 | 0.524 | 2 | 1.0 |
| a18-web-ledgerline-classic | web | 28 | 67 | 89 | 0.513 | 2 | 1.0 |
| a19-report-freight-facts | report | 76 | 100 | 100 | 0.419 | 1 | 1.0 |
| h01-report-onboarding | report | 92 | 92 | 100 | 1.0 | 0 | 1.0 |
| h02-docs-site-tests | docs | 97 | 97 | 91 | 1.0 | 0 | 1.0 |
| h03-web-cloudgov-faq | web | 83 | 100 | 89 | 0.96 | 1 | 1.0 |
| h04-docs-oauth-proxy | docs | 94 | 100 | 97 | 0.996 | 0 | 1.0 |
| h05-general-new-ten | general | 91 | 91 | 96 | 1.0 | 0 | 1.0 |
| h06-report-https | report | 47 | 88 | 87 | 0.968 | 0 | 1.0 |
| h07-email-va-enrollment | email | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| h08-email-va-claim | email | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| h09-social-parks-day | social | 94 | 93 | 93 | 0.939 | 0 | 1.0 |
| h10-docs-express-readme | docs | 82 | 86 | 91 | 0.997 | 0 | 1.0 |
| h11-report-gao-review | report | 94 | 94 | 100 | 1.0 | 0 | 0.997 |
| h12-general-emoji-docs | general | 100 | 100 | 100 | 1.0 | 0 | 1.0 |
| h13-general-estonia | general | 66 | 96 | 93 | 0.956 | 0 | 0.972 |
| h14-resume-sample | resume | 64 | 100 | 46 | 0.891 | 2 | 1.0 |

## Blind judge (AI samples, both orders)

Wins that held in both orders: deslop 8, plain Claude 9, split or tie 2.

| Mean score (1-10) | deslop | plain Claude |
|---|---|---|
| human | 6.5 | 8.0 |
| specific | 7.3 | 6.6 |
| faithful | 8.6 | 7.8 |
