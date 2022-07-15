# This file was autogenerated by the 'packer hcl2_upgrade' command. We
# recommend double checking that everything is correct before going forward. We
# also recommend treating this file as disposable. The HCL2 blocks in this
# file can be moved to other files. For example, the variable blocks could be
# moved to their own 'variables.pkr.hcl' file, etc. Those files need to be
# suffixed with '.pkr.hcl' to be visible to Packer. To use multiple files at
# once they also need to be in the same folder. 'packer inspect folder/'
# will describe to you what is in that folder.

# Avoid mixing go templating calls ( for example ```{{ upper(`string`) }}``` )
# and HCL2 calls (for example '${ var.string_value_example }' ). They won't be
# executed together and the outcome will be unknown.

# All generated input variables will be of 'string' type as this is how Packer JSON
# views them; you can change their type later on. Read the variables type
# constraints documentation
# https://www.packer.io/docs/templates/hcl_templates/variables#type-constraints for more info.

variable "box_basename" {
  type    = string
  default = "ubuntu-20.04"
}

variable "cpus" {
  type    = string
  default = "2"
}

variable "disk_size" {
  type    = string
  default = "20468"
}

variable "esxi_datastore" {
  type    = string
  default = ""
}

variable "esxi_host" {
  type    = string
  default = ""
}

variable "esxi_password" {
  type    = string
  default = ""
}

variable "esxi_username" {
  type    = string
  default = ""
}

variable "esxi_network_with_dhcp_and_internet" {
  type    = string
  default = ""
}

variable "guest_additions_url" {
  type    = string
  default = ""
}

variable "headless" {
  type    = string
  default = "false"
}

variable "iso_checksum" {
  type    = string
  default = "sha256:28ccdb56450e643bad03bb7bcf7507ce3d8d90e8bf09e38f6bd9ac298a98eaad"
}

variable "memory" {
  type    = string
  default = "4096"
}

variable "name" {
  type    = string
  default = "ubuntu-20.04"
}

variable "template" {
  type    = string
  default = "ubuntu-20.04-amd64"
}

variable "version" {
  type    = string
  default = "TIMESTAMP"
}

locals {
  build_timestamp = "${legacy_isotime("20060102150405")}"
  http_directory  = "${path.root}/http"
}

# source blocks are generated from your builders; a source can be referenced in
# build blocks. A build block runs provisioner and post-processors on a
# source. Read the documentation for source blocks here:
# https://www.packer.io/docs/templates/hcl_templates/blocks/source
source "vmware-iso" "autogenerated_1" {
  boot_command            = ["<esc><wait><esc><wait><f6><wait><esc><wait>","<bs><bs><bs><bs><bs>", "autoinstall ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/ ","--- <enter>"]  
  boot_wait               = "9s"
  cpus                    = "${var.cpus}"
  disk_size               = "${var.disk_size}"
  disk_type_id            = "thin"
  guest_os_type           = "ubuntu-64"
  http_directory          = "${local.http_directory}"
  insecure_connection     = true
  iso_checksum            = "${var.iso_checksum}"
  iso_url                 = "https://releases.ubuntu.com/20.04/ubuntu-20.04.4-live-server-amd64.iso"
  keep_registered         = true
  memory                  = "${var.memory}"
  pause_before_connecting = "1m"
  remote_datastore        = "${var.esxi_datastore}"
  remote_host             = "${var.esxi_host}"
  remote_password         = "${var.esxi_password}"
  remote_type             = "esx5"
  remote_username         = "${var.esxi_username}"
  shutdown_command        = "echo 'vagrant' | sudo -S shutdown -P now"
  skip_export             = true
  ssh_username            = vault("/packer/unix","username")
  ssh_password            = vault("/packer/unix","password")
  ssh_port                = 22
  ssh_timeout             = "1h1m1s"
  temporary_key_pair_type = "ed25519"
  vm_name                 = "Ubuntu2004"
  vmx_data = {
    "cpuid.coresPerSocket"           = "2"
    "ethernet0.networkName"          = "${var.esxi_network_with_dhcp_and_internet}"
  }
  vnc_disable_password = false
  vnc_over_websocket   = true
  vnc_port_max         = 5980
  vnc_port_min         = 5900
}

# a build block invokes sources and runs provisioning steps on them. The
# documentation for build blocks can be found here:
# https://www.packer.io/docs/templates/hcl_templates/blocks/build
build {
  sources = ["source.vmware-iso.autogenerated_1"]
}
