// User-provided FlameWM RSS and external published idle-system measurements.
// IMPORTANT: Do not use these different scopes to claim comparable performance.
export const benchmarks = [
  { id: 'flamewm', name: 'FlameWM', value: 17, source: 'internal', kind: 'WM process RSS', icon: 'F', color: '#f35058' },
  { id: 'icewm', name: 'IceWM', value: 288, source: 'q4os', kind: 'Q4OS 5.8 idle system', icon: 'I', color: '#8baad7' },
  { id: 'lxqt', name: 'LXQt', value: 745, source: 'ubuntu', kind: 'Ubuntu 26.04 idle system', icon: 'L', color: '#43c0b6' },
  { id: 'mate', name: 'MATE', value: 835, source: 'ubuntu', kind: 'Ubuntu 26.04 idle system', icon: 'M', color: '#8ab77d' },
  { id: 'xfce', name: 'Xfce', value: 888, source: 'ubuntu', kind: 'Ubuntu 26.04 idle system', icon: 'X', color: '#91b7f1' },
  { id: 'gnome', name: 'GNOME', value: 894, source: 'ubuntu', kind: 'Ubuntu 26.04 idle system', icon: 'G', color: '#93afea' },
  { id: 'cinnamon', name: 'Cinnamon', value: 960, source: 'ubuntu', kind: 'Ubuntu 26.04 idle system', icon: 'C', color: '#d19b70' },
  { id: 'plasma', name: 'KDE Plasma', value: 1209, source: 'ubuntu', kind: 'Ubuntu 26.04 idle system', icon: 'K', color: '#a79ee6' },
] as const;

export const sources = {
  ubuntu: 'https://computingforgeeks.com/desktop-environment-ram-usage/',
  q4os: 'https://www.q4os.org/forum/viewtopic.php?pid=29965',
} as const;
