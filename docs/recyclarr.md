# Recyclarr

Follow the Github for PlexTraktSync for more details. [https://github.com/Taxel/PlexTraktSync/tree/main](https://github.com/Taxel/PlexTraktSync/tree/main)

Specifically, read through [https://github.com/linuxserver-labs/docker-plextraktsync](https://github.com/linuxserver-labs/docker-plextraktsync) for this container.

This document is just what I did to setup PlexTraktSync in the docker container.

## Setup

If you choose to add recyclarr during the ezarr setup, you need to do a few more things to finish setting it up

After the `docker-compose.yml` file is created that contains recyclarr, inside the folder with that file run

```sh
docker-compose run --rm recyclarr config create
```

This will create a `recyclarr.yml` file inside your recyclarr config folder along with other necessary files.

We want to change the template of this `recyclarr.yml` file so delete it then replace it with this template. There's two templates listed below. Pick the one that works best for you.

You can always view this page to see all the profiles [https://recyclarr.dev/wiki/guide-configs/](https://recyclarr.dev/wiki/guide-configs/)

## Basic recyclarr.yml Template

[https://raw.githubusercontent.com/imjustleaving/ServersatHome/refs/heads/main/recyclarr.yml](https://raw.githubusercontent.com/imjustleaving/ServersatHome/refs/heads/main/recyclarr.yml)

Make sure to do all of this inside the `/config/recyclarr/` folder

```sh
rm recyclarr.yml

wget https://raw.githubusercontent.com/imjustleaving/ServersatHome/refs/heads/main/recyclarr.yml
```

## Nolan's recyclarr.yml Template that Includes Anime

[https://raw.githubusercontent.com/nolanwinsman/ezarr/refs/heads/main/templates/recyclarr.yml](https://raw.githubusercontent.com/nolanwinsman/ezarr/refs/heads/main/templates/recyclarr.yml)

Make sure to do all of this inside the `/config/recyclarr/` folder

```sh
rm recyclarr.yml

wget https://raw.githubusercontent.com/nolanwinsman/ezarr/refs/heads/main/templates/recyclarr.yml
```

## Edit recyclarr.yml

Now edit `recyclarr.yml` to include your sonarr/radarr URLs and their API keys which you find in the General Settings.

## Run Recyclarr Sync

Run this command to sync recyclarr with Sonarr and Radarr

```sh
docker-compose run --rm recyclarr sync
```
