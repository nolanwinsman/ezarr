# PlexTraktSync

Follow the Github for PlexTraktSync for more details. [https://github.com/Taxel/PlexTraktSync/tree/main](https://github.com/Taxel/PlexTraktSync/tree/main)

Specifically, read through [https://github.com/linuxserver-labs/docker-plextraktsync](https://github.com/linuxserver-labs/docker-plextraktsync) for this container.

This document is just what I did to setup PlexTraktSync in the docker container.

## Setup

If you choose to add PlexTraktSync during the ezarr setup, it will create a docker container that runs day in the middle of the night.

After the `docker-compose.yml` file is created that contains PlexTraktSync, inside the folder with that file run

```sh
docker exec -it plextraktsync plextraktsync
```

This script is fairly straightforward. It will ask for your Plex login details, trakt Client ID and Client Secret, then a few other basic questions and then it should be good to go.

Now it should be up and running

## Cron Scheduling

By default, plextraktsync will run every two hours. To change this, run

```sh
docker exec -it plextraktsync /bin/sh
```

```sh
vi /config/crontabs/abc
```

I changed mine to run every 12 hours.

```sh
# min   hour    day month   weekday     command
0 */12 * * * /usr/bin/with-contenv python3 -m plextraktsync
```