#!/bin/bash

#project code repo
REPO_BASE=https://github.com/solariswu/
export APERSONAIDP_REPO_NAME=customsso
export APERSONAADM_REPO_NAME=cognito-userpool-myraadmin

#install NODE NPM GIT
NVM_VER=v0.39.7
NPM_VER=11.0.0

rm -rf .nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VER/install.sh | bash
source ~/.bashrc
echo "install nvm "$NVM_VER
nvm install --lts >/dev/null
 
 #install git
echo "install git"
sudo yum update -y >/dev/null
sudo yum install git -y >/dev/null
 
 #update npm
echo "install npm v"$NPM_VER
npm install -g npm@$NPM_VER >/dev/null
npm install -g aws-cdk >/dev/null

#download code repo
echo "clone the repo $REPO_BASE$APERSONAIDP_REPO_NAME"
git clone $REPO_BASE$APERSONAIDP_REPO_NAME
echo "clone the repo $REPO_BASE$APERSONAADM_REPO_NAME"
git clone $REPO_BASE$APERSONAADM_REPO_NAME
cd $APERSONAIDP_REPO_NAME
git pull 
cp ./config.sh ../
cp ./install.sh ../
cp ./uninstall.sh ../
cp ./aPersona_ASM-and-aPersona_Identity_Mgr_Ts_Cs.11-27-2024.txt ../
cd ..
cd $APERSONAADM_REPO_NAME
git pull
