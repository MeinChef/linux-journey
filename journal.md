# This file contains everything I learned during the setup of my new Fedora Workstation System. <br />

## GRUB <br />
### GRUB not recognizing root <br />
After I used Clonezilla to copy my installation from one HardDisk to another, 
I also used this opportunity to put my /home folder into a different partition.
 
Following that - to verify everything is working, I booted my system several times.
For some reason, when booting it up the next day, I found myself in GRUB, unable to boot.

[This Blog](https://www.linuxfoundation.org/blog/blog/classic-sysadmin-how-to-rescue-a-non-booting-grub-2-on-linux) and [this question thread](https://askubuntu.com/questions/883992/stuck-at-grub-command-line)  were extremely helpful when trying to troubleshoot<br />
At first I tried booting from GRUB, where I tried to manually select the root partition.
To have a look at all available Partitions, Hard drives...

```
grub> ls
```

Some natural-language partitions?, followed by a long list of partitions of the form (hd#,gpt#) 

```
grub> ls (hd0,gpt0)
```

Returns like: Linux Partition, ext2 (even though it should be ext4, well)

```
grub> ls (hd0,gpt0)/
```

lists the names of the folders in said partition
The goal is to find the root folder. When found, execute

```
grub> set root=(hd0,gpt1)
```

Instead of `<Tab>` you could also type the linux you found when ls-ing

```
grub> linux /vml<Tab> root=/dev/nvmne0n1p3
grub> initrd /in<Tab>
grub> boot
```

This, however did not lead to me booting into the OS. The bootup got stuck, and threw me in the emergency console, from which I couldn't recover. (I assume because of non-correct /home or /root)


---

### Using a live installation to recreate GRUB config files. <br />
I refused to give up on my installation, so I found myself browsing the forums, and stumbled upon [this thread](https://discussion.fedoraproject.org/t/repair-reinstall-grub-after-windows-11-update-dual-boot-fedora-f39/113155) <br />
Here, I should boot a live-system to `chroot` into my original installation - basically bypassing GRUB.
Doing all the steps correctly was not easy, and with the help from the thread I was able to actually change the root of my live-system to my original installation.

#### Change the root of the live-system <br />
The following chain of commands were how I got there

```
# fdisk -l 
```

This prints all of your drives, partitions and file systems. You should locate your `EFI`, `boot` and `root` partition. 
For me it was:
- /dev/nvme1n1p1 -> EFI
- /dev/nvme1n1p2 -> boot
- /dev/nvme1n1p3 -> root (btrfs, so I needed the subvolume "root" and not "home")

Mount root, boot and EFI (in this order)

```
# mount /dev/nvme1n1p3 /mnt -o subvol=root
# mount /dev/nvme1n1p2 /mnt/boot
# mount /dev/nvme1n1p1 /mnt/boot/efi
```

For the system to allow `chroot`, we also need a bunch of other filsystems

```
# for fs in proc sys run dev sys/firmware/efi/efivars ; do mount -o bind /$fs /mnt/$fs ; done
```

Aaaand 

```
# chroot /mnt
```

Huzzah! This is basically now the System I wanted to get to :) <br />
Now mount the leftovers from `/etc/fstab` with

```
# mount -a
```

and I was set for phase 2

#### Re-install GRUB and recreate config files <br />

A lot of the information is also in the [Fedora Docs - GRUB2 Bootloader](https://docs.fedoraproject.org/en-US/quick-docs/grub2-bootloader/)

Since my system is a UEFI system, I had to run

```
# dnf reinstall grub2-efi grub2-efi-modules shim-\*
```

But it failed, because of missing grub2-efi-modules
Thus after installing them

```
# dnf install grub2-efi-modules
# grub2-mkconfig -o /boot/grub2/grub.cfg
```

I recreated the config file.

I booted, but got still stuck in GRUB. Unable to boot.
After remounting, chroot and more googling, I added `GRUB_SAVEDEFAULT=false` to `/etc/default/grub`.
A `sync && reboot` booted successfully!

## System <br />

### Moving the installation across drives with clonezilla <br />
I used Linux now exclusively on my dual-boot machine with Windows for three months. 
Deciding I want to get rid of Windows and use the prescious SSD space on my more write-endurable for my Linux instead.

In preparation to cloning partitions, I had to delete any partition on nvme1n1, and create three partitions of the same size (could also have been bigger).

In Clonezilla using a part-to-part clone, making sure you select the right partition for the right things makes the cloning a breeze.
The only "issue" there is then that the partitions have the exact same UUID or Identifier. This means that from boot to boot the mounted partitions will be different. Often across drives.
As it seems the drive selected in BIOS will contain the mounted boot partition.

I changed the UUID of the `boot` and `fedora` partition (the UUID of a FAT partition is only inferred upon creation and can not be changed), to make them different from the others, and changed the boot priority in BIOS to match the drive selection.
**Don't forget to change `/etc/fstab` accordingly on the new partition**
After booting, I verified that all partitions worked, and deleted the EFI partition and verified again.

All partitions working, I deleted the "old" `boot` and `fedora`. And my sytem was transferred successfully!

### Moving `/home` to a different partition

Copy home to a backup location 

```
# rsync -aXs /home/. /path/to/destination/. --exclude='/*/.gvfs'
```

.gvfs is a file automatically created by gnome, and has been known to cause trouble in the past - excluding it is a safe bet and won't hurt.

Create a new partition for the home folder.
Copy the home folder with the same command.
Edit `/etc/fstab`, with the `/home` mountpoint now pointing to the new partition.


### Autostart <br />

There is a way to autostart apps / execute commands at login, but it seems kind of difficult.
See [Stackexchange](https://unix.stackexchange.com/questions/626969/fedora-33-run-command-or-script-at-startup) and [.desktop file-specifications](https://specifications.freedesktop.org/desktop-entry-spec/latest/)

---

### fstab <br />
Use UUID. \
Spaces in Folder/Drive names are `\040` \
Useful Tags: 
- windows_names - enforces Windows Naming on mounted partition, particularly useful for NTFS drives.\
- x-gvfs-show - adds an icon to the file explorer, to make the partitions easily accessible there.

---

## Gnome <br />
### Autostart <br />

Autostarting apps, the easiest is to install Gnome-Tweaks and Gnome-Extensions-app. For managing the extensions, the gnome extensions manager is advised.
[list of extensions](https://extensions.gnome.org/)

---

### Usericon
The user-icon on the lock-screen is located at `/var/lib/AccountService/icons`. The path to said icon is specified in `/var/lib/AccountService/user/`

---

## Steam / Proton <br />
### Drive-Specific Issues <br />
Some games refuse to work if they are not an ext4 drive (e.g. instead from a mounted NTFS drive).
Affected Games (that I installed and had to move):
- Borderlands GOTY
- Plate Up
- In Sink

You should not mount drives to your home directory, mount them to /media or whatever, and symlink the drives to your `$HOME` directory.

### Proton commands <br />
Write log: `PROTON_LOG=1 %command%`

### Game Specific Issues <br />
#### Borderland GOTY <br />
