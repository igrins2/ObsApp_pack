# Installation for ObsApp ### 

1. Download `ObsApp_pack` directory from GitHub.

2. Setup the python library
	```
	$ cd $HOME/ObsApp_pack/installation
	$ sh ObsApp_setup.sh
	```
	After setup finished, exit the current terminal, **open new terminal**!!!
3. Set nfs mount
	- dcs: server / ics, TelOps: client
		
		**S-192.168.1.11**

	- ObsApp setting directory - $HOME/ObsApp
	```
	# dnf install nfs-utils nfs4-acl-tools
	# showmount -e 192.168.1.11
	# mount -t nfs 192.168.1.11:/home/dcss/DCS/Data $HOME/ObsApp/dcss
	
	# mount | grep nfs
	
	# echo "192.168.1.11:/home/dcss/DCS/Data     $HOME/ObsApp/dcss  nfs     defaults 0 0">>/etc/fstab
	# cat /etc/fstab
	```
4. Start software
	- If simulation
	```
	$ sh ../OpsApp_pack/run_ObsApp.sh True
	```
	- Else
	```
	$ sh ../OpsApp_pack/run_ObsApp.sh
	```
