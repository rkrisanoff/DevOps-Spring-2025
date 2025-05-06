#!/usr/bin/env bash
# Минималистичный пайплайн для Terraform и Ansible
set -euo pipefail
IFS=$'\n\t'

DRY_RUN=false
STEP="all"

usage() {
  cat <<EOF
Использование: $(basename "$0") [-n] [-t шаг] [-h]

  -n          dry-run (команды только печатаются)
  -t шаг      terraform | ansible | all (по умолчанию all)
  -h          показать эту помощь
EOF
}

while getopts "hnt:" opt; do
  case "$opt" in
    h) usage; exit 0 ;;
    n) DRY_RUN=true ;;
    t) STEP=$OPTARG ;;
    *) usage; exit 1 ;;
  esac
done
shift $((OPTIND -1))

run() {
  if $DRY_RUN; then
    echo "[DRY] $*"
  else
    "$@"
  fi
}

# Шаги
if [[ $STEP =~ ^(terraform|all)$ ]]; then
  echo ">>> Terraform"

  export YC_TOKEN=$(yc iam create-token)
  export YC_CLOUD_ID=$(yc config get cloud-id)
  export YC_FOLDER_ID=$(yc config get folder-id)

  run terraform init -input=false
  run terraform plan -out=tfplan
  run terraform apply -auto-approve tfplan

fi



if [[ $STEP =~ ^(ansible|all)$ ]]; then
  echo ">>> Ansible"
  run ansible-galaxy collection install community.kubernetes

  export EXTERNAL_IP=$(terraform output -raw external_ip_address)
  echo 'external ip: ' $EXTERNAL_IP

  export ANSIBLE_HOST_KEY_CHECKING=False
  export ANSIBLE_SSH_PRIVATE_KEY="/home/trisolaris/.ssh/id_rsa"
  export ANSIBLE_USER="ubuntu"

  run ansible-playbook --inventory "${EXTERNAL_IP}," \
                       --user "${ANSIBLE_USER}" \
                       --extra-vars "ansible_ssh_private_key_file=${ANSIBLE_SSH_PRIVATE_KEY}" \
                       playbooks/deploy-services.yml -v

  run ansible-playbook --inventory "${EXTERNAL_IP}," \
                       --user "${ANSIBLE_USER}" \
                       --extra-vars "ansible_ssh_private_key_file=${ANSIBLE_SSH_PRIVATE_KEY}" \
                       playbooks/deploy-metrics.yml -v

  run ansible-playbook --inventory "${EXTERNAL_IP}," \
                       --user "${ANSIBLE_USER}" \
                       --extra-vars "ansible_ssh_private_key_file=${ANSIBLE_SSH_PRIVATE_KEY}" \
                       playbooks/open-ports.yml -v


fi

echo "Finished"
