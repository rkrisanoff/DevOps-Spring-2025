sudo apt install -y snapd
sudo snap install k8s --classic
sudo snap install kubectl --classic
sudo swapoff -a

sudo k8s bootstrap

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# сюда будет монтирован том для pg-vector
mkdir /home/ubuntu/pg-data
