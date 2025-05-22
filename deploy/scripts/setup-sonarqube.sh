sudo apt update
sudo apt install -y unzip jq

# Postgresql installation from APT Repo
# Import the repository signing key:
sudo apt install curl ca-certificates
sudo install -d /usr/share/postgresql-common/pgdg
sudo curl -o /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc --fail https://www.postgresql.org/media/keys/ACCC4CF8.asc

# Create the repository configuration file:
. /etc/os-release
sudo sh -c "echo 'deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $VERSION_CODENAME-pgdg main' > /etc/apt/sources.list.d/pgdg.list"

sudo apt update
sudo apt -y install postgresql

# Postgres config
CHECK_SERVER_ENCODING=$(sudo -u postgres psql -tAc "SHOW SERVER_ENCODING;")

if [[ "$CHECK_SERVER_ENCODING" != "UTF8" ]]; then
    echo "Server Encoding is not UTF8 ($CHECK_SERVER_ENCODING), changing..."

    sudo sed -i '/^#*server_encoding/c\server_encoding = utf8' "/etc/postgresql/*/main/postgresql.conf"
    sudo systemctl restart postgresql.service
else
    echo "Server Encoding UTF8 is installed."
fi


# Sonar uses DB "sonarqube", public schema. All priviliges for all objects go to sonarqube user
# sed to add login/pass to sonar.properties -- sonarqube/sonarqube default, works without it
POSTGRES_USERNAME="sonarqube"
POSTGRES_PASSWORD="sonarqube"

sudo -u postgres psql -c "CREATE DATABASE sonarqube"

PSQL_COMMAND="sudo -u postgres psql -v ON_ERROR_STOP=1"
$PSQL_COMMAND -c "CREATE USER ${POSTGRES_USERNAME} WITH PASSWORD '${POSTGRES_PASSWORD}';"

$PSQL_COMMAND -d sonarqube -c "
    GRANT USAGE ON SCHEMA public TO ${POSTGRES_USERNAME};
    GRANT CREATE ON SCHEMA public TO ${POSTGRES_USERNAME};

    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${POSTGRES_USERNAME};
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ${POSTGRES_USERNAME};

    ALTER DEFAULT PRIVILEGES FOR ROLE ${POSTGRES_USERNAME} IN SCHEMA public GRANT ALL ON TABLES TO ${POSTGRES_USERNAME};
    ALTER DEFAULT PRIVILEGES FOR ROLE ${POSTGRES_USERNAME} IN SCHEMA public GRANT ALL ON SEQUENCES TO ${POSTGRES_USERNAME};
"

sudo sed -i '/^# TYPE  DATABASE        USER            ADDRESS                 METHOD$/a local all sonarqube md5' /etc/postgresql/17/main/pg_hba.conf
sudo systemctl restart postgresql.service

# JAVA installation
curl -o openjdk-21-bin.tar.gz https://download.java.net/openjdk/jdk21/ri/openjdk-21+35_linux-x64_bin.tar.gz
tar xf openjdk-21-bin.tar.gz

export JAVA_HOME=/home/ubuntu/jdk-21
export PATH=$PATH:$JAVA_HOME/bin

# Sonarqube
# use env variables instead of modifying config
export SONAR_JDBC_USERNAME=$POSTGRES_USERNAME
export SONAR_JDBC_PASSWORD=$POSTGRES_PASSWORD
export SONAR_JDBC_URL="jdbc:postgresql://localhost/sonarqube"

curl -o sonarqube.zip https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-25.5.0.107428.zip
unzip sonarqube.zip

bash sonarqube-25.5.0.107428/bin/linux-x86-64/sonar.sh start


SONAR_HOST_PORT="localhost:9000"
SONAR_USER="admin"
SONAR_PASSWORD="AdminAdmin1@"

echo "Going to sleep for 3 minutes to wait until Sonarqube Server is fully up"
sleep 3m
echo "Continue setting up Sonarqube"

curl --max-time 10 "http://$SONAR_HOST_PORT/"

echo "Going to sleep for 3 minutes to wait until Sonarqube Web-server is fully up"
sleep 3m
echo "Continue setting up Sonarqube"

PROJECT_NAME="BookApp"

curl -X POST -u $SONAR_USER:admin "http://$SONAR_HOST_PORT/api/users/change_password" \
    --data-urlencode "login=$SONAR_USER" \
    --data-urlencode "previousPassword=admin" \
    --data-urlencode "password=$SONAR_PASSWORD"

PROJECT_JSON=$(
    curl -X POST -u $SONAR_USER:$SONAR_PASSWORD "http://$SONAR_HOST_PORT/api/projects/create" \
        --data-urlencode "name=$PROJECT_NAME" \
        --data-urlencode "project=$PROJECT_NAME"
)

SET_BRANCH_JSON=$(
    curl -X POST -u $SONAR_USER:$SONAR_PASSWORD "http://$SONAR_HOST_PORT/api/project_branches/rename" \
        --data-urlencode "project=$PROJECT_NAME" \
        --data-urlencode "name=lab4"
)

SONAR_PROJECT_TOKEN_JSON=$(
    curl -X POST -u $SONAR_USER:$SONAR_PASSWORD "http://$SONAR_HOST_PORT/api/user_tokens/generate" \
        --data-urlencode "login=$SONAR_USER" \
        --data-urlencode "name=Github"
)

SONAR_PROJECT_TOKEN=$(echo "$SONAR_PROJECT_TOKEN_JSON" | jq -r '.token')
echo "Token: $SONAR_PROJECT_TOKEN"
echo "$SONAR_PROJECT_TOKEN" >> /home/ubuntu/sonar_token.txt

# Setup custom Quality Gate
QUALITY_GATE="devops-qg"
curl -X POST -u $SONAR_USER:$SONAR_PASSWORD "http://$SONAR_HOST_PORT/api/qualitygates/copy" \
     --data-urlencode "name=$QUALITY_GATE" \
     --data-urlencode "sourceName=Sonar way"

curl -X POST -u $SONAR_USER:$SONAR_PASSWORD "http://$SONAR_HOST_PORT/api/qualitygates/create_condition" \
     --data-urlencode "gateName=$QUALITY_GATE" \
     --data-urlencode "metric=coverage" \
     --data-urlencode "op=LT" \
     --data-urlencode "error=80"

curl -X POST -u $SONAR_USER:$SONAR_PASSWORD "http://$SONAR_HOST_PORT/api/qualitygates/select" \
     --data-urlencode "gateName=$QUALITY_GATE" \
     --data-urlencode "projectKey=$PROJECT_NAME"
