# EZarr Permission Model

This document describes the group and user permission structure used in the EZarr setup to control access to media and configuration directories.

---

# Groups

## media_read
Read-only access to media libraries.

Used for:
- Streaming media
- Browsing libraries
- Media server read access (no file modifications)

---

## media_write
Full write access to media libraries and download pipeline.

Used for:
- Downloading content
- Renaming/moving files
- Importing media into libraries
- Managing folder structure under `/data`

---

# Users and Group Memberships

## Media Servers (Read-Only Access)

- jellyfin → media_read
- plex → media_read

---

## ARR Stack (Write Access - Media Automation)

These services manage and modify media files:

- sonarr → media_write
- radarr → media_write
- lidarr → media_write
- readarr → media_write
- mylar → media_write
- bazarr → media_write
- audiobookshelf → media_write

---

## Downloaders (Write Access Required)

These services write to incomplete/complete download folders:

- qbittorrent → media_write
- sabnzbd → media_write
- unpackerr → media_write

---

## Indexers (No Media Filesystem Access)

These services do not access media storage:

- prowlarr → no filesystem access
- jackett → no filesystem access

---

## Request / Automation Services (No Media Access)

These services only interact via APIs:

- jellyseerr → no filesystem access
- overseerr → no filesystem access

---

# Summary Model

- media_read → streaming-only services
- media_write → automation + download pipeline services
- no group → API-only services with no filesystem access

---

# Security Goal

This setup follows a least-privilege model:

- Media servers cannot modify files
- Downloaders are isolated to controlled write paths
- ARR stack handles all file organization
- Indexers and request services have no direct filesystem access
