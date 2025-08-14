#!/usr/bin/env bash

# I had an issue where sometimes `update_containers.sh` did not work so I wrote this simple script to make sure they all get updated excluded the bad container

mapfile -t services < <(docker compose ps --services)

for service in "${services[@]}"; do
    echo "Updating service: $service"
    docker compose pull "$service"
    docker compose up -d "$service"
done

# Prune images after all updates
docker image prune -f
