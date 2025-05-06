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


resource "yandex_compute_disk" "boot-disk" {
  name     = "book-app-drive"
  type     = "network-ssd"
  zone     = "ru-central1-a"
  size     = "10"
  image_id = "fd85m9q2qspfnsv055rh"
}

resource "yandex_compute_instance" "book-app-vm" {
  name                      = "book-app-vm"
  allow_stopping_for_update = true
  platform_id               = "standard-v3"
  zone                      = "ru-central1-a"

  resources {
    cores  = 4
    memory = 4
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
  size     = "10"
  image_id = "fd85m9q2qspfnsv055rh"
}


resource "yandex_compute_instance" "monitoring-vm" {
  name                      = "monitoring-vm"
  allow_stopping_for_update = true
  platform_id               = "standard-v3"
  zone                      = "ru-central1-a"

  resources {
    cores  = 2
    memory = 2
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
      private_key = file("~/.ssh/yandex-cloud")
      host        = yandex_compute_instance.book-app-vm.network_interface[0].nat_ip_address
    }

    script = "scripts/install-kubernetes.sh"
  }
}


locals {
  prometheus_custom_config = templatefile(
    "templates/prometheus_template.yml",
    {
      external_ip_address = yandex_compute_instance.book-app-vm.network_interface.0.nat_ip_address
    }
  )
}

resource "local_file" "copy_file" {
  content = local.prometheus_custom_config
  filename = "prometheus_vm/prometheus.yml"
}


resource "null_resource" "setup_monitoring" {
  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/yandex-cloud")
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

  # Run setup scripts
  provisioner "remote-exec" {
    scripts = [
      "scripts/setup-prometheus.sh",
      "scripts/setup-grafana.sh"
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
