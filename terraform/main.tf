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
  service_account_key_file = "key.json"
}

resource "yandex_vpc_network" "network-1" {
  name = "network1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  name           = "subnet1"
  zone           = "ru-central1-a"
  v4_cidr_blocks = ["192.168.10.0/24"]
  network_id     = "${yandex_vpc_network.network-1.id}"
}
resource "yandex_iam_service_account" "sa" {
  name        = "vmmanager"
  description = "service account to manage VMs"
}

resource "yandex_compute_disk" "boot-disk-1" {
  name     = "boot-disk-1"
  type     = "network-hdd"
  zone     = "ru-central1-a"
  size     = "20"
  image_id = "fd84r9t01ao2ktahik80"
}

resource "yandex_compute_instance" "devopsvm" {
  name                = "devopsvm"
  resources {
    cores  = 4
    memory = 8
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot-disk-1.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
  }

  metadata = {
    user-data = "${file("cloud-init.txt")}"
  }
}
output "internal_ip_address_vm_1" {
  value = yandex_compute_instance.devopsvm.network_interface.0.ip_address
}
output "external_ip_address_vm_1" {
  value = yandex_compute_instance.devopsvm.network_interface.0.nat_ip_address
}
