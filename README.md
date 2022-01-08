# Projet I3 : SNEAKERS 
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

## Requirements
### With Docker
* Docker Engine (>= 19.03.0+)
### Without Docker
* Python (>= 3.8)
* pip
## Configuration 
### Docker
#### IP Forward for containers (Linux kernel)
1. Configure the Linux kernel to allow IP forward
```bash
sysctl net.ipv4.conf.all.forwarding=1
```
2. Change the policy for the `iptables` `FORWARD` policy from `DROP` to `ACCEPT`
```bash
sudo iptables -P FORWARD ACCEPT
```
#### Set path for volumes
Volumes of the containers use env file for define path to access images and output files (json).
Variable for set path to images is `PATH_IMG` : 
```
PATH_IMG=/path/to/images
```
Variable for set path to locate directory to store json files is `PATH_OUT` :
```
PATH_OUT=/path/to/out/directory
```
### Application
[Configuration app documentation](config/config-doc.md)
## Installation
### Linux/MacOs
For installing, we recommande to use script `deploy.sh`. 
### Windows
For installing, we recommande to use script `deploy.ps1`.
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
    "idProduct": "BQ5448",
    "lstImg": [
        "BQ5448_001-3--30666212-defe-4130-b4c1-5e86c70becf8.png",
        "BQ5448_001-1--e7758f70-7776-4020-9102-21a1f5d7cb00.png",
        "BQ5448_001-2--7916f055-4b3e-45dc-a839-08c8caab2d3e.png"
    ],
    "style": "LOW",
    "Colorway": [
        {
            "mainColor": {
                "name": "ANTHRACITE",
                "rgb": [
                    48,
                    48,
                    48
                ]
            }
        },
        {
            "secondaryColor": {
                "name": "LICORICE",
                "rgb": [
                    37.5,
                    33.0,
                    33.0
                ]
            }
        }
    ],
    "probaShoes": 0.995
}
```