# >> [Community Scripts](https://community-scripts.github.io/ProxmoxVE/scripts) <<
  Scripts can usually be updated by running `update` in the LXC Console.   
  All LXCs run Debian, except specified.
# Pihole
# Vaultwarden
# Immich
## Important Files
Environment file: `/opt/immich/.env`
Log files: `/var/log/immich` (`web.log`, `ml.log`)
## Change Layout (Upload Location)
- Edit in the `.env` file the entry `IMMICH_MEDIA_LOCATION`.
- Create Symlink in `/opt/immich/app` & `/opt/immich/app/machine-learning` to new location. (`ln -s TARGET NAME`)
- Copy all the stuff over
- Make sure the permissions are correct (`chown -R user:group`)
## Setting up Remote ML
In the docker-compose.yml on your ML-Server, make sure you expand the line containing `image: ...:${IMMICH_VERSION:-release}` with `-cuda` or whatever flavour of ML-Architecture you're using
# Listmonk
# Cockpit
# Jellyfin
# Navidrome
# Factorio
# Minecraft (Ubuntu)
## Why Ubuntu?
Java. Newest Java version wasn't easily available on Debian, and thus Ubuntu had to resolve this.
## Important Files
- `server.jar` (the Minecraft server) at `/opt/minecraft/server/server.jar`
- Backups: `/opt/minecraft/backups`
