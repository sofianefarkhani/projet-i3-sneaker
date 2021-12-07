# Projet I3 : SNEAKERS
## Requirements
### With Docker
* Docker Engine (>= 19.03.0+)
### Without Docker
* Python (>= 3.8)
* pip
## Configuration
### IP Forward for containers (Linux kernel)
1. Configure the Linux kernel to allow IP forward
```bash
sysctl net.ipv4.conf.all.forwarding=1
```
2. Change the policy for the ```iptables``` ```FORWARD``` policy from ```DROP``` to ```ACCEPT```
```bash
sudo iptables -P FORWARD ACCEPT
```
## Installation
For installing, we recommande to use script deploy.sh. 
### Create container
For generate one container you write command bellow :
```bash
./deploy.sh --create
```
### Delete container
For delete all containers generate by this script I just use argument --drop.
```bash
./deploy.sh --drop
```
### Reboot container
If you wish reboot all containers, you use argument --start.
```bash
./deploy.sh --start
```
### Informations on container
For collect informations of all containers you use --infos.
```bash
./deploy.sh --infos
```
## Usage
