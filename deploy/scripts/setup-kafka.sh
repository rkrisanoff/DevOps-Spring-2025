# check if Java is already installed
if [ ! -d "/home/ubuntu/jdk-21" ]; then
    cd /home/ubuntu
    curl -o openjdk-21-bin.tar.gz https://download.java.net/openjdk/jdk21/ri/openjdk-21+35_linux-x64_bin.tar.gz
    tar xf openjdk-21-bin.tar.gz
fi
export JAVA_HOME=/home/ubuntu/jdk-21
export PATH=$PATH:$JAVA_HOME/bin

# Install Kafka
curl -o kafka_2.13-4.0.0.tgz https://dlcdn.apache.org/kafka/4.0.0/kafka_2.13-4.0.0.tgz
tar -xzf kafka_2.13-4.0.0.tgz

cd kafka_2.13-4.0.0

KAFKA_CONFIG_PATH=/home/ubuntu/kafka_server.properties
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone -t $KAFKA_CLUSTER_ID -c $KAFKA_CONFIG_PATH
bin/kafka-server-start.sh -daemon $KAFKA_CONFIG_PATH

echo "Going to sleep for 30 seconds to wait until Kafka Server is fully up"
sleep 30s
echo "Continue setting up Kafka"

bin/kafka-topics.sh --create --topic notifications --bootstrap-server localhost:9092

# Install kafkacat for testing
sudo apt install -y kafkacat
