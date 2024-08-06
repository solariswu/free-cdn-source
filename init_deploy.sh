#!/bin/bash

#project code repo
PRJ_REPO_BASE=https://github.com/solariswu/
PRJ_REPO_NAME=customsso

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
git clone $PRJ_REPO_BASE$PRJ_REPO_BASE
cd $PRJ_REPO_NAME
git pull

./deployment.sh | bash
