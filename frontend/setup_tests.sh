# bash -i setup.sh из директории tests/
apt-get update && apt-get install unzip

curl -o- https://fnm.vercel.app/install | bash

# Add fnm to the current shell session  / or use new terminal
export PATH="/root/.local/share/fnm:$PATH"
eval "`fnm env`"

# из нового терминала
fnm install 22
node -v && npm -v

npm install

# command to run tests:
# npm test -- --coverage
