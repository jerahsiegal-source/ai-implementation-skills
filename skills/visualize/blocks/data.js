// Real content: the design skills toolkit, as of Mon 23 Nov 2026, 9:55 PM ET.
window.P = {
  name: "Design skills toolkit",
  asOf: "Mon 23 Nov · 9:55 PM",
  health: "on", // on | risk | off
  healthWord: { on: "On track", risk: "At risk", off: "Off track" },
  pct: 58,
  title: "Design skills",
  verdict: "Design and Explore shipped. Visualize is next.",
  update: [
    "/design and /explore are live in Claude Code and Codex.",
    "Explore now researches and critiques before you see anything.",
    "Six Visualize formats are built. Studio is the look."
  ],
  since: [
    { label: "Skills shipped", val: "2", delta: "of 5 planned", tone: "ok" },
    { label: "PRs merged", val: "3", delta: "all tonight", tone: "ok" },
    { label: "References studied", val: "12", delta: "6 captured live", tone: "ok" },
    { label: "Decisions waiting", val: "2", delta: "look picked", tone: "warn" }
  ],
  need: "Two quick calls: auto-offer, and what comes next.",
  streams: [
    { id: "design", name: "/design", s: "done", pct: 100, note: "Taste, surfaces, craft rules", detail: "Applies your taste to any UI. Reads the project's DESIGN.md, your private taste file and the shared kit. Upgraded tonight with concrete craft rules and a 'would a studio ship this?' check.", src: "PR #1, PR #3" },
    { id: "explore", name: "/explore", s: "done", pct: 100, note: "Research, concepts, critique", detail: "Rebuilt after round one: real research with captured references, concepts in words first, then full builds with a fresh critique and one revision.", src: "PR #1, PR #3" },
    { id: "kit", name: "Design kit", s: "done", pct: 100, note: "Floor, craft, styles, checks", detail: "Shared rules every design skill reads: readability floor, craft, screenshot quality check, brand intake, candidate styles.", src: "PR #1, PR #3" },
    { id: "install", name: "Install on your PC", s: "done", pct: 100, note: "Claude Code + Codex linked", detail: "All five skills are junctions to the repo in .claude\\skills and .agents\\skills. Old Intent Brief and Work Loop copies are backed up. One git pull updates everything.", src: "Install run, 8:47 PM" },
    { id: "visualize", name: "/visualize", s: "doing", pct: 40, note: "Six formats built", detail: "12 references studied. Six formats built, critiqued and revised. Studio picked as the look. Now packaging it as a skill.", src: "INTENT.md, research page" },
    { id: "loop", name: "Intent + Work Loop fit", s: "doing", pct: 70, note: "Wired, not yet used for real", detail: "Both skills now say how design work fits: pick the look first, then the loop builds and proves each visual item with screenshots. Not yet exercised on a real build.", src: "PR #1" },
    { id: "chart", name: "/chart", s: "next", pct: 0, note: "After Visualize", detail: "Chart rules: pick the chart by relationship (FT Visual Vocabulary), honest scales, labels on lines, a takeaway headline.", src: "Plan page" },
    { id: "flow", name: "/flow", s: "next", pct: 0, note: "After Chart", detail: "UX review: cognitive walkthrough, 0 to 4 severity, every finding tied to a screenshot.", src: "Repo research" }
  ],
  risks: [
    { t: "/explore not yet tried inside Codex", d: "Codex lists same-named skills side by side and Claude has a built-in Explore agent. Needs one real run in each tool.", tone: "warn" },
    { t: "Windows installer needs a policy tweak", d: "PowerShell's execution policy blocked install.ps1, so the steps were run by hand. A one-line note in the README would fix it for others.", tone: "warn" }
  ],
  decisions: [
    { q: "Shared look", why: "One look keeps every format in the same family.", opts: [
      { n: "Paper", c: "Warm off-white, teal accent, soft corners. Calm for long reading." },
      { n: "Studio", c: "Crisp white, ink blue, tight corners, a technical feel." },
      { n: "Night", c: "Dark ground, cyan accent. Easy on the eyes late at night." }
    ], rec: 1, pick: 1, recWhy: "Crisp and product-like. Paper stays as an option." },
    { q: "Offer on long answers?", why: "Manual skills, but long text is when a visual helps most.", opts: [
      { n: "Manual only", c: "Only runs when you type /visualize." },
      { n: "Offer, don't run", c: "Adds one line: 'Want this as a visual?' when output is big." },
      { n: "Run automatically", c: "Builds the page without asking on big outputs." }
    ], rec: 1, recWhy: "Keeps you in control and still saves you from walls of text." },
    { q: "Next skill", why: "Visualize leans on charts.", opts: [
      { n: "/chart next", c: "Visualize's charts get the full rule set sooner." },
      { n: "/flow next", c: "Better UX reviews for your product pages sooner." }
    ], rec: 0, recWhy: "Visualize will use charts every day." }
  ],
  get open(){return this.decisions.filter(d=>d.pick==null)},
  timeline: [
    { t: "7:49 PM", h: "Plan drafted", d: "Two front doors, three add-ons, one shared kit." },
    { t: "8:00 PM", h: "/design and /explore shipped", d: "PR #1 merged. Names picked: design, explore, flow, chart, visualize." },
    { t: "8:21 PM", h: "Codex folder fixed", d: "PR #2 moved installs to .agents\\skills." },
    { t: "8:47 PM", h: "Installed on your PC", d: "All skills linked in Claude Code and Codex. Old copies backed up." },
    { t: "9:25 PM", h: "Round one rejected", d: "You didn't love any direction. Diagnosed: no research, recycled looks, no critique." },
    { t: "9:48 PM", h: "Explore upgraded", d: "PR #3 merged: research first, concepts first, critique round, craft rules." },
    { t: "9:52 PM", h: "Six concepts shortlisted", d: "Health Brief, Insight Tabs, Mission Map, Margin Notes, Pulse Board, Decision Desk." }
  ],
  // activity per 20-minute block, 7:40 PM to 10:00 PM ET (7 blocks), from commits and installs
  activity: {
    design: [1,0,0,0,0,1,0], explore: [1,1,0,0,0,1,1], kit: [1,0,0,0,0,1,0], install: [0,1,1,1,0,0,0],
    visualize: [0,1,0,0,0,1,1], loop: [1,0,0,0,0,0,0], chart: [0,0,0,0,0,0,0], flow: [0,0,0,0,0,0,0]
  },
  insights: [
    { k: "Lead with the answer", claim: "The best reports put the finding first and the evidence under it. Our World in Data opens each insight with a plain claim, and the chart sits beside it as proof.", src: "Our World in Data", url: "https://ourworldindata.org/co2-and-greenhouse-gas-emissions", use: "Every Visualize page opens on a one-sentence verdict." },
    { k: "Status is health plus change", claim: "Linear's project updates pair a health word (On track, At risk, Off track) with what changed since the last update. You see direction, not just a snapshot.", src: "Linear changelog, Aug 2023", url: "https://linear.app/changelog/2023-08-16-project-progress-reports", mock: 1, use: "Status pages show a health pill and a 'since last time' strip." },
    { k: "Sources beside claims", claim: "Tufte's sidenotes keep sources next to the sentence they support, so you never jump to the bottom of a page to check something.", src: "Tufte CSS", url: "https://edwardtufte.github.io/tufte-css/", use: "Research claims carry a margin source on wide screens, a tap on phones." },
    { k: "Compare in a grid", claim: "Ink & Switch compare options against goals in one matrix of ✓, — and ✗. A whole argument reads in a glance.", src: "Ink & Switch, Local-first", url: "https://www.inkandswitch.com/local-first/", use: "Any comparison of 3+ options becomes a matrix." },
    { k: "Pick the chart by relationship", claim: "The FT's Visual Vocabulary chooses a chart by what you are showing: change over time, ranking, part of a whole, flow.", src: "FT Visual Vocabulary", url: "https://ft-interactive.github.io/visual-vocabulary/", use: "Visualize routes each number set to a chart type by its relationship." }
  ],
  matrix: {
    goals: ["5-second read", "Detail on demand", "Sources visible", "Many projects", "Good to present"],
    rows: [
      { n: "Health Brief", v: [2,2,2,1,1] },
      { n: "Insight Tabs", v: [2,2,2,0,1] },
      { n: "Mission Map", v: [1,2,1,2,1] },
      { n: "Margin Notes", v: [1,2,2,0,1] },
      { n: "Pulse Board", v: [2,1,0,2,1] },
      { n: "Decision Desk", v: [2,1,1,1,2] }
    ]
  }
};
