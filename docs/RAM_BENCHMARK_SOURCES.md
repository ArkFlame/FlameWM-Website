# Side by Side RAM Usage — sources and measurement boundaries

Updated 2026-10-21.

## FlameWM

- ~17 MB: internally reported resident-set size (RSS) of the FlameWM window-manager process.
- No measurement log or exact test environment was supplied to this website rebuild. The value is **preliminary and unverified externally**.
- Not a measurement of a complete FlameWM login session, distribution, X server, Linux kernel, display manager, background services or application set.

## Ubuntu 26.04 desktop idle measurements

Source: [ComputingForGeeks, Oct 12 2026](https://computingforgeeks.com/desktop-environment-ram-usage/) — published same-base Ubuntu 26.04 VM comparison. Whole-system idle RAM, medians of nine readings over three cold boots.

| Desktop | Idle RAM used (MiB) |
|---|---:|
| LXQt | 745 |
| Budgie | 806 |
| MATE | 835 |
| Xfce | 888 |
| GNOME | 894 |
| Cinnamon | 960 |
| KDE Plasma | 1,209 |

## IceWM (separate source)

Source: [Q4OS forum / Q4OS team, June 2025](https://www.q4os.org/forum/viewtopic.php?pid=29965): IceWM 288 MB after second login, 4 minutes uptime, in VirtualBox with Q4OS 5.8. This is not the Ubuntu test. The website labels its Q4OS origin alongside the other entries.

## Publication rules

- Never compare 17 MB *process RSS* directly against 745–1,209 MiB *complete system idle* as if measured identically.
- Do not claim a verified global lightest-desktop record without controlled end-to-end same-machine testing.
- Brand emblems are not performance evidence. Source figures may differ with distro, VM, drivers, package set, cache, start-up services and tool.
- Test all systems on the same OS/hardware and publish process PSS, session PSS, whole-system idle, Xorg/Wayland resource use, startup and idle wakeups before publishing a controlled ranking.

### Presentation decision

The website shows nine entries in one visual chart. Each entry states its measurement type: **Window manager** for FlameWM (process RSS), **Q4OS** for IceWM (system idle), and **System idle** for the Ubuntu desktop results. The shared visual scale does not make the measurements equivalent or prove an end-to-end FlameWM memory advantage.
