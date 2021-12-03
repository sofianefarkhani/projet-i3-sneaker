#!/bin/bash

########################################################
#
#   Description : script use for deploy containers
#
#   Author : Sofiane FARKHANI
#
#   Date : 03/12/2021
#
########################################################

#############################################################
#
# Functions
#
#############################################################

# Documentation
help() {
echo "
    Options :
        * --create  : creation of the container
        * --drop    : delete all containers create by this script
        * --run   : reboot all containers
        * --infos   : informations of the containers
        * --help    : documentation
"
}

# Create container
create() {
    echo -e "Creation of the containers:\n"

}

# Drop all containers
drop() {
   echo -e "Drop all of the containers:\n"
   docker rm -f $(docker ps -a | grep "sneakers" | awk '{print $1}')
   echo -n "End of drop"
   echo -n ""
}

# Reboot containers
run() {
    echo -e "Run containers\n"
    docker start $(docker ps -a | grep "sneakers" | awk '{print $1}')
    echo -n ""

}


# Print informations of the containers create by deploy.sh
infos() {
    echo -e "Informations of containers:\n"
    for containers in $(docker ps -a | grep "sneakers" | awk '{print $1}');do
        docker inspect -f ' => {{.Name}} - {{.State.Status}}' $containers
    done
    echo -n ""

}


#############################################################
#
# Main
#
#############################################################

case "$1" in
    "--create")
        create;
        ;;
    "--drop")
        drop;
        ;;
    "--run")
        run;
        ;;
    "--infos")
        infos;
        ;;
    "--help")
        help;
        ;;
    *)
        echo -n "Error : your choice is not valid."
        ;;
esac