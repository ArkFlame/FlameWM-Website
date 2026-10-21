# FlameWM V7 — Window-Entry Taskbar, Pinning, Context Actions & Direct Reordering Native Quirks Report

**Project:** FlameWM  
**Studio:** ArkFlame Studios  
**Base:** IceWM 4.1.0 / X11  
**Reference:** `breeze-desktop-prototype-v7`  
**Date:** 2026-09-02  
**Status:** Final V7 addendum. This document supersedes older FlameWM taskbar grouping/context-menu rules where they conflict. All unrelated V6/V5/V4 behavior remains in force.

---

# 0. Final V7 decision

FlameWM's taskbar application area is a **unified ordered strip of application launch slots and individual open-window entries**.

The word **active** in this V7 requirement means:

> **The application has an open window.**

It does **not** mean focused, selected, foreground, unminimized or maximized.

The final visible model is:

```text
pinned app + zero open represented windows
    -> one persistent launcher entry

pinned app + one open represented window
    -> one window entry occupying the persistent pinned slot

pinned app + N open represented windows
    -> N independent window entries
       one occupies the persistent pinned slot
       N-1 are additional independent entries

unpinned app + N open represented windows
    -> N independent window entries
```

**No same-application window grouping is allowed in the FlameWM task strip.**

If Dolphin has three open windows, FlameWM shows three Dolphin task entries. They may be focused, minimized, closed and reordered independently.

Pinning remains application-level. Window state remains window/frame-level.

---

# 1. Exact final context-menu matrix

This matrix is normative.

## 1.1 Pinned and no open represented window

```text
Open
Unpin
```

Semantics:

- `Open` launches a new application window/process through the existing application-launch authority.
- `Unpin` removes the application from FlameWM's pinned application set.
- No Close, Maximize or Minimize exists because there is no window target.

## 1.2 Pinned and open window

Every open window gets its own entry.

Right-click that specific window entry:

```text
Unpin
────────
Maximize | Minimize
Close
```

Semantics:

- `Unpin` changes **application pin state**. It does not close this window or any sibling window.
- `Maximize/Minimize` applies only to the clicked window.
- `Close` applies only to the clicked window.

## 1.3 Unpinned and open window

```text
Pin
────────
Maximize | Minimize
Close
```

Semantics:

- `Pin` pins the application identity represented by this window.
- The clicked window becomes the anchor occupying the persistent pinned slot at its current task-strip position.
- Other windows of the same application remain separate task entries.

## 1.4 State-dependent size action

Use exactly one size/state action, not a verbose window menu.

```text
window is visible + maximized -> Minimize
otherwise                     -> Maximize
```

This includes minimized windows: a minimized window offers `Maximize`, which restores it and places it maximized.

Do not expose both Maximize and Minimize simultaneously in this compact task context menu.

Do not add Restore unless a later explicit product decision requests it.

---

# 2. V7 supersessions

V7 supersedes these older project-source statements:

## 2.1 Superseded: one grouped icon per application

Older reports proposed:

```text
multiple windows of same application
-> one icon + count/dots/group popup
```

That is no longer the FlameWM product.

Final V7:

```text
multiple windows of same application
-> one task entry per window
```

## 2.2 Superseded: pinned task context = Unpin only

That applied to V3/V4.

Final V7 distinguishes inactive pinned launchers from pinned open-window entries.

## 2.3 Superseded: non-pinned task context = Activate / Close

Final V7 uses:

```text
Pin
Maximize | Minimize
Close
```

Activation is primarily the normal left-click behavior, not a required context-menu row.

---

# 3. Source-grounded IceWM findings

The uploaded IceWM 4.1.0 source was re-audited specifically for this V7 change.

## 3.1 IceWM already supports disabling same-class grouping

Source:

```text
src/default.h
```

Current preference declaration:

```cpp
XIV(int, taskBarTaskGrouping, 0)
```

Current preference metadata describes:

```text
TaskBarTaskGrouping
0 = off
1 = digits
2 = dots
3 = both
```

Therefore FlameWM does **not** need to invent a new anti-grouping mechanism.

Final FlameWM default/effective behavior for the product task strip must be equivalent to:

```text
TaskBarTaskGrouping=0
```

## 3.2 `TaskPane::addApp()` already creates independent task buttons when grouping is disabled

Source:

```text
src/atasks.cc
TaskPane::addApp(ClientData* frame)
```

The current source only searches for an existing same-class task button inside:

```cpp
if (grouping()) {
    ...
}
```

When grouping is zero, `task` remains null and IceWM creates a new:

```cpp
new TaskButton(this)
```

for the frame.

This is exactly the native engine behavior V7 wants for open windows.

### Native rule

Do not replace this with a new process/window grouping registry.

Reuse IceWM's frame/task ownership and ensure Flame's final product path does not later regroup same-app windows.

## 3.3 IceWM already supports direct task-button drag reordering

Source:

```text
src/atasks.cc
TaskButton::handleBeginDrag(...)
TaskPane::startDrag(...)
TaskPane::processDrag(...)
TaskPane::endDrag()
```

Current behavior:

```text
left-button drag begins
-> TaskPane grabs pointer events
-> dragged TaskButton follows pointer
-> processDrag() finds target slot
-> fTasks.swap(drag, drop)
-> relayout
```

The IceWM manual also documents that task-window buttons can be dragged with the left mouse button to rearrange their order.

### Consequence

V7 does **not** require a replacement drag engine for running window buttons.

The native work is to extend/unify this behavior so inactive pinned launcher placeholders participate in the same ordered strip.

## 3.4 IceWM already owns exact window state/actions

Existing task/frame machinery already knows:

- focused;
- visible;
- minimized;
- maximized;
- ability to minimize;
- ability to close;
- activation/focus;
- task association with its frame/client.

FlameWM must derive menu rows from these authoritative states.

Do not duplicate them in a separate task state database.

## 3.5 IceWM currently separates pinned-like launchers from active task buttons

Current architecture separates:

```text
ObjectBar / toolbar launchers
TaskPane / TaskButton running windows
```

This is the actual remaining architectural gap.

V7 wants one continuous ordered interaction surface where:

- a pinned launcher can occupy a slot;
- that slot can become an active window entry;
- extra windows can be adjacent or moved elsewhere;
- all entries can be reordered directly.

---

# 4. Native identity model

Do not confuse application identity with window identity.

## 4.1 Application identity

Pinning is keyed to stable application identity.

Recommended lookup order remains:

```text
1. desktop application ID
2. .desktop StartupWMClass
3. X11 WM_CLASS mapping
4. normalized fallback only when unavoidable
```

Never pin by window title.

A pinned record stores an application/desktop-entry identity, not an X11 window ID.

## 4.2 Window identity

Every managed open frame/window receives its own active task entry.

Native authority is the existing IceWM `ClientData` / `TaskBarApp` / `TaskButton` / `YFrameWindow` relationship.

Window entries are ephemeral.

Never persist raw X window IDs across sessions.

## 4.3 Pin slot identity

A pinned application owns one persistent logical **pin slot**.

Conceptually:

```text
PinSlot {
    ApplicationId app;
    ordered position;
}
```

The slot renders in one of two forms:

```text
no represented app window
    -> PinnedLauncherEntry

one or more represented app windows
    -> one chosen WindowTaskEntry occupies the pin slot
```

Additional windows always render as separate window entries.

---

# 5. Stable pinned-slot behavior

This detail prevents the taskbar from jumping around as applications open and close.

## 5.1 Opening first window of pinned app

Before:

```text
[ Firefox launcher ] [ Dolphin launcher ] [ Konsole launcher ]
```

Open Dolphin:

```text
[ Firefox launcher ] [ Dolphin window #1 ] [ Konsole launcher ]
```

Do **not** render:

```text
[ Dolphin launcher ] [ Dolphin window #1 ]
```

That duplicate-icon behavior is forbidden.

## 5.2 Opening second and third windows

```text
[ Firefox launcher ] [ Dolphin #1 ] [ Dolphin #2 ] [ Dolphin #3 ] [ Konsole ]
```

Their initial placement may be adjacent to the pinned anchor slot, but the user can then reorder every task entry independently.

## 5.3 Closing anchor window

If Dolphin #1 occupied the pin slot and closes while #2/#3 remain:

- choose a surviving Dolphin window deterministically as the pin-slot occupant;
- retain the pin slot's position;
- do not make the whole Dolphin group jump to a new location.

Recommended deterministic selection:

```text
most recently focused surviving app window
```

or, if easier to integrate with current IceWM ordering:

```text
first surviving app window in current task order
```

Choose one rule and test it. Do not use random container iteration order.

## 5.4 Closing last window

The persistent pinned launcher reappears in the same pin slot:

```text
[ Dolphin #last ] -> close -> [ Dolphin launcher ]
```

---

# 6. Pin/Unpin transitions with multiple windows

## 6.1 Pin from a live window entry

Given:

```text
[ Firefox ] [ Dolphin #1 ] [ Dolphin #2 ]
```

Dolphin is not pinned.

Right-click Dolphin #2 → Pin.

Required:

- app identity becomes pinned;
- clicked #2 becomes the pin-slot anchor at its current strip position;
- #1 stays a separate live entry;
- no extra Dolphin launcher appears.

## 6.2 Unpin from any live window of a pinned app

Given three pinned Dolphin windows:

```text
[ Dolphin #1 ] [ Dolphin #2 ] [ Dolphin #3 ]
```

Right-click any one → Unpin.

Required:

- application pin state becomes false;
- no window closes;
- all three remain independent live task entries;
- their current ordering is preserved;
- when all later close, no launcher remains.

This is application-level state changed from a window-level entry.

---

# 7. Left-click behavior for individual entries

For every live window entry:

```text
if this exact window is focused + visible
    -> minimize this exact window
else
    -> restore if minimized
    -> activate/focus this exact window
```

Do not route same-app task clicks to an arbitrary most-recent window.

This is the main behavioral consequence of removing application grouping.

For a pinned inactive launcher:

```text
left click -> Open
```

which launches a new app window.

---

# 8. Multiple-window launch contract

The prototype's old behavior attempted to find an existing same-app window and focus it instead of creating another.

V7 removes that generic restriction.

Native FlameWM must not impose a shell-level single-instance policy.

Application launch behavior should be:

```text
user activates launcher/application entry
-> execute its normal .desktop launch action
-> application decides whether that action creates a new process/window or focuses an existing singleton instance
```

This is important: native FlameWM should not fabricate extra client windows for applications that are internally single-instance.

The browser prototype can create another simulated window because it is modeling window-capable applications. Native FlameWM simply launches normally and reflects whatever windows the application actually creates.

---

# 9. Direct task-entry drag reordering

## 9.1 Product gesture

```text
left press on application/window entry
hold
move along taskbar axis
entry follows/reorders
release
new order remains
```

No edit mode.

No explicit “Reorder taskbar” command.

## 9.2 Axis

```text
Bottom / Top  -> horizontal X order
Left / Right  -> vertical Y order
```

## 9.3 Reuse existing TaskPane drag mechanics

Current IceWM's active `TaskButton` drag implementation already does the difficult pointer grab and swap logic.

The Flame implementation should reuse/refactor that rather than writing a parallel drag controller for active tasks.

## 9.4 Unified strip gap

Inactive pinned launchers are not ordinary `TaskButton`s in stock IceWM.

To satisfy V7, implement one ordered Flame task-strip abstraction that can contain:

```text
PinnedLauncherEntry
WindowTaskEntry
```

while window actions/state still delegate to existing TaskButton/TaskBarApp/frame authorities.

Possible low-divergence shape:

```text
FlameTaskStrip
    OrderedEntry[]

OrderedEntry =
    PinnedSlot(ApplicationId)
    WindowSlot(TaskBarApp/TaskButton)
```

Do not duplicate frame state inside `FlameTaskStrip`.

## 9.5 Dragging does not pin/unpin

Reordering an entry changes only order.

Dragging a running unpinned task among pinned slots must **not** implicitly pin it.

Dragging an inactive pinned launcher does not unpin it.

Pin state changes only through explicit Pin/Unpin commands.

---

# 10. Ordering persistence

Separate persistent product order from ephemeral window order.

## 10.1 Persist

Persist:

- application pin membership;
- persistent pin-slot ordering.

Use stable application identities.

## 10.2 Session-only

Window task-entry ordering may be session-only because windows are ephemeral.

If the WM already retains task-button order for the current lifetime, reuse it.

## 10.3 Never persist

Never write raw X11 window IDs as durable cross-session taskbar configuration.

They are not stable identities.

---

# 11. Current workspace semantics

FlameWM's normal taskbar represents windows visible for the task pane's configured workspace policy.

Default product direction remains current-workspace oriented.

Therefore “active = any window open” means:

> any open window represented by this taskbar's current task-window scope, regardless of focus/minimized state.

Do not reinterpret “active” as focused.

If a future setting enables show-all-workspace windows, the same V7 entry/context rules apply to those represented windows.

---

# 12. Context-menu positioning

Retain the already-approved V3+ geometry rule.

For bottom panel:

```text
menu.left = clicked entry left edge where possible
menu appears above taskbar
```

Top/Left/Right panels use edge-aware adjacent positioning.

The menu target is the **specific task entry**, not the app as a whole, except Pin/Unpin state itself.

---

# 13. Window-state action rules

## 13.1 Maximize

Use `YFrameWindow`/existing frame action authority.

If minimized:

```text
restore/show
then maximize
then focus
```

If normal/snapped:

```text
maximize using normal IceWM maximize semantics
```

Do not implement maximize by manually writing taskbar-owned geometry.

## 13.2 Minimize

Use normal frame `wmMinimize()` semantics.

## 13.3 Close

Use the existing WM close action/protocol path.

Do not kill client processes from the taskbar.

---

# 14. Visual state

Each window entry retains the final Flame visual state rules:

```text
running background
    -> subtle activity indicator

focused + visible
    -> strong Flame accent activity indicator

minimized
    -> activity indicator retained
    -> icon visually de-emphasized
```

Pinned inactive launcher:

```text
icon
no running indicator
```

A pinned active window does not need a separate pin badge; pin state is discoverable through its context menu and stable slot behavior.

---

# 15. Accessibility and pointer behavior

- Drag threshold must be non-zero so ordinary click does not accidentally reorder.
- Right-click must never start a drag.
- Pointer grab must be released on normal release, cancel, task destruction and taskbar destruction.
- Closing a window while its task entry is being dragged must end/cancel the drag safely.
- Output/taskbar orientation change during a drag must cancel or complete the drag deterministically; do not retain a stale X/Y drag basis.
- Keyboard task navigation must continue working after mouse reordering.

---

# 16. Multi-monitor / per-output panels

V5 established that native FlameWM eventually has one panel per physical output.

V7 ordering is therefore panel-local presentation state backed by shared IceWM window authorities.

Rules:

- a window entry appears on the panel/output policy chosen by FlameWM;
- moving a window to another output may move its task representation accordingly if the final panel model filters by output;
- pin membership is application-level and should normally be shared across panels;
- pin ordering policy should be deliberately chosen as global or per-output; do not accidentally duplicate config because each panel has an object instance.

Recommended first complete product:

```text
pin membership/order = global Flame config
active window entries = output/current-workspace derived
```

---

# 17. Source touchpoints

Expected native touchpoints:

```text
src/atasks.cc/.h
    keep one-task-per-window behavior with grouping disabled
    reuse drag mechanics
    expose/refactor ordered task operations where Flame strip needs them

src/objbar.cc/.h
    only if existing toolbar launcher implementation is reused for inactive pinned slots

src/wmtaskbar.cc/.h
    host unified Flame task strip / context routing

src/flamewm/panel/taskidentity.*
    stable application identity and pin state

src/flamewm/panel/taskstrip.*          # likely new
    unified ordered pinned/window entry model

src/flamewm/panel/taskcontext.*        # optional bounded owner
    exact V7 menu matrix/action routing

src/flamewm/core/config.*
    persistent pinned identities/order
```

Do not turn `atasks.cc` into a large Flame policy file.

---

# 18. Minimal data contracts

Conceptually:

```cpp
struct PinnedApplication {
    DesktopAppId appId;
    int order;
};
```

A runtime task entry can be represented without owning window state:

```cpp
enum class TaskEntryKind {
    PinnedLauncher,
    Window
};

struct TaskEntryRef {
    TaskEntryKind kind;
    DesktopAppId appId;
    TaskBarApp* windowTask; // null for inactive launcher
};
```

Exact C++ type design must follow the current repository's memory/lifetime conventions. The important contract is identity separation, not these literal names.

---

# 19. Required native verification matrix

## 19.1 Context matrix

Test all three exact contexts:

```text
pinned + zero windows
pinned + one/multiple windows
unpinned + one/multiple windows
```

Verify exact allowed actions and absence of forbidden rows.

## 19.2 Window action targeting

With two Dolphin windows:

- right-click Dolphin A → Close closes only A;
- Dolphin B remains;
- right-click B → Maximize affects only B;
- minimize B changes B's indicator only.

## 19.3 Pin state

With two unpinned same-app windows:

- Pin A → application becomes pinned;
- A and B remain separate;
- both now expose Unpin;
- Unpin B → both become unpinned;
- no window closes.

## 19.4 Inactive pinned slot

- pin app;
- close all windows;
- one launcher remains;
- context = Open/Unpin;
- Open invokes application launch;
- first resulting window replaces launcher at same logical slot.

## 19.5 No grouping

Open 1, 2, 3 windows with identical `WM_CLASS`.

Expected:

```text
3 visible task entries
```

Not:

```text
1 grouped task button
```

Ensure Flame defaults/effective settings do not accidentally re-enable `TaskBarTaskGrouping`.

## 19.6 Reordering

With entries:

```text
A B C D
```

Drag C before A:

```text
C A B D
```

Verify:

- exact visual order;
- click target still maps to correct frame;
- context target still maps to correct frame;
- no pin-state mutation;
- minimize/focus still targets correct window;
- horizontal and vertical panels;
- same-app sibling windows can cross each other in order.

## 19.7 Drag cancellation

Verify:

- pointer cancel;
- window closes during drag;
- workspace changes during drag;
- taskbar edge/orientation changes;
- output disappears;

No stuck grab.

---

# 20. Prototype V7 implementation model

The browser V7 uses the following explicit task keys:

```text
pin:<appId>
    persistent pin slot

win:<windowId>
    additional/ephemeral window slot
```

A pinned app's selected anchor window occupies `pin:<appId>` while it is open.

This is prototype state only. Native code should not copy browser localStorage or string IDs literally; it should preserve the semantics using native application/frame identities.

---

# 21. Performance rules

This feature should be nearly free at idle.

Do not add:

- periodic task polling;
- process scanning;
- repeated X property queries on a timer;
- per-entry background threads;
- animations requiring permanent frame timers.

Task strip updates are event-driven from existing IceWM frame/task lifecycle events and explicit user reorder/pin actions.

---

# 22. Final native implementation decision

Use IceWM's existing task engine as much as possible:

```text
TaskBarTaskGrouping=0
    -> one active TaskButton per open frame

existing TaskButton/TaskPane drag
    -> running-window reorder mechanics

existing YFrameWindow state/actions
    -> focus/minimize/maximize/close authority
```

Add only the Flame product layer that IceWM lacks:

```text
stable application pin identity
persistent pin slots
inactive pinned launcher representation
first-window replacement of pinned slot
exact V7 context matrix
unified drag order across pinned launchers + active windows
```

The implementation is wrong if it solves V7 by reimplementing window state, X11 window enumeration, minimize/maximize/close semantics, or active-task drag from zero.

The implementation is also wrong if it leaves IceWM grouping enabled and hides multiple windows behind one application icon.

---

# 23. Canonical V7 summary for future coding agents

> **FlameWM V7 defines taskbar “active” as having an open window, not focus. Pinned/no-window entries expose Open + Unpin. Every open window is its own task entry—even when several share the same application/class. A pinned open window exposes Unpin + one state-dependent Maximize/Minimize action + Close; an unpinned open window exposes Pin + the same window-state action + Close. Pinning is application-level; size/close actions are window-level. Pinned apps own a stable launcher slot: the first open window occupies that slot, extra windows get independent entries, and the launcher returns when the last window closes. All application/window entries can be reordered by direct left-button press-hold drag along the taskbar axis, with no edit mode. Native IceWM 4.1.0 already provides TaskBarTaskGrouping=0, one TaskButton per frame when grouping is off, exact window state/actions, and left-drag TaskPane reordering; FlameWM must reuse those and add only the unified pinned-slot/window-entry product layer.**
