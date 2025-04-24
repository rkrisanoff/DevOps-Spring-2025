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

  export YC_FOLDER_ID=b1gqtutqct831hr4afpn # LITERALLY ME
  export YC_TOKEN=$(yc iam create-token)

  run terraform init -input=false
  run terraform plan -out=tfplan
  run terraform apply -auto-approve tfplan

fi



if [[ $STEP =~ ^(ansible|all)$ ]]; then
  echo ">>> Ansible"
  run ansible-galaxy collection install community.kubernetes


  export EXTERNAL_IP=$(terraform output -raw external_ip_address_vm_1)
  export INTERNAL_IP=$(terraform output -raw internal_ip_address_vm_1)
  echo 'external ip: ' $EXTERNAL_IP
  echo 'internal ip: ' $INTERNAL_IP

  # run ansible-playbook -i inventories/production.ini site.yml
  export ANSIBLE_HOST_KEY_CHECKING=False
  run ansible-playbook --inventory "${EXTERNAL_IP}," \
                       --user ubuntu \
                       --extra-vars "ansible_ssh_private_key_file=/home/trisolaris/.ssh/id_ed25519" \
                       --extra-vars "internal_ip={INTERNAL_IP}" \
                       playbooks/deploy-infra.yml -vv
fi

echo "Finished"
