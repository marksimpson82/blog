---
title: "Repairing a corrupt jellyfin.db file"
date: 2026-07-15T00:00:00+00:00
author: Mark Simpson
layout: single
tags:
  - dsm
  - jellyfin
  - nas
  - synology
---

**Note**: This blog post was hand-written -- I am not a robot 🤖🔫. I used Gemini to get direction on running the `sqlite3` command, though.

I recently encountered a problem where my Jellyfin media server stopped processing / displaying new media. For my particular case, it was a simple fix. 

At the time of writing, my Jellyfin version was: `10.11.11`

## Symptom: Recently added shows did not appear in the UI
The files were in place, and Jellyfin continued to (mostly) function, tracking watch progress and serving existing media. New media did not get picked up, though.

## Diagnosis
I'm running via a Synology NAS with DSM. To investigate, I looked at the Jellyfin logs:
- Open DSM container manager
- Open the running Jellyfin container
- Select 'logs' and examine the content

Your investigation will obviously look a bit different if you're running Jellyfin via other means, or if you have to `ssh` in to see the logs.

In my case, I saw numerous errors like:
```
Microsoft.Data.Sqlite.SqliteException (0x80004005): SQLite Error 11: 'database disk image is malformed'. 
```

Hmm, not too healthy-looking.

## Jellyfin version: YMMV
Recent versions of Jellyfin moved to a single database file called `jellyfin.db`. My version only has the single `.db` file, plus some old backup files present in the data directory.

If you're running an older version, you may have multiple database files to contend with.

## Fixing it
- Stop the Jellyfin service
- Open a ssh connection to the jellyfin host
- Navigate to the `jellyfin/config/data` directory
- Backup the main `jellyfin.db` file via: 
  - `mv jellyfin.db jellyfin.db.corrupt`
- Also take a note of the file permissions
- Backup all other `*.db*` files (including any `db-shm` and `db-wal` files), moving them out of the root data directory to a backup dir
- Run the SQLite dump command to extract the readable data into a SQL file:
  - `sqlite3 jellyfin.db.corrupt ".recover" | sqlite3 jellyfin.db`
- Import the extracted data into a new database file:
  - `sqlite3 jellyfin.db < dump.sql`
- Ensure the newly created `jellyfin.db` file has the correct ownership and permissions for the Jellyfin user, or whatever your old setup was using
  - I had to `chown` it, similar to `chown jellyfin:jellyfin jellyfin.db`
- Start the Jellyfin service
- Navigate to the Jellyfin UI using a web browser, then start a media scan and wait a while(tm)
- Confirm that the missing media appears

## I _really_ like Jellyfin
This was the first issue I've run into after a few years of Jellyfin bliss. Kudos to the maintainers.
