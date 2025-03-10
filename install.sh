#!/bin/bash
# elevated stuff
sudo /bin/bash << EOF
	# vscode
	rpm --import https://packages.microsoft.com/keys/microsoft.asc
	echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null 
	dnf check-update
	dnf install code

	# steam
	dnf install steam

	# flatpaks
	flatpak install flathub com.spotify.Client
	flatpak install flathub org.keepassxc.KeePassXC
	flatpak install flathub dev.vencord.Vesktop
	flatpak install flathub org.videolan.VLC
	flatpak install flathub io.ente.auth
	flatpak install flathub org.mozilla.Thunderbird
	flatpak install flathub org.gimp.GIMP
	
	# uninstall unneccesary preinstalled (gnome/fedora) apps
	dnf remove gnome-weather
	dnf remove gnome-contacts
	dnf remove gnome-maps
	dnf remove mediawriter
	dnf autoremove
EOF

# miniconda
mkdir $HOME/miniconda3/
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O $HOME/miniconda3/miniconda.sh
bash $HOME/miniconda3/miniconda.sh -b -u -p $HOME/miniconda3
rm $HOME/miniconda3/miniconda.sh
source $HOME/miniconda3/bin/activate
conda init --all
conda deactivate
conda config --set auto_activate_base false

# and venv setup for SNNs
conda create -n snn python=3.12
conda activate snn
pip install snntorch
