# PlexTraktSync

Follow the Github for PlexTraktSync for more details. [https://github.com/Taxel/PlexTraktSync/tree/main](https://github.com/Taxel/PlexTraktSync/tree/main)

This document is just what I did to setup PlexTraktSync in the docker container.

## Setup

If you choose to add PlexTraktSync during the ezarr setup, it will create a docker container that runs day in the middle of the night.

After the `docker-compose.yml` file is created that contains PlexTraktSync, inside the folder with that file run

```sh
docker compose run plextraktsync login
```

This script is fairly straightforward. It will ask for your Plex login details, trakt Client ID and Client Secret, then a few other basic questions and then it should be good to go.
