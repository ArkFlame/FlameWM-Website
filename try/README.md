# FlameWM Desktop Prototype v8 — Final Taskbar Reorder Fix

Interactive HTML/CSS/JavaScript specification for FlameWM, ArkFlame Studios' lightweight IceWM 4.1.0 fork.

This is a behavioral/visual prototype only. Production FlameWM remains native C++/X11 on IceWM; no browser/WebView runtime is intended.

## Run

```bash
./dev.sh
```

No npm install or build step is required.

## V8 final fix

V8 fixes the taskbar drag/reorder defect that remained in V7.

- Every pinned launcher and every open-window task entry can be press-held and dragged.
- Drop positions are real insertion slots: before the first entry, between any two entries, or after the final entry.
- Reordering commits only when the pointer is released.
- The held entry is represented by a floating drag ghost and a Flame-accent insertion marker.
- The original task entry stays in its DOM slot during the gesture, keeping pointer capture stable instead of moving the captured element itself.
- Reordering works for both inactive pinned launchers and active window entries.
- Multiple windows from the same application remain independent task entries and can be reordered independently.
- Horizontal taskbars use the X axis. Left/right taskbars use the Y axis.
- A short click still activates/minimizes the exact window; movement beyond the drag threshold starts reordering.
- Reordered task state persists in the V8 storage namespace.

## Final task context policy

```text
Pinned + no window
Open
Unpin

Pinned + open window
Unpin
Maximize / Minimize
Close

Not pinned + open window
Pin
Maximize / Minimize
Close
```

“Active” means at least one window from the application is open; it does not mean focused.

## Retained V6/V7 behavior

All non-conflicting V6/V7 behavior remains: Flame red accent, pitch-black desktop, Breeze icons, FlameWM branding, compact tree Start with inline search, independent same-app windows, four-edge taskbar, two-row virtual desktops, media/audio/Wi-Fi/calendar, sticky notes, desktop grid/selection/Trash, snap layouts, per-monitor Settings simulation, font/icon-theme controls, hotkeys, taskbar personalization and `https://wm.arkflame.com`.

## Important files

- `index.html` — shell surfaces.
- `styles.css` — FlameWM visual system and V8 drag ghost/drop marker.
- `app.js` — V8 interaction/state implementation.
- `PORTING_CONTRACT.md` — concise prototype-to-native contract.
- `FLAMEWM_V8_TASKBAR_DRAG_REORDER_FINAL_QUIRKS_REPORT.md` — V8 regression/native implementation note.
- `VERIFICATION.md` — executed verification record.
- `historical/` — previous V4–V7 reports retained for provenance.
