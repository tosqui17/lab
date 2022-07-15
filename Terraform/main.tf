provider "esxi" {
  esxi_hostname = var.esxi_hostname
  esxi_hostport = var.esxi_hostport
  esxi_username = var.esxi_username
  esxi_password = var.esxi_password
}

resource "esxi_guest" "Ubuntu2004" {
  guest_name = "Ubuntu2004"
  boot_disk_type = "thin"
  disk_store = var.esxi_datastore
  power      = "off"
  network_interfaces {
    virtual_network = var.vm_network
   }
  }

