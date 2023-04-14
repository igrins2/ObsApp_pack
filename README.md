### Installation for ObsApp ### 

1. Download "ObsApp_pack" directory from GitHub.


2. Setup the python library

$ cd $HOME/ObsApp_pack/installation
$ sh ObsApp_setup.sh

After setup finished, exit the current terminal, open new terminal


3. Set nfs mount
dcs: server / ics, TelOps: client
(S-192.168.1.100)

IGRINS setting directory - $HOME/IGRINS

# dnf install nfs-utils nfs4-acl-tools

# showmount -e 192.168.1.100  //for dcss

# mount -t nfs 192.168.1.100:/home/dcss/DCS/Data $HOME/IGRINS/dcss

# mount | grep nfs

# echo "192.168.1.100:/home/dcss/DCS/Data     $HOME/IGRINS/dcss  nfs     defaults 0 0">>/etc/fstab
# cat /etc/fstab


4. Start software
if simulation:
	$ sh ../OpsApp_pack/run_ObsApp.sh True
else:
	$ sh ../OpsApp_pack/run_ObsApp.sh



