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
		
		**S-192.168.1.200**

	- ObsApp setting directory - $HOME/ObsApp
	```
	# dnf install nfs-utils nfs4-acl-tools
	# showmount -e 192.168.1.200
	# mount -t nfs 192.168.1.200:/home/dcss/DCS/Data $HOME/ObsApp/dcss
	
	# mount | grep nfs
	
	# echo "192.168.1.200:/home/dcss/DCS/Data     $HOME/ObsApp/dcss  nfs     defaults 0 0">>/etc/fstab
	# cat /etc/fstab
	```
4. Start software
	- If simulation
	```
	$ sh ../OpsApp_pack/run_ObsApp.sh simul
	```
	- Else
	```
	$ sh ../OpsApp_pack/run_ObsApp.sh obs
	```

5. For testing in simulation mode
   	- $HOME/IGRINS in ICS
   	  
 	Please check in $HOME/IGRINS/Config/IGRINS.ini"
	```
 	[MAIN]
	...
	simulation = True
 	```
   	Please start virtual hardware components.
 	```
  	(base) [ics@localhost ~]$ cd ics_pack/
	(base) [ics@localhost ics_pack]$ ls
	code  installation  README.md  run_ics.sh
	(base) [ics@localhost ics_pack]$ sh run_ics.sh 
	Usage: run_ics.sh {simul|eng|cli}
	(base) [ics@localhost ics_pack]$ sh run_ics.sh simul
	(lt) Listening to localhost:10006
	(ut) Listening to localhost:10007
	(pdu) Listening to localhost:50023
	(tmc1) Listening to localhost:10001
	(tmc2) Listening to localhost:10002
	(tmc3) Listening to localhost:10003
	(tm) Listening to localhost:10004
	(vm) Listening to localhost:10005
	Server loop running in thread: Thread-1
	Server loop running in thread: Thread-2
	Server loop running in thread: Thread-3
	Server loop running in thread: Thread-4
	Server loop running in thread: Thread-5
	Server loop running in thread: Thread-6
	Server loop running in thread: Thread-7
	Server loop running in thread: Thread-8
	Press enter to quit the server.
  	```
  	Please open another terminal and start **subsystem.service**.
	```
 	(base) [ics@localhost ics_pack]$ sudo systemctl start subsystem.service
	(base) [ics@localhost ics_pack]$ sudo systemctl status subsystem.service
	● subsystem.service - subsystem Service
	   Loaded: loaded (/etc/systemd/system/subsystem.service; enabled; vendor preset: disabled)
	   Active: active (running) since Fri 2023-07-14 14:51:51 KST; 2s ago
	 Main PID: 5798 (run_subsystem.s)
	    Tasks: 23 (limit: 204018)
	   Memory: 207.0M
	   CGroup: /system.slice/subsystem.service
	           ├─5798 /bin/bash /home/ics/ics_pack/installation/run_subsystem.sh
	           ├─6158 /home/ics/miniconda3/envs/igos2n/bin/python /home/ics/ics_pack/code/SubSystems/star>
	           ├─6159 python /home/ics/ics_pack/code/SubSystems/temp_ctrl.py 1
	           ├─6160 python /home/ics/ics_pack/code/SubSystems/temp_ctrl.py 2
	           ├─6161 python /home/ics/ics_pack/code/SubSystems/temp_ctrl.py 3
	           ├─6162 python /home/ics/ics_pack/code/SubSystems/monitor.py 4
	           ├─6163 python /home/ics/ics_pack/code/SubSystems/monitor.py 5
	           ├─6164 python /home/ics/ics_pack/code/SubSystems/pdu.py
	           └─6165 python /home/ics/ics_pack/code/SubSystems/DB_uploader.py
	
	Jul 14 14:51:51 localhost.localdomain systemd[1]: Started subsystem Service.
 	```
 	And then, you can see the communication status in previous terminal.
	```
	 data received tmc1: [KRDG? B
	] 9
	response sent tmc1: [+130.79
	]
	data received tmc3: [HTR? 2
	] 8
	response sent tmc3: [+21.0
	]
	data received tmc2: [HTR? 1
	] 8
	response sent tmc2: [+80.0
	]
	data received tmc1: [HTR? 1
	] 8
	response sent tmc1: [+05.0
	]
	data received tmc3: [SETP? 2
	] 9
	response sent tmc3: [+65.000
	]
	data received tmc2: [HTR? 2
	] 8
	response sent tmc2: [+00.0
	]
	data received tmc1: [HTR? 2
	] 8
	response sent tmc1: [+15.0
 	```
	- $HOME/DCS in DCSS

	Please check the **IAM = "DCSS"** for simulation test in $HOME/dcs_pack/code/DetCtrl/DC_def.py.
	
	(It will be removed for the future)

	Please check in $HOME/DCS/DCS.ini".
	```
 	[ICS]
	ip_addr = 192.168.1.203
	id = igos2n
	pwd = kasi2023
	...
 
	[DCSS]
	ip_addr = 192.168.1.100
	sn = 26
	myid = igos2n (RabbitMQ Server is in ICS and if DCS is in same system with ICS)
	pwd = kasi2023
 	...
 	```
	Please open new terminal and start **dc-core.service**.
	```
 	(base) [ics@localhost ~]$ sudo systemctl start dc-core.service
 	(base) [ics@localhost ~]$ sudo systemctl status dc-core.service 
	● dc-core.service - DC-core Service
	   Loaded: loaded (/etc/systemd/system/dc-core.service; disabled; vendor preset: disabled)
	   Active: active (running) since Fri 2023-07-14 15:04:35 KST; 3s ago
	 Main PID: 7417 (run_dc_core.sh)
	    Tasks: 2 (limit: 204018)
	   Memory: 77.0M
	   CGroup: /system.slice/dc-core.service
	           ├─7417 /bin/bash /home/ics/dcs_pack/installation/run_dc_core.sh
	           └─7452 /home/ics/miniconda3/envs/dcs/bin/python /home/ics/dcs_pack/code/DetCtrl/DC_core.py
	
	Jul 14 15:04:35 localhost.localdomain systemd[1]: Started DC-core Service.
	Jul 14 15:04:35 localhost.localdomain run_dc_core.sh[7417]: net.core.rmem_max = 134000000
	Jul 14 15:04:36 localhost.localdomain run_dc_core.sh[7417]: success
	(base) [ics@localhost ~]$ sudo systemctl status dc-core.service 
	● dc-core.service - DC-core Service
	   Loaded: loaded (/etc/systemd/system/dc-core.service; disabled; vendor preset: disabled)
	   Active: active (running) since Fri 2023-07-14 15:04:35 KST; 19s ago
	 Main PID: 7417 (run_dc_core.sh)
	    Tasks: 11 (limit: 204018)
	   Memory: 198.8M
	   CGroup: /system.slice/dc-core.service
	           ├─7417 /bin/bash /home/ics/dcs_pack/installation/run_dc_core.sh
	           └─7452 /home/ics/miniconda3/envs/dcs/bin/python /home/ics/dcs_pack/code/DetCtrl/DC_core.py
	
	Jul 14 15:04:35 localhost.localdomain systemd[1]: Started DC-core Service.
	Jul 14 15:04:35 localhost.localdomain run_dc_core.sh[7417]: net.core.rmem_max = 134000000
	Jul 14 15:04:36 localhost.localdomain run_dc_core.sh[7417]: success
	Jul 14 15:04:51 localhost.localdomain run_dc_core.sh[7417]: queueName= 'amq.gen-HuWey7XYPMA4Ls4Qs7ZXM>
	Jul 14 15:04:51 localhost.localdomain run_dc_core.sh[7417]: queueName= 'amq.gen-vVgyWbPxMBzL7NBoTC6qh>
	Jul 14 15:04:51 localhost.localdomain run_dc_core.sh[7417]: queueName= 'amq.gen-RLkw1i--FWoi90aNLm2yX>
	Jul 14 15:04:51 localhost.localdomain run_dc_core.sh[7417]: queueName= 'amq.gen-c25-I5vUcBhWA3F8R9Zhk>
	Jul 14 15:04:51 localhost.localdomain run_dc_core.sh[7417]: queueName= 'amq.gen-PMIn2owpPu6-gnczMRoLO>
	lines 1-18/18 (END)
	```
   	Since dc-core.service connects to RabbitMQ Server after recognizing its own MACIE board (around 10s),

   	you need to wait until you see the connection message such as queueName=~.
	- $HOME/ObsApp in TelOps(?)

	Please check the ip address of RabbitMQ in $HOME/ObsApp/ObsApp.ini.
	```
	...
 	[MAIN]
 	...
 	ip_addr = 192.168.1.203
	id = igos2n
	pwd = kasi2023
 	```
	Please start ObsApp. 	
	```
	(base) [ics@localhost ~]$ cd ObsApp_pack/
	(base) [ics@localhost ObsApp_pack]$ ls
	code  installation  README.md  run_ObsApp.sh
	(base) [ics@localhost ObsApp_pack]$ sh run_ObsApp.sh
	Usage: run_ObsApp.sh {obs|simul}
	(base) [ics@localhost ObsApp_pack]$ sh run_ObsApp.sh simul
	queueName= 'amq.gen-NH3VxZRuFGv37MnUB3MAtQ'
	queueName= 'amq.gen--D9xEboviZ-K8QoEoBzXUw'
	queueName= 'amq.gen-F8yhz1preb-Ekcn4sF5wew'
	queueName= 'amq.gen-I4ttzGEGovKIy0YyrTyXPg'
	queueName= 'amq.gen-kOcPvhMKmqGXDeldhly0Gw'
	queueName= 'amq.gen-DKIZZhzVJCsEj71q_lKKCw'
	queueName= 'amq.gen-69G7hoJXay8fC7sVaWxLCQ'
	PySide6.QtCore.QRect(0, 0, 870, 662)
 	```
 	And then, you can see the pressure, temperature, and enabled "Exposure" button on ObsApp gui.
