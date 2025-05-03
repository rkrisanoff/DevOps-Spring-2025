# bash -i setup.sh из директории tests/
apt-get update && apt-get install unzip

curl -o- https://fnm.vercel.app/install | bash
source /root/.bashrc

# из нового терминала
fnm install 22
node -v && npm -v

npm install
