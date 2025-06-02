terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  zone = "ru-central1-a"
}


variable "BOT_TOKEN" {
  type = string
}


resource "yandex_compute_disk" "boot-disk" {
  name     = "book-app-drive"
  type     = "network-ssd"
  zone     = "ru-central1-a"
  size     = "30"
  image_id = "fd85m9q2qspfnsv055rh"
}

resource "yandex_compute_instance" "book-app-vm" {
  name                      = "book-app-vm"
  allow_stopping_for_update = true
  platform_id               = "standard-v3"
  zone                      = "ru-central1-a"

  resources {
    cores  = 8
    memory = 8
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot-disk.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    # ssh-keys = "ubuntu:${file("~/.ssh/yandex-cloud.pub")}"
    user-data = "${file("cloud-init.txt")}"
  }

}


resource "yandex_compute_disk" "monitoring-boot-disk" {
  name     = "monitoring-drive"
  type     = "network-ssd"
  zone     = "ru-central1-a"
  size     = "20"
  image_id = "fd85m9q2qspfnsv055rh"
}


resource "yandex_compute_instance" "monitoring-vm" {
  name                      = "monitoring-vm"
  allow_stopping_for_update = true
  platform_id               = "standard-v3"
  zone                      = "ru-central1-a"

  resources {
    cores  = 8
    memory = 8
  }

  boot_disk {
    disk_id = yandex_compute_disk.monitoring-boot-disk.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    # ssh-keys = "ubuntu:${file("~/.ssh/yandex-cloud.pub")}"
    user-data = "${file("cloud-init.txt")}"
  }

}

resource "yandex_vpc_network" "network" {
  name = "network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}


resource "null_resource" "prepare_vm" {
  provisioner "remote-exec" {

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("/home/anastasia/.ssh/yandex-cloud")
      host        = yandex_compute_instance.book-app-vm.network_interface[0].nat_ip_address
    }

    script = "scripts/install-kubernetes.sh"
  }
}


locals {
  # build Prometheus properties
  prometheus_custom_config = templatefile(
    "templates/prometheus_template.yml",
    {
      external_ip_address = yandex_compute_instance.book-app-vm.network_interface.0.nat_ip_address
    }
  )

  # build Kubernetes Manifest for TG Bot
  tg_bot_manifest = templatefile(
    "templates/notification_bot_secret_template.yml",
    {
      bot_token = var.BOT_TOKEN,
      monitoring_ip_address = yandex_compute_instance.monitoring-vm.network_interface.0.nat_ip_address
    }
  )

  # build Kafka properties to use with custom IP
  kafka_server_properties = templatefile(
    "templates/kafka_server_template.properties",
    {
      monitoring_ip_address = yandex_compute_instance.monitoring-vm.network_interface.0.nat_ip_address
    }
  )
}

resource "local_file" "copy_file_prometheus" {
  content = local.prometheus_custom_config
  filename = "prometheus_vm/prometheus.yml"
}

resource "local_file" "copy_file_notification_bot_secret" {
  content = local.tg_bot_manifest
  filename = "manifests/notification-bot-secret.yaml"
}

resource "local_file" "copy_file_kafka" {
  content = local.kafka_server_properties
  filename = "kafka/kafka_server.properties"
}

resource "null_resource" "setup_monitoring" {
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("/home/anastasia/.ssh/yandex-cloud")
    host        = yandex_compute_instance.monitoring-vm.network_interface[0].nat_ip_address
  }

  # Copy Prometheus files to remote
  provisioner "remote-exec" {
    inline = ["mkdir /home/ubuntu/prometheus"]
  }

  provisioner "file" {
    source      = "prometheus_vm/"
    destination = "/home/ubuntu/prometheus/"
  }

  # Copy Grafana files to remote
  provisioner "remote-exec" {
    inline = ["mkdir /home/ubuntu/grafana_provisioning"]
  }
  provisioner "file" {
    source      = "grafana_provisioning_vm/"
    destination = "/home/ubuntu/grafana_provisioning/"
  }

  # Copy Kafka Config to remote
  provisioner "file" {
    source      = "kafka/kafka_server.properties"
    destination = "/home/ubuntu/kafka_server.properties"
  }

  # Run setup scripts
  provisioner "remote-exec" {
    scripts = [
      "scripts/setup-prometheus.sh",
      "scripts/setup-grafana.sh",
      "scripts/setup-sonarqube.sh",
      "scripts/setup-kafka.sh"
    ]
  }

}


output "internal_ip_address" {
  value = yandex_compute_instance.book-app-vm.network_interface.0.ip_address
}

output "external_ip_address" {
  value = yandex_compute_instance.book-app-vm.network_interface.0.nat_ip_address
}

output "internal_ip_address_monitoring" {
  value = yandex_compute_instance.monitoring-vm.network_interface.0.ip_address
}

output "external_ip_address_monitoring" {
  value = yandex_compute_instance.monitoring-vm.network_interface.0.nat_ip_address
}
