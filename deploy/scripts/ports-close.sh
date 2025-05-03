declare -A ports

ports["backend-nodeport"]="31002"
ports["frontend-load-balancer"]="30200"
ports["kube-state-metrics"]="31001"
ports["node-exporter"]="31000"
ports["pgvector"]="31004"

minikube_ip=$(minikube ip)
echo $minikube_ip
for key in "${!ports[@]}"; do
    port="${ports[$key]}"
    echo "Removing port forwading on $port for $key..."
    sudo iptables -t nat -D PREROUTING -p tcp --dport "$port" -j DNAT --to-destination "${minikube_ip}:$port"
    sudo iptables -D FORWARD -p tcp -d "$minikube_ip" --dport "$port" -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT
done
