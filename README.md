# Git pace

A local web page that shows how much work went into a git repository over time.

    python gitpace.py path/to/repo

It opens the browser at `http://127.0.0.1:8765/` (or a free port if 8765 is taken; the address is printed).
Standard library only; the page has no outside dependencies. **Refresh** reads the history again.

What the page shows, for the chosen period (All / 24 h / 7 / 30 / 90 days, or a stretch dragged on the bar chart):

- **Totals:** commits, lines added and removed, work sessions, active time, lines changed per active hour.
- **Bars:** lines changed (by top-level folder, three biggest + Other) or commits, per 15 min / hour / day / week / month.
  One huge bar (an initial import) is cut and labelled so it does not flatten the rest.
- **Work sessions:** commits closer than the "session break" belong to one session. A session's length is
  first to last commit, so the time before the first commit of a session is not counted.
- **Size of the code:** added minus removed lines, all time.
- **Commits** in the period, newest first.

Merge commits are left out. Binary files count as 0 lines.
