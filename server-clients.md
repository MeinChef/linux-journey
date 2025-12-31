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
## Folder Structure
```
/opt/factorio/
├── bin/
│   └── x64/
│       └── factorio          # Main Factorio executable (Linux 64-bit)
│
├── saves/
│   ├── autosave_*.zip        # Auto-saves
│   └── custom_name.zip       # Saved game
│
└── mods/
    └── any_mod.zip
```
## Update Routine
### Backup
From the Proxmox interface start a backup.
Ideally copy the save to a backup folder
### Stop the Service
```systemctl stop factorio```
### Update the binary
```rm /opt/factorio/bin/x64/factorio && wget -vO /opt/factorio/bin/x64/factorio https://factorio.com/get-download/stable/headless/linux64```
### Sync Mods
```rsync --delete --exclude-from=/home/$USER/.factorio/mod-exclude.txt -avze ssh /home/$USER/.factorio/mods/ user@example.com:/opt/factorio/mods/```
### Permissions
```chown -R factorio:factorio /opt/factorio```
### Start the Service
```systemctl start factorio```

# Minecraft (Ubuntu)
## Why Ubuntu?
Java. Newest Java version wasn't easily available on Debian, and thus Ubuntu had to resolve this.
## Important Files
- `server.jar` (the Minecraft server) at `/opt/minecraft/server/server.jar`
- Backups: `/opt/minecraft/backups`
