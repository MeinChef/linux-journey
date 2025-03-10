# This file contains everything I learned during the setup of my new Fedora Workstation System. <br />

## System <br />
### Autostart <br />

There is a way to autostart apps / execute commands at login, but it seems kind of difficult. 
See [Stackexchange](https://unix.stackexchange.com/questions/626969/fedora-33-run-command-or-script-at-startup) and [file-specifications](https://specifications.freedesktop.org/desktop-entry-spec/latest/)
---
### fstab <br />
Use UUID. \
Spaces in Folder/Drive names are `\040` \
Useful Tags: \
- windows_names - enforces Windows Naming on mounted partition, particularly useful for NTFS drives.\
- x-gvfs-show - adds an icon to the file explorer, to make the partitions easily accessible there.

---


## Gnome <br />
### Autostart <br />
Autostarting apps, the easiest is to install Gnome-Tweaks and Gnome-Extensions-app. For managing the extensions, the gnome extensions manager is advised.
A list of extensions can be found here: https://extensions.gnome.org/]
---
### Usericon

The user-icon on the lock-screen is located at /var/lib/AccountService/icons. The path to said icon is specified in /var/lib/AccountService/user/


## Steam / Proton <br />
### Drive-Specific Issues <br />
Some games refuse to work if they are not an ext4 drive (e.g. instead from a mounted NTFS drive).
Affected Games (that I installed and had to move):
- Borderlands GOTY
- Plate Up
- In Sink

You can't mount drives to your home directory, mount them to /media or whatever, and symlink the drives to your $HOME directory.

### Proton commands <br />
Write log: `PROTON_LOG=1 %command%`

### Game Specific Issues <br />
#### Borderland GOTY <br />
