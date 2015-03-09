import os
from os import system as cmd

import fileinput

if os.geteuid() != 0:
    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.\n")

cmd("apt-get install dhcp3-server tftpd-hpa syslinux nfs-kernel-server initramfs-tools");

cmd("service isc-dhcp-server start")
cmd("/etc/init.d/tftpd-hpa start")

subnet_ip=raw_input("Enter your subnet ip: ")
subnet_mask=raw_input("Enter your subnet mask: ")

print "\nEnter Range of local IPs: " 

start=raw_input("Start: ")
end=raw_input("End: ")

#this will only work if you do not already have a dhcp server on your network. If there is one, add a "next-server" tag to its config file to point to this system.

wfile=open("/etc/dhcp/dhcpd.conf","w")
wfile.write("allow booting;\nallow bootp;\n\n");
wfile.write("subnet " + subnet_ip + " netmask " + subnet_mask +" {\n");
wfile.write("range " + start + " " + end)
wfile.write("filename \"/pxelinux.0\";\n}\n\n")
wfile.close()

wfile=open("/etc/default/tftpd-hpa","w")
wfile.write("#Defaults for tftpd-hpa\nRUN_DAEMON=\"yes\"\nOPTIONS=\"-l -s /tftpboot\"\n")
wfile.close()

cmd("service isc-dhcp-server restart")
cmd("/etc/init.d/tftpd-hpa restart")

path=raw_input("Enter the path to your Ubuntu 14.04 (x86) ISO image: ")

cmd("mkdir mount_temp")
cmd("mkdir /var/www/ubuntu")

cmd("mount -o loop -t iso9660 " + path + " " + mount_temp)
cmd("cp -r ./mount_temp /var/www/ubuntu")

cmd("umount ./mount_temp")
cmd("rm -r ./mount_temp")

path=raw_input("Enter the path to the netboot directory (should also be named so): ")
cmd("cp -r " + path + "/var/lib/tftpboot/");

path=raw_input("Enter the path to the .ks file: ")
cmd("cp -r " + path + "/var/www/html/");

ip=raw_input("Enter your ip address: ")

for line in fileinput.input(path, inplace=True):
    print(line.replace("host_ip_address", ip))

wfile=open('/var/lib/tftpboot/netboot/ubuntu-installer/i386/boot-screens/txt.cfg','a')

wfile.write("\nlabel install\n")
wfile.write("\tmenu label ^Install (from local http server)\n")
wfile.write("\tmenu default\n")
wfile.write("\tkernel ubuntu-installer/i386/linux\n")
wfile.write("\tappend ks=http://"+ ip +"/ks.cfg vga=normal initrd=ubuntu-installer/i386/initrd.gz -- quiet\n")

wfile.close()

print "\n\nYour initial setup is over!!\n\nYou may now proceed to install ubuntu on your network connected machines.."


