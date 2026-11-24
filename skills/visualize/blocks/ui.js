// Shared helpers: status icons (one stroke set) and words. Color comes from CSS via .st-<state>.
window.UI = {
  word: { done: "Done", doing: "In progress", next: "Next", blocked: "Blocked", on: "On track", risk: "At risk", off: "Off track" },
  icon(s, size = 16) {
    const p = {
      done: '<path d="M4 8.5l2.5 2.5L12 5.5"/>',
      on: '<path d="M4 8.5l2.5 2.5L12 5.5"/>',
      doing: '<circle cx="8" cy="8" r="5.5"/><path d="M8 2.5a5.5 5.5 0 0 1 0 11z" fill="currentColor" stroke="none"/>',
      next: '<path d="M3.5 8h9M9 4.5L12.5 8 9 11.5"/>',
      blocked: '<path d="M8 3.5v5.5M8 12v.5"/>',
      risk: '<path d="M8 3.5v5.5M8 12v.5"/>',
      off: '<path d="M4.5 4.5l7 7M11.5 4.5l-7 7"/>',
      src: '<path d="M6.5 9.5l3-3M7 4.5l1-1a2.5 2.5 0 0 1 3.5 3.5l-1 1M9 11.5l-1 1A2.5 2.5 0 0 1 4.5 9l1-1"/>',
      x: '<path d="M4.5 4.5l7 7M11.5 4.5l-7 7"/>'
    }[s] || "";
    return `<svg class="ic" width="${size}" height="${size}" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
  },
  tag(s) { return `<span class="st st-${s}">${this.icon(s, 14)}${this.word[s]}</span>`; }
};
