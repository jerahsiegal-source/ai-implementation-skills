# my-voice

Make AI write like you, not like AI.

Run `/my-voice setup`. It takes about 25 minutes, mostly talking, and you don't need any writing samples. It gets better every time you edit a draft it wrote.

## How it works

```
Quick setup (25 min)  →  Profile  →  Drafts  →  Your edits  →  Learn  →  Better profile
   talk, habits,           built by a              saved as         proposes
   scenarios, taste        fresh subagent          before/after     changes you approve
                           from your raw words
```

Optional deep setup, any order:

| Add-on | Time | Adds |
|---|---|---|
| `setup samples` | any | Your real emails, posts, texts, reports. The biggest single upgrade. |
| `setup blindtest` | 10 min | 5 AI pieces mixed with 5 of yours. What gives the AI away becomes a rule. |
| `setup interview` | 30–40 min | What you'd choose to say: opinions, decisions, how you explain things |
| `setup scenarios+` | 20–30 min | Resume bullets, reports, critical feedback, and more |
| `setup crosscheck` | 5 min | A second model flags profile rules your evidence doesn't support |

## What makes it work

- **Raw answers, word for word.** The profile is built from your actual words, never from summaries.
- **Fresh-eyes builds.** A clean subagent reads only your evidence, so the profile isn't skewed by the interview chat.
- **Real writing beats self-description.** People describe themselves wrong. The builder trusts what you actually wrote and notes where it differs.
- **Never invent facts.** In blind tests, made-up excuses and events gave the AI away fastest, so drafts never add facts you didn't give.
- **Blind tests measure it.** Your reasons for spotting the AI turn straight into rules.

## With deslop

my-voice writes in your voice. [deslop](../deslop) catches AI tells. They work together in one step: after drafting, my-voice runs deslop's linter on the draft and fixes only the real tells, in your words. It does not run a full deslop rewrite, because deslop is voice-neutral and would sand your voice off. deslop is optional; without it my-voice checks the common tells by eye.

```
your facts  ->  my-voice draft (profile)  ->  deslop lint check  ->  ready to paste  ->  your edits  ->  learn
```

## Privacy

Your data lives in `~/.ai-skills/personal/my-voice/` (or `$MY_VOICE_HOME`) on your computer, next to the other private skill files. Nothing in it is ever committed. This repo ships only prompts and scripts. Sample import saves only your own words, and redacts phone numbers, addresses and account numbers.

## Install

**Claude Code and Codex**

Run the repo's install script (`./install.sh` or `.\install.ps1`). It links my-voice (and deslop) into both. Then type `/my-voice setup` in Claude Code or `$my-voice setup` in Codex.

Where Codex has no subagent tool, the skill runs builds as a separate step that reads only your evidence files.

**Claude app (claude.ai)**

Zip the `my-voice` folder and upload it under Settings → Capabilities → Skills. The app can't keep a folder on your computer between chats, so run setup inside a Project. At the end of setup, ask Claude to give you the `profile/` files and add them to the Project's knowledge. The best setup is to build your profile in Claude Code or Codex, then add `profile/` to a Claude Project for everyday drafting.

## Commands

| Command | Does |
|---|---|
| `/my-voice setup` | Quick setup |
| `/my-voice setup <add-on>` | samples, blindtest, interview, scenarios+, crosscheck |
| `/my-voice draft <what>` | Draft in your voice (or just say "write this as me") |
| `/my-voice learn` | Turn your edits into profile updates you approve |
| `/my-voice rebuild` | Rebuild the profile from all evidence |
| `/my-voice status` | Progress, confidence per medium, next step |

Helper: `python3 scripts/voice.py {init,status,import,log-edit,snapshot,mark-learned,where}` (standard library only; uses pandoc or pdftotext if installed). On Windows use `python` or `py`.

## Does it beat plain Claude?

`tests/voice_eval.py` drafts from fact-only briefs of messages you really sent, then a blind judge compares each draft with the real one. See [tests/README.md](tests/README.md).

## Files

```
my-voice/
  SKILL.md
  references/  setup-quick, setup-deep, samples, builder, drafting, blindtest, learn
  scripts/voice.py
  tests/voice_eval.py
  agents/openai.yaml
```
