#!/bin/bash

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
