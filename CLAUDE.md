# Git pace — a local web page showing how much work went into a git repository over time

`README.md` is the user-facing description; keep it in step with the page.

## Files

- `gitpace.py` — the server, Python standard library only (3.7+). Runs `git log --no-merges --numstat` on
  each `/api/data` request and serves `index.html`. Binds to 127.0.0.1 only and never writes to the
  repository. If the port is taken or reserved (Windows reserves port ranges), it falls back to a free port
  and prints the address.
- `index.html` — the whole page: vanilla JS and inline SVG, no outside libraries, nothing loaded from the
  network. Colours are CSS tokens with light and dark values.

Keep it that way: no dependencies, no build step, two files.

## Run and check

    python gitpace.py path/to/repo [--port N] [--no-browser]

A change is done when it is checked in a real browser (headless Chrome is fine): the numbers match
`git log`, no console errors, and light, dark and a 500 px wide window all render. Check the tooltips,
drag-to-zoom, the period/bucket/measure switches, the session break, the size-chart crosshair and the
picture report if the change could touch them.

## Design choices

- A work session is commits closer than the "session break" (default 45 min); its length is first to last
  commit, so active time is an underestimate.
- Bars are coloured by top-level folder: the three biggest over the whole history, the rest as "Other", so a
  folder keeps its colour whatever period is shown.
- When the biggest bar is over 3x the third biggest, the scale follows the third and taller bars are cut and
  labelled with their value.
- Merge commits are left out; binary files count as 0 lines.

## Picture report

- Built as one SVG in the light palette and drawn to a PNG at 2x; Save PNG and Copy (clipboard).
- Uses the chosen period, folders and bars (auto: same rule as the page, so 15 min up to 30 hours). The
  picture widens to about 26 px per bar (1200 to 3200 px) so numbers fit; else they are written upwards, and
  bars thinner than 9 px get no numbers. Commits oldest first, capped at 300 rows. No work sessions in the
  report.
- The size axis is fitted to the period; when the period starts before the first commit, the line starts
  there.
