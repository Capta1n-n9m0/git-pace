# Git pace

A small local web page that shows how much work went into a git repository over time: when the commits
happened, how many lines changed, in which folders, in how many work sessions, and how the code grew.

One Python file and one HTML file. No dependencies beyond Python and git, nothing to install, no data leaves
your machine.

## Quick start

    git clone <this repository>
    python git-pace/gitpace.py path/to/some/repo

Your browser opens the page. Press **Refresh** on the page after new commits; press Ctrl+C in the terminal to
stop the server.

Requirements: Python 3.7 or newer and `git` on the `PATH`. Works on Windows, macOS and Linux.

## Options

    python gitpace.py [REPO_PATH] [--port PORT] [--no-browser]

| Option         | Default | Meaning                                                                 |
|----------------|---------|-------------------------------------------------------------------------|
| `REPO_PATH`    | `.`     | The repository to look at (any folder inside it works).                 |
| `--port`       | `8765`  | Port to listen on. If it is taken or reserved, a free port is used.     |
| `--no-browser` | off     | Do not open the browser; just print the address.                        |

The address is always printed, for example `http://127.0.0.1:8765/`.

## What the page shows

Pick a period (All, 24 h, 7, 30 or 90 days) or drag across the bar chart to zoom into a stretch of time.

- **Totals:** commits, lines added and removed, work sessions, active time, and lines changed per active hour.
- **Bars:** lines changed or commits per 15 minutes, hour, day, week or month (chosen automatically, or by
  you). Lines changed are coloured by top-level folder: the three biggest folders over the whole history, the
  rest as "Other", so a folder keeps its colour whatever period you look at. When one bar is far taller than
  the rest (an initial import, a vendored library), it is cut and labelled with its value so it does not
  flatten everything else.
- **Work sessions:** commits closer together than the *session break* (45 minutes by default, adjustable)
  form one session. Each session is listed with its start, end, length, commits and lines changed.
- **Size of the code:** lines added minus lines removed, over the whole history.
- **Commits** in the period, newest first, with lines added and removed and the folders they touched.

Hover over anything for the numbers behind it. The page follows your system's light or dark theme and works
on a narrow screen.

### Picture report

**Picture report** draws the chosen period as one PNG that you can save or copy and paste into a chat, a
ticket or a timesheet: the totals, when the commits happened, the lines-changed bars with their values, the
size of the code, and the list of commits (oldest first, up to 300).

## How the numbers are counted

- History comes from `git log --no-merges --numstat` on the current branch, read fresh on every load.
- Merge commits are left out, so merged work is counted once, in its original commits.
- Binary files count as 0 lines. Renames count only the lines that changed.
- A session's length is from its first to its last commit. Time spent before the first commit of a session
  is not visible in git, so **active time is an underestimate**, and "lines per active hour" an overestimate.
  A session with a single commit has length zero.
- Commit times are author times, shown in your browser's time zone.

These are rough measures of activity, not of value: a deleted thousand lines can be the best work of the
week.

## Privacy and safety

The server listens on `127.0.0.1` only, so other machines on your network cannot reach it. It only reads
the repository (`git log`); it never writes to it. The page loads nothing from the internet: no fonts, no
scripts, no analytics.

## How it works

`gitpace.py` (Python standard library only) runs `git log` on each request to `/api/data` and returns the
commits as JSON: hash, time, author, subject, and lines added and removed per top-level folder. It also
serves `index.html`, which does everything else in plain JavaScript and inline SVG.

## Licence

See [LICENSE](LICENSE).
