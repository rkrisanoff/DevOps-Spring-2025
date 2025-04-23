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
    cores  = 2
    memory = 2
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

resource "yandex_vpc_network" "network" {
  name = "network"
}

resource "yandex_vpc_subnet" "subnet" {
  name           = "subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.network.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}


resource "null_resource" "deploy" {
  provisioner "remote-exec" {

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/yandex-cloud")
      host        = yandex_compute_instance.book-app-vm.network_interface[0].nat_ip_address
    }

    scripts = [
      "install-docker.sh",
      "deploy.sh"
    ]
  }
}


output "internal_ip_address" {
  value = yandex_compute_instance.book-app-vm.network_interface.0.ip_address
}

output "external_ip_address" {
  value = yandex_compute_instance.book-app-vm.network_interface.0.nat_ip_address
}
