# Cloudflared

This setup is primarily for sharing your webpages outside of your network in clean http**s** pages anyone can access. Make sure you create a strong password for whatever applications you plan to share.

## Create Cloudflare account

Go to Cloudflare and create a free account [https://dash.cloudflare.com](https://dash.cloudflare.com)

## Add Domain to Cloudflare

This is quite easy and there's a lot of guides for this. I added my Squarespace Domain to Cloudflare.

## Tunnel Token

Create a new tunnel for your server then save the Tunel Token. Will be needed when ezarr is ran or needs to be added to the `docker-compose.yml` after

## Login

Assuming your Tunnel Token is correct, the first step after running `docker compose up -d` with cloudflared is to login

```sh
docker exec -it cloudflared cloudflared tunnel login
```

This will give you a link to login and authorize your machine. It will also install a certificate

## Addings Tunnel Routes

For now, I only want to expose Jellyfin so I created the route `jellyfin.mydomainname.com` and mapped the Service URL to `http://jellyfin:8096`

Now I can access `jellyfin.mydomainname.com` from any machine on any network.
