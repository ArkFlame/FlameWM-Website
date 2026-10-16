# FlameWM V6 Final — UX, Prototype and Native IceWM Implementation Quirks Report

**Project:** FlameWM  
**Studio:** ArkFlame Studios  
**Native base:** IceWM 4.1.0 / X11  
**Reference prototype:** `breeze-desktop-prototype-v6`  
**Status:** Final V6 browser-prototype contract and native implementation addendum  
**Date:** 2026-09-02

---

## 0. Purpose

V6 is the final HTML/CSS/JavaScript behavioral reference before native FlameWM implementation work begins.

This document records the last UX decisions, the implementation mistakes exposed by V1–V5, and the exact native rules needed to avoid reproducing those mistakes in the IceWM fork.

The browser implementation is not production architecture. It exists to make state transitions, visual hierarchy, context menus, settings semantics, layering and interaction contracts executable before touching the real X11 window manager.

The core native rule remains:

> IceWM owns mature window-manager state. FlameWM owns the finished product experience around that state.

Do not recreate a second focus manager, workspace manager, window registry, task registry, XRandR geometry model, XEmbed tray or icon lookup engine merely because the browser prototype has local JavaScript objects for those concepts.

---

# 1. Authority and supersessions

Use this precedence when implementing FlameWM:

1. newest explicit product requirement;
2. verified current IceWM 4.1.0 source behavior;
3. this V6 final report;
4. V5 settings/display/hotkey report;
5. V4 prototype-to-native report;
6. complementary architecture/maintainability blueprint;
7. Product Soul / older planning reports;
8. historical prototype behavior.

V6 explicitly supersedes the following older UI decisions:

- Website is `https://wm.arkflame.com`.
- Start search stays inside the Start menu and replaces normal Start rows while filtering.
- Desktop context no longer creates virtual desktops.
- Virtual desktop creation belongs to the taskbar/workspace UX.
- One workspace means no workspace pager is shown.
- Sticky notes are a first-class optional desktop feature.
- Taskbar configuration includes color, opacity, height, Start label and custom Start icon.
- Custom accent selection is immediate; no Apply/Use Custom Color step.
- Hotkey reset appears only when a row differs from the shipped default and sits immediately beside the shortcut value.
- Desktop selection feedback must not paint over application windows or the taskbar.
- System icon-theme selection is a normal Appearance concept, but native FlameWM must reuse existing IceWM/freedesktop icon infrastructure.

---

# 2. V6 final behavior inventory

The final prototype adds or corrects these behaviors:

1. Website action uses `https://wm.arkflame.com`.
2. Settings explanatory copy is short and task-focused.
3. Custom accent color applies continuously as the color input changes.
4. Audio volume dragging retains pointer ownership after the pointer leaves the slider track.
5. Hotkey reset is white/high-contrast, adjacent to the assignment, and conditional on modification.
6. Start search is an in-menu mode rather than a separate launcher surface.
7. Desktop selection rectangle sits over desktop entries only—not application windows or taskbar.
8. Sticky notes support creation, editing, dragging, resizing, per-note appearance, deletion and global feature disable.
9. Blank taskbar context menu owns workspace creation and Taskbar Settings.
10. Taskbar Settings controls color, opacity, logical height, Start text and Start icon.
11. Appearance exposes icon theme selection.
12. Workspace pager disappears completely with one workspace.
13. `Add Virtual Desktop` is removed from the desktop context menu.
14. V6 retains all accepted V5/V4 behavior that does not conflict with the above.

---

# 3. Source-grounded IceWM facts that constrain V6 native implementation

## 3.1 IceWM has one global TaskBar today

Current `src/wmtaskbar.cc` declares:

```cpp
TaskBar *taskBar;
```

This remains a native architectural constraint for FlameWM's desired per-output panel behavior. V6 prototype code has one browser panel; native FlameWM eventually needs a panel host/manager capable of one panel per active physical output while preserving shared IceWM task/workspace authorities.

Do not pretend a CSS-style duplication of panels solves this in native code. Work areas, struts, Start anchoring, tray behavior and XRandR updates must all be source-consistent.

## 3.2 IceWM already owns Start-menu toggling semantics

Current `Win95Keys` explicitly supports the left Super key toggling the Start menu.

Current `TaskBar::popupStartMenu()` opens the applications menu owned by that taskbar.

FlameWM therefore does not need a second keyboard concept. It needs a product-level `Toggle Start menu` action that resolves the correct physical output/panel and calls the existing/extended panel authority.

## 3.3 Current `KeySysMenu` wording is position-specific

IceWM currently describes `KeySysMenu` as activating the root menu in the lower-left corner.

That assumption is obsolete for FlameWM because panels can be Bottom, Top, Left or Right and, natively, may exist on multiple outputs.

The product action must mean:

```text
Toggle Start menu on the currently active output's FlameWM taskbar.
```

## 3.4 IceWM already has freedesktop icon-theme lookup

Current IceWM exposes `IconThemes` and `IconPath`, and `src/yicon.cc` already resolves icon-theme candidates.

The freedesktop Icon Theme Specification defines icon themes as user-selectable named mappings and requires theme inheritance/fallback behavior, including `hicolor` fallback.

Therefore native FlameWM's Appearance icon-theme picker must change the selected theme/policy consumed by the existing `YIcon` pipeline. It must not implement a parallel recursive filesystem icon engine.

## 3.5 IceWM Start is still a classic menu model

`StartMenu::refresh()` in `src/wmprog.cc` builds the classic IceWM menu and appends traditional management items.

FlameWM should reuse application discovery, launching, menu primitives and session actions, but its approved compact Start/search semantics are product behavior and should be isolated in Flame-owned launcher code if the existing class cannot support them cleanly.

## 3.6 Filesystem desktop and sticky notes remain Flame-owned desktop concerns

IceWM does not provide a general filesystem desktop model. `MiniIcon` is for minimized windows, not files/folders/notes.

The established architecture remains:

```text
flamewm-desktop
    filesystem desktop entries
    grid/layout
    selection rectangle
    Trash/file actions
    sticky notes
    FlameWM desktop watermark
```

Do not put sticky-note persistence/editor code in `YWindowManager` or `YFrameWindow`.

---

# 4. Start menu search — final V6 contract

## 4.1 Why V5-style detached thinking was wrong

Search is not a second application launcher. It is a mode of the same Start surface.

A separate search popup creates unnecessary spatial switching and makes Start feel like two unrelated widgets.

## 4.2 Exact behavior

Closed Start:

```text
click Start / Toggle Start menu
-> normal category tree
-> search field remains at bottom
```

Search input empty:

```text
Development
Games
Graphics
Internet
Multimedia
System
Utilities
Power / Session
-----------------
Search…
```

Search input non-empty:

```text
Applications
matching app 1
matching app 2
matching app 3
-----------------
Search query stays editable here
```

While filtering:

- normal category rows are removed from the primary pane;
- category submenu is closed;
- matches appear in the same primary pane;
- no second detached result box;
- Enter/click launches the selected result;
- deleting the query to empty restores normal categories immediately.

## 4.3 Search data source

Native production search operates over the same normalized XDG desktop-entry application model used for Start categories.

Do not scan `/usr/share/applications` synchronously on every keystroke.

Preferred model:

```text
AppModel refreshed on application/menu changes
-> normalized searchable text cached per app
-> input event filters cached model in memory
-> renderer updates rows only
```

At minimum index:

```text
Name
GenericName / product description where available
Categories
keywords when safely supported by existing parser/model
```

Do not execute or evaluate search text as shell input.

## 4.4 Focus/keyboard requirements

- Start opened by keyboard may focus search immediately or route typed printable characters into search.
- Arrow navigation must remain deterministic.
- Escape closes Start.
- Clearing search restores category navigation without closing Start.
- Search state should normally reset when Start fully closes unless a later product decision explicitly preserves it.

---

# 5. Continuous controls — do not destroy the active widget while dragging

V6 exposed an important UI implementation class of bug: a live setting can technically work once and still be broken because its handler rerenders/replaces the element currently receiving the pointer interaction.

## 5.1 General rule

For continuous controls such as:

- taskbar opacity;
- taskbar height;
- accent color;
- sticky-note text size;
- overlay opacity;
- audio volume;

an `input`/motion event must update the underlying property **without replacing the active control**.

Bad pattern:

```text
range input motion
-> update setting
-> rebuild whole settings page/window
-> original range disappears
-> pointer continues over a new DOM/native object with no active grab
-> drag stops or behaves unpredictably
```

Native equivalent mistakes are equally possible if a settings widget hierarchy is destroyed/rebuilt on every slider notification.

## 5.2 Correct native model

```text
pointer/slider changes
-> update typed property
-> apply small runtime delta
-> repaint/reflow affected shell surface
-> keep Settings control alive
```

Only rebuild a page when the structure itself changes.

When a size change requires a heavier work-area/window relayout, perform cheap visual updating during drag and commit expensive reconciliation on release/change where appropriate.

---

# 6. Audio volume slider — pointer/grab semantics

## 6.1 Bug class

Listening only for motion while the pointer remains physically above the slider causes volume adjustment to stop when the user drags beyond the track.

That is contrary to normal desktop slider behavior.

## 6.2 V6 behavior

On primary-button press:

1. capture/grab the pointer;
2. compute value from root/client X relative to the track;
3. clamp below track to 0;
4. clamp beyond track to 100;
5. continue handling movement even outside the visual slider bounds;
6. release grab on pointer/button release or cancellation.

## 6.3 Native X11 requirement

Use the appropriate IceWM/YWindow mouse-grab mechanism or X11 pointer grab semantics already consistent with other drag interactions.

Do not poll pointer position.

Do not require the pointer to remain inside the slider child window.

No UI rebuild may occur during active volume drag.

## 6.4 Audio backend remains event-driven

This UX rule is independent from the real audio backend. The native product still uses an asynchronous PulseAudio-compatible client path against PipeWire-Pulse/PulseAudio and subscribes to external volume changes.

---

# 7. Hotkeys — final row model

## 7.1 Minimal help copy

Canonical helper text:

```text
Click a shortcut and press the new combination.
```

Do not explain Escape, reset icons, serialization details or implementation concepts in the permanent paragraph. The interaction itself should make them discoverable.

## 7.2 Row geometry

Canonical row:

```text
Action name                     [↶] [Ctrl + Win + Left]
```

When unchanged from shipped default:

```text
Action name                         [Ctrl + Win + Left]
```

The reset/revert icon belongs beside the value it restores—not beside the action name.

## 7.3 Reset visibility

Render reset only when:

```text
current effective assignment != shipped default assignment
```

If the user changes a shortcut and then manually sets it back to the exact default, the icon disappears.

## 7.4 Reset contrast

Dark FlameWM theme:

```text
revert glyph = white / current high-contrast symbolic foreground
```

Do not rely on the source SVG's fixed dark fill. Resolve symbolic icons through the semantic foreground/mask path.

## 7.5 Escape semantics

During capture:

```text
Escape -> unassigned/null -> display “Not assigned”
```

Escape is not recorded as the shortcut.

## 7.6 Native value model

Use a nullable typed binding:

```cpp
std::optional<KeyBinding>
```

or equivalent.

Do not store the literal UI string `Not assigned` as a key chord.

## 7.7 Live registration closure

After change:

```text
validate chord
-> resolve conflicts
-> persist override atomically
-> unregister prior X grab
-> register new grab when non-null
-> if grab fails, report failure and restore/effectively mark failed state
-> refresh only affected row/state
```

Never display a shortcut as active when X11 could not claim it.

---

# 8. Desktop selection rectangle — stacking contract

V6 final order:

```text
wallpaper
FlameWM watermark where applicable
desktop filesystem entries
selection rectangle
sticky notes
managed application windows
snap preview / shell popovers as appropriate
taskbar
```

The key invariant is:

> Desktop selection feedback can highlight/select desktop entries but must never visually wash over normal application windows or the panel.

## 8.1 Native implications

If `flamewm-desktop` owns the rectangle, keep it within the desktop-layer stacking domain beneath normal windows.

Do not create a root-level override-redirect selection window stacked above every client merely because that is convenient to draw.

The snap preview is a different overlay and may intentionally be above the window being moved. The two overlays share accent styling but **not stacking authority**.

---

# 9. Sticky notes — final product contract

## 9.1 Feature boundary

Sticky notes are intentionally simple and desktop-local.

They are not:

- a note-taking application framework;
- a widget SDK;
- cloud-synced;
- rich text;
- Markdown;
- a task database.

They are lightweight persistent text boxes on the desktop.

## 9.2 Desktop context action

When enabled:

```text
Open Terminal
Create New Folder
New Sticky Note
----------------
Desktop and Wallpaper…
```

When disabled, `New Sticky Note` is absent.

`Add Virtual Desktop` is absent in both states.

## 9.3 Note appearance

Default:

```text
square-ish note
warm yellow background
black/dark text
no titlebar
no cog icon
no visible settings chrome
```

The note should read as a text surface, not a miniature decorated application window.

## 9.4 Editing

Primary click into content allows direct multiline text editing.

Text persists incrementally or on safe coalesced edits.

Persist UTF-8 text exactly; do not turn note contents into shell syntax or markup.

## 9.5 Dragging

Because the note has no visible titlebar, reserve a small invisible/interaction-only top strip as the drag area.

This avoids the impossible conflict where the entire editable text surface both selects text and always drags the note.

Recommended logical behavior:

```text
top ~16–20 dp -> drag note
main content -> text selection/editing
bottom-right native resize affordance -> resize
```

The strip must not be visually presented as extra chrome.

## 9.6 Resizing

- minimum useful size enforced;
- maximum bounded to desktop work area;
- resize never places note under taskbar/outside usable desktop;
- after taskbar move, height change, resolution change or output topology change, clamp/reflow notes into valid work area.

Persist logical size/position, not assumptions tied to one screen pixel rectangle.

## 9.7 Right-click menu

```text
Settings
--------
Delete Note
```

Settings becomes a compact contextual editor for:

```text
Background color
Text color
Text size
```

All three apply live.

No global Apply button.

## 9.8 Persistence model

Suggested native model:

```cpp
struct StickyNote {
    NoteId id;
    WorkspaceId workspace;
    OutputIdentity output;
    LogicalRect rect;
    std::string textUtf8;
    RgbColor background;
    RgbColor foreground;
    int textSizeLogical;
};
```

Store in FlameWM user data/config owned by `flamewm-desktop`, using atomic replacement.

If the note model becomes large enough to justify a separate data file, do not overload general FlameWM settings with arbitrary multiline note contents.

## 9.9 Workspace changes

Notes follow the same deterministic workspace index transformations as desktop-specific shell objects:

- insertion before/after shifts indices consistently;
- removing a workspace moves notes on that workspace to the same destination policy used for user windows;
- notes above the removed index decrement.

Do not leave invisible/orphaned notes on removed workspace IDs.

## 9.10 Disable semantics

V6 final says disabling Sticky notes **removes all sticky notes altogether**.

Therefore toggle-off is destructive to stored notes, not merely hidden presentation.

Native Settings should make this clear with concise copy such as:

```text
Disabling removes all notes.
```

The destructive action should be intentional. If later product direction asks for temporary hiding instead, that is a different semantic and requires a new decision.

---

# 10. Taskbar context menu

Blank taskbar context:

```text
Create New Virtual Desktop
--------------------------
Taskbar Settings…
```

Only blank/non-control area opens this menu.

Right-clicking:

- pinned app -> pinned-app context (`Unpin` only under current product rule);
- running non-pinned app -> task context;
- workspace -> workspace context;
- status/clock -> their own behavior;
- blank taskbar -> taskbar context.

Do not let parent taskbar context handling swallow child-specific context menus.

---

# 11. Workspace creation ownership and one-workspace hiding

## 11.1 Desktop context no longer owns workspace creation

Remove `Add Virtual Desktop` from desktop context.

Why:

- workspace management is taskbar/workspace state;
- desktop filesystem context should stay about desktop content/background;
- duplicate creation paths add clutter without improving discoverability.

## 11.2 Taskbar creates workspace

Blank taskbar menu `Create New Virtual Desktop` uses the same IceWM workspace transaction as pager context actions.

No second workspace count variable.

## 11.3 Hide pager at one workspace

Exact behavior:

```text
workspace count == 1 -> pager consumes zero visible panel space
workspace count >= 2 -> pager appears using FlameWM two-row topology
```

Do not render a lonely `1` merely to prove workspaces exist.

The model still has workspace 1; only its redundant indicator is hidden.

After creating workspace 2, pager appears immediately.

After removing back to one, it disappears immediately.

---

# 12. Taskbar Settings — final V6 fields

Page controls:

```text
Color
Opacity
Height
Start button text
Start button icon
```

## 12.1 Taskbar color

- semantic user color;
- live apply;
- persist as validated RGB/hex color;
- does not alter arbitrary application windows.

## 12.2 Opacity

V6 prototype allows 0–100%.

Native product must distinguish capability:

- with real alpha/compositor-capable path, honor requested opacity;
- without a correct transparency path, do not lie by exposing a control that has no visible effect;
- compositor-free pseudo-transparency can be implemented later using root wallpaper data if chosen.

The prototype demonstrates the desired user control, not a guarantee that X11 without a compositor can alpha-blend every panel surface.

## 12.3 Logical height

Height is a logical FlameWM panel metric.

Changing it must update:

- panel geometry;
- panel child hit targets/icons as defined by metrics;
- EWMH struts/work areas;
- desktop grid usable area;
- sticky-note bounds;
- window work-area constraints;
- Start/popover anchoring.

Do not merely paint a taller background while leaving old work areas.

## 12.4 Custom Start icon

Default remains approved FlameWM icon.

User may select a custom local image/vector.

Native security/robustness rules:

- decode as image data; never execute it;
- reject unsupported/corrupt files visibly;
- retain aspect ratio;
- scale through semantic Start-icon size;
- copy/import to FlameWM-owned config/data path or persist a stable URI/path according to final config policy;
- if source disappears, fall back to FlameWM icon rather than blank Start.

## 12.5 Optional Start text

If non-empty:

```text
[text] [icon]
```

Text is explicitly to the **left** of the icon.

If empty, Start remains icon-only.

Text must not alter the action semantics or create separate click targets.

---

# 13. Appearance icon-theme selection

## 13.1 Default

```text
FlameWM Breeze (Built-in)
```

This means FlameWM ships/chooses its curated Breeze-compatible baseline and packaged critical fallbacks.

## 13.2 Native enumeration

The browser prototype lists representative system themes because a normal webpage cannot safely enumerate host icon-theme directories.

Native `flamewm-settings` should enumerate installed freedesktop themes from standard icon-theme locations and `index.theme` metadata, while respecting `Hidden=true` and user-visible theme names.

Standard base directories include the freedesktop locations used by the system, and lookup must retain inherited theme and `hicolor` fallback semantics.

## 13.3 Reuse IceWM `YIcon`

Correct architecture:

```text
Settings selects theme name
-> Flame config persists theme choice
-> runtime updates IceWM/Flame icon-theme preference/policy
-> YIcon cache/theme generation invalidated safely
-> shell surfaces repaint/re-resolve icons
```

Wrong architecture:

```text
Settings scans themes
-> separate FlameIconLoader independently implements theme inheritance
-> taskbar uses one lookup engine
-> IceWM menus use another
-> inconsistent/missing icons
```

## 13.4 Flame-critical fallbacks

Regardless of selected system theme, shell-critical FlameWM actions must have a safe fallback:

- Start;
- window controls;
- settings categories;
- power/session;
- network/audio/media;
- workspace/taskbar actions.

A third-party theme that omits one icon must not make a core control invisible.

## 13.5 Live apply

Icon theme changes should repaint/re-resolve immediately when safe.

Do not require logout merely to change icon theme if the cache can be invalidated correctly.

---

# 14. Concise Settings copy rule

V6 generalizes one UX lesson: permanent help text should explain the next action, not document the implementation.

Good:

```text
Fonts: Choose the desktop font.
Displays: Select a display to configure it.
Hotkeys: Click a shortcut and press the new combination.
Appearance: Colors and icons.
```

Avoid paragraphs that explain:

- storage behavior;
- browser simulation;
- how reset works;
- exact internal implementation;
- all supported edge cases.

Put deep explanation in documentation/tooltips only where needed.

A Settings page is a control surface, not a manual.

---

# 15. V6 About contract

Visible identity:

```text
[FlameWM logo]
A lightweight desktop by ArkFlame Studios
```

Centered actions:

```text
Donate       -> https://paypal.me/LinsaFTW
Source Code  -> https://github.com/arkflame/flamewm
Website      -> https://wm.arkflame.com
```

Native implementation must launch external URIs through a safe desktop URL-opening mechanism.

Do not construct a shell command by concatenating an unquoted URL/string.

Brand icons must preserve their applicable license/brand usage requirements. Shell product icons remain separate from third-party brand icons.

---

# 16. State ownership matrix for V6 additions

| Behavior | Native authority | Notes |
|---|---|---|
| Managed windows/focus | IceWM `YWindowManager` / frames | Never duplicate |
| Workspace count/index | IceWM manager | Flame UX issues transactions |
| Task states | IceWM task/frame state | Flame renders them |
| Start application model | Reused/extracted XDG/FDO model | Search is Flame presentation |
| Start open panel | Flame panel manager + IceWM taskbar host | Output-aware |
| Audio state | Pulse integration | UI owns slider interaction only |
| Icon theme selection | Flame setting + existing `YIcon` resolution | No second resolver |
| Taskbar color/opacity/height | Flame settings/runtime | Must update real struts/geometry |
| Start custom icon/text | Flame settings/panel renderer | Product-owned |
| Desktop files/grid | `flamewm-desktop` | Separate process |
| Desktop selection | `flamewm-desktop` | Below normal windows |
| Sticky notes | `flamewm-desktop` | Separate from WM core |
| Sticky enable toggle | Flame settings -> desktop process | Off deletes notes under V6 contract |
| Window snap preview | WM-linked Flame snap controller | Separate overlay from desktop selection |
| System display modes | XRandR transaction authority | Rollback-safe |

---

# 17. Implementation sequence for V6-specific native work

V6 features should not be applied as one giant patch.

## Phase A — product settings schema

Add typed fields for:

```text
icon theme
taskbar color
taskbar opacity
taskbar logical height
custom Start icon
Start text
sticky notes enabled
```

Keep V5 fields for:

```text
accent
fonts
overlay opacities
hotkeys
display selection/scale
```

Tests:

- defaults;
- parse/serialize;
- invalid values;
- atomic persistence;
- unknown-key preservation if part of chosen schema.

## Phase B — launcher search mode

Implement pure filter/model behavior first, then wire to Start renderer.

Tests:

- empty query -> categories;
- non-empty -> results;
- clear -> categories;
- no stale submenu;
- keyboard navigation;
- launch correct desktop entry.

## Phase C — continuous input behavior

Audit every live Settings slider/color picker.

Prove active widget remains alive throughout drag and only affected product state changes.

## Phase D — taskbar settings/runtime

Apply color/height/opacity/text/icon with one typed delta path.

Height must integrate real panel geometry/struts before being called complete.

## Phase E — workspace pager visibility/taskbar context

Add blank-panel context and pager hide/show logic without changing workspace state authority.

## Phase F — desktop selection stacking

Verify desktop-layer window stacking against normal client frames and panel.

## Phase G — sticky notes

Implement model, persistence, renderer, editor, drag/resize, context settings, workspace migration and feature disable in `flamewm-desktop`.

## Phase H — icon-theme selection

Enumerate real installed themes in Settings and route selected theme through `YIcon`/Flame icon policy with safe fallbacks.

---

# 18. Native verification matrix

## 18.1 Start

- open Start -> categories visible;
- type one character -> category rows replaced;
- search header/results remain in same panel;
- clear -> categories restored;
- submenu closed while searching;
- result launch correct;
- Escape closes;
- Toggle Start targets active physical output.

## 18.2 Audio

- press slider center;
- drag beyond left -> 0;
- drag beyond right -> 100;
- continue outside slider child;
- release terminates grab;
- external audio changes update UI;
- active drag does not recreate slider widget.

## 18.3 Hotkeys

- default row has no reset icon;
- change binding -> reset appears;
- reset appears immediately left of assignment;
- symbolic icon white on dark theme;
- set exact default manually -> reset disappears;
- Escape -> Not assigned;
- reset unassigned customized row -> shipped default;
- X grab conflict surfaced.

## 18.4 Selection stacking

With one desktop selection drag overlapping the screen coordinates of a normal window:

- selected desktop entries update;
- selection rectangle is clipped/stacked beneath normal window;
- window remains visually unobscured;
- taskbar remains unobscured;
- sticky note remains above selection rectangle.

## 18.5 Sticky notes

- action visible only when enabled;
- create default yellow/black note;
- edit UTF-8 text;
- drag via invisible top strip;
- text selection inside body does not drag;
- resize within work area;
- right-click settings live-update background/text/text-size;
- delete note;
- workspace switch visibility;
- workspace insert/remove migration;
- panel edge/height changes clamp notes;
- resolution/output topology changes clamp/reassign safely;
- disable toggle deletes every note and removes context action;
- restart preserves notes while enabled.

## 18.6 Taskbar

- blank context shows only relevant panel actions;
- create desktop uses IceWM transaction;
- Taskbar Settings opens directly;
- color changes continuously;
- opacity changes continuously when runtime capability exists;
- height changes continuously without killing Settings interaction;
- work area/struts update;
- custom icon loads/falls back;
- Start text precedes icon;
- four-edge docking remains valid.

## 18.7 Workspace pager

- one workspace -> zero visible pager area;
- create second -> pager appears;
- remove second -> pager disappears;
- current workspace state itself never becomes zero/missing.

## 18.8 Icon themes

- installed theme list sourced from actual system metadata;
- selected theme persists;
- shell icons repaint;
- inherited/fallback icon lookup works;
- missing core icon falls back to FlameWM/Breeze packaged asset;
- dark/light symbolic contrast remains correct;
- hicolor fallback remains intact.

---

# 19. Prototype verification closure

The packaged V6 reference has been checked with:

- `node --check app.js`;
- unique HTML IDs;
- all current `iconDefs` asset references present/non-empty;
- exact final external URLs;
- semantic headless Chromium execution by injecting the packaged HTML/CSS/JS into an isolated browser document because direct local/network navigation is restricted in the execution environment;
- no page/JavaScript console errors in that semantic run.

The semantic browser run covered:

- in-menu Start search / clear restoration;
- audio drag beyond both slider ends;
- live accent application;
- icon-theme selection state;
- Hotkeys reset visibility/order/white contrast and Escape unassignment;
- live taskbar height/opacity without replacing Settings DOM;
- custom Start text and custom SVG icon;
- selection/sticky/window/taskbar z-order;
- sticky creation/editing/appearance/dragging;
- disabling Sticky notes deletes notes and removes the action;
- blank taskbar context;
- workspace creation/removal behavior and one-workspace pager suppression;
- exact About destinations.

Browser limitations are not native implementation proof. Native X11/XRandR/D-Bus/libpulse/filesystem functionality must pass the native gates above before release.

---

# 20. Final implementation principle

The V6 prototype is intentionally richer than a theme but narrower than a full desktop-environment framework.

The final native product should remain:

```text
IceWM mature engine
+ FlameWM product shell
+ FlameWM desktop process
+ event-driven standard Linux integrations
+ simple settings
+ strong defaults
```

Not:

```text
IceWM
+ duplicated managers
+ embedded web runtime
+ widget framework
+ polling helper zoo
+ Plasma-sized dependency surface
```

The goal is still the same: **make IceWM feel finished without making it heavy.**
