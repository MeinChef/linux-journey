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
# Listmonk
# Cockpit
# Jellyfin
# Navidrome
# Factorio
# Minecraft
