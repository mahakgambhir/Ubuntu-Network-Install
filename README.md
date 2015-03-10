# Ubuntu-Network-Install
Automatically install ubuntu over a local network


# Instructions 
To be run on an ubuntu machine to act as a server for the network.
Run init.py as the root user, and provide the required information.

Besides the provided files, you would need a x86 Ubuntu 14.04 ISO image file.

Clone the repository as:                                        
git clone https://github.com/mahakgambhir/Ubuntu-Network-Install

Move into the repository:                                       
cd Ubuntu-Network-Install

Run the python script:                                  
sudo python init.py

Supply the required information.
If you have a local DHCP server running, make sure that it has a 'next-server' entry pointing to your IP.

Now network book the workstation on which Ubuntu needs to be installed, and select the "Install (from local http server)" option once you have selected to install Ubuntu.
