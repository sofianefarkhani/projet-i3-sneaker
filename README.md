# Projet I3 : SNEAKERS
## Requirements
### With Docker
* Docker Engine (>= 19.03.0+)
### Without Docker
* Python (>= 3.8)
* pip
## Configuration (if you use Docker)
### IP Forward for containers (Linux kernel)
1. Configure the Linux kernel to allow IP forward
```bash
sysctl net.ipv4.conf.all.forwarding=1
```
2. Change the policy for the `iptables` `FORWARD` policy from `DROP` to `ACCEPT`
```bash
sudo iptables -P FORWARD ACCEPT
```
### Set path for volumes
Volumes of the containers use env file for define path to access images and output files (json).
Variable for set path to images is `PATH_IMG` : 
```
PATH_IMG=/path/to/images
```
Variable for set path to locate directory to store json files is `PATH_OUT` :
```
PATH_OUT=/path/to/out/directory
```
## Installation
For installing, we recommande to use script deploy.sh. 
### Create container
For generate one container you write command bellow (`--create`) :
```bash
./deploy.sh --create
```
### Delete container
For delete all containers generate by this script I just use argument `--drop`.
```bash
./deploy.sh --drop
```
### Reboot container
If you wish reboot all containers, you use argument `--start`.
```bash
./deploy.sh --start
```
### Informations on container
For collect informations of all containers you use `--infos`.
```bash
./deploy.sh --infos
```
## Usage
Result of all treatment write in `data.json`.
```json
{
    "id": {
        "lstImg": [
            "id-1.jpg",
            "id-2.jpg"
        ],
        "style": "high",
        "mainColor": {
            "name": "Black",
            "rgb": [0, 0, 0]
        },
        "secondaryColor": {
            "name": "White",
            "rgb": [255, 255, 255]
        },
        "probaShoes": 0.94
    }
}
```