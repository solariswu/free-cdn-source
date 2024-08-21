#!/bin/bash

#project code repo
export APERSONAIDP_REPO=https://github.com/solariswu/customsso
export APERSONAADM_REPO=https://github.com/solariswu/cognito-userpool-myraadmin

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

#download code repo
echo "clone the repo $APERSONAIDP_REPO"
git clone $APERSONAIDP_REPO
echo "clone the repo $APERSONADM_REPO"
git clone $APERSONAADM_REPO
cd $APERSONAIDP_REPO
git pull 
cd ..
cd $APERSONAADM_REPO
git pull
