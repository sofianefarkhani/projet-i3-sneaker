<#######################################################################################
#
#   Description : script use for deploy containers with Windows
#  
#   Author : Sofiane FARKHANI
#
#   Date : 10/12/2021
#
#######################################################################################>

<#######################################################################################
#
#   Functions
#
#######################################################################################>
function Help
{
    Write-Host "
    Options :
        * --create  : creation of the container
        * --drop    : delete all containers create by this script
        * --start   : reboot all containers
        * --infos   : informations of the containers
        * --help    : documentation
    "
}

function Create
{
    Write-Host "Creation of the containers:"
    if ($(docker images -q sneakers) -eq "")
    {
        docker build --tag sneakers .
    }
    # Number of containers
    $nbContainers=1

    for ($i = 0; $i -lt $nbContainers; $i++) {
        docker compose up -d
    }
    Infos
    
}
function Drop 
{
    Write-Host "Drop all of the containers:"
    docker rm -f $(docker ps -a | Select-String -Pattern "sneakers" | ForEach-Object {docker ps -aq})
    Write-Host "End of drop"
}

function Start
{
    Write-Host "Reboot containers"
    docker run $(docker ps -a | Select-String -Pattern "sneakers" | ForEach-Object {docker ps -aq})
}

function Infos
{
    Write-Host "Informations of containers:"
    foreach ($containers in $(docker ps -a | Select-String -Pattern "sneakers" | ForEach-Object {docker ps -aq})) {
        docker inspect -f ' => {{.Name}} - {{.State.Status}}' $containers
    }
}

<#######################################################################################
#
#   Main
#
#######################################################################################>
$Value = $args[0]
switch ($Value) {
    "--create" 
    {
        Create
    }

    "--drop"
    {
        Drop
    }

    "--start"
    {
        Start
    }

    "--infos"
    {
        Infos
    }
    "--help"
    {
        Help
    }
    Default 
    {
        Write-Host "Error : your choice is not valid."
    }
}