#!/bin/bash

#project code repo
REPO_BASE=https://github.com/solariswu/
export APERSONAIDP_REPO_NAME=customsso
export APERSONAADM_REPO_NAME=cognito-userpool-myraadmin

#install NODE NPM GIT
NVM_VER=v0.39.7
NPM_VER=10.8.2

rm -rf .nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/$NVM_VER/install.sh | bash
source ~/.bashrc
nvm install --lts

#install git
sudo yum update -y
sudo yum install git -y

#update npm
npm install -g npm@$NPM_VER
npm install -g aws-cdk 

#download code repo
echo "clone the repo $REPO_BASE$APERSONAIDP_REPO_NAME"
git clone $REPO_BASE$APERSONAIDP_REPO_NAME
echo "clone the repo $REPO_BASE$APERSONAADM_REPO_NAME"
git clone $REPO_BASE$APERSONAADM_REPO_NAME
cd $APERSONAIDP_REPO_NAME
git pull 
cp ./config.sh ../
cp ./install.sh ../
cd ..
cd $APERSONAADM_REPO_NAME
git pull
