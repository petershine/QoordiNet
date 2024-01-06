#!/bin/bash
dockerContainerName="QoordiNet"
dockerImageName="qoordinet"

dockerVolumePath="~/fXDocker/_volume"
dockerMountedRoot="/_python/_mounted"

dockerPortNumber=50002


TEMP_COLOR='\033[0;37m'
NC='\033[0m' # No Color. Necessary for resetting


echo
echo "[REDEPLOY] container: \"$dockerContainerName\" from image: \"$dockerImageName\""

echo
echo "[STOP] currently running: $dockerContainerName"
echo -e "${TEMP_COLOR}$(docker stop $dockerContainerName)${NC}"

echo
echo "[REMOVE] container: $dockerContainerName"
echo -e "${TEMP_COLOR}$(docker container rm $dockerContainerName)${NC}"

echo
echo "[REMOVE] image : $dockerImageName"
echo -e "${TEMP_COLOR}$(docker image rm $dockerImageName)${NC}"

echo
echo "[COPY] "../_shared" to "./mainApp/_temp_shared" for Docker image"
echo -e "${TEMP_COLOR}$(cp -rv ../_shared ./mainApp/_temp_shared)${NC}"
echo -e "${TEMP_COLOR}$(ls -al ./mainApp/_temp_shared)${NC}"

echo
echo "[(Re)BUILD] image : $dockerImageName"
docker build -t $dockerImageName .

echo
echo "[REMOVE] "./mainApp/_temp_shared" that was copied into Docker image"
echo -e "${TEMP_COLOR}$(rm -rvf ./mainApp/_temp_shared)${NC}"

echo
echo "[(Re)CREATE] container: \"$dockerContainerName\" from image: \"$dockerImageName\""
docker create --name $dockerContainerName -v ~/fXDocker/_volume:$dockerMountedRoot -p $dockerPortNumber:$dockerPortNumber $dockerImageName


echo
echo "[(Re)START] container: \"$dockerContainerName\" from image: \"$dockerImageName\""
docker restart $dockerContainerName


echo
echo "[FINISHED] deploy \"$dockerContainerName\" from image \"$dockerImageName\""
echo -e "${TEMP_COLOR}$(docker image ls -a)${NC}"
echo
echo -e "${TEMP_COLOR}$(docker container ls -a)${NC}"

echo
echo "[REVIEW] crontab"
echo -e "${TEMP_COLOR}$(crontab -l)${NC}"
