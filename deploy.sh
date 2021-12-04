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
        * --start   : reboot all containers
        * --infos   : informations of the containers
        * --help    : documentation
"
}

# Create container
create() {
    echo -e "Creation of the containers:\n"

    # Test docker image exist
    if [[ "$(docker images -q sneakers 2> /dev/null)" == "" ]];then
        docker build --tag sneakers .
    fi

    # Number of containers
    nbContainers=1

    # Setting min and max
    min=1
    max=0

    # Get max value of id
    idmax=`docker ps -a --format '{{.Names}}' | awk -F "-" -v user="$USER" '{print $3}' | sort -r | head -1`

    # Redefine min and max
    min=$(($idmax + 1))
    max=$(($idmax + $nbContainers))

    for i in $(seq $min $max);do
        docker compose up
    done
    infos

}

# Drop all containers
drop() {
   echo -e "Drop all of the containers:\n"
   docker rm -f $(docker ps -a | grep "sneakers" | awk '{print $1}')
   echo -n "End of drop"
   echo -n ""
}

# Reboot containers
start() {
    echo -e "Reboot containers\n"
    docker run $(docker ps -a | grep "sneakers" | awk '{print $1}')
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
    "--start")
        start;
        ;;
    "--infos")
        infos;
        ;;
    "--help")
        help;
        ;;
    *)
        echo -e "Error : your choice is not valid.\n";
        ;;
esac