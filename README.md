# Project Compass — Version 1

A Windows-friendly **local-first** project dashboard that runs without a subscription or third-party Python libraries. This is an initial working version, not yet the final cloud/AI application.

## Start (Windows 11)

1. Unzip the folder somewhere permanent (for example `D:\Projects\ProjectCompass`).
2. Double-click **`start_windows.bat`**. Python 3 is required.
3. If no browser opens, visit **http://127.0.0.1:8765** in Chrome or Edge.
4. Leave the minimised server window running while you use the dashboard. Close the server window when finished.

Or, in a terminal from this folder: `python server.py`.

## Today’s workflow

- **Dashboard:** Your three pinned/highest priority projects, their completion, progress change over 7 days, and a line chart versus on-hold average.
- **Home:** Create and manage projects or ideas; use the search and filters.
- **Project details:** Update status, priority, progress, tasks, goals, notes, file-folder reference, and activity history.
- **Backup:** Click **Export JSON** regularly. Use **Import JSON** to restore/migrate projects later.
- Demo entries are clearly labelled **Example**. Replace or delete them when ready.

## Data safety

Your projects are stored in **`data/projects.sqlite3`** on your computer; the app listens only on **127.0.0.1**. No cloud service is used. To back up everything, use Export JSON and also copy the SQLite file after stopping the server.

**Limitations of V1:** This does not synchronise with your phone or cloud, run AI, inspect Windows files, send reminders, automatically start with Windows, or offer team collaboration. A Chrome/Edge browser window is used instead of a native desktop application. All those are future phases. Progress is entered manually in V1; the chart uses that history, not fabricated AI analysis. Window size/position is managed by your browser/OS and is not guaranteed to be restored in this version.

## Privacy

The starter is local and has no external API calls. Do not expose port 8765 to your network or the public internet. An authenticated, secure backend is required before cloud deployment or team use.

## Portability

`Export JSON` includes project details, tasks, progress history, notes, tags and activity records. Versioned JSON supports a future migration to Django/PostgreSQL without re-entering project information.

## Version 1.1 fix
- Use **Remove sample projects** on Dashboard/Home to clear only the four examples (keeps your own projects).
- Project Delete now uses an in-app confirmation instead of a browser popup.
- To update an existing installation, close Project Compass, extract the archive over your existing `ProjectCompass_V1` folder, and allow code files to be replaced. Do **not** delete the `data` folder; this update does not contain it.
