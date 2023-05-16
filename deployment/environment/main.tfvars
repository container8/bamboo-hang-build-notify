server = {
  name = "bamboo-hanging-build-notifier"
  image = "ubuntu-22.04"
  type = "cx21"
  ipv4_enabled = true
  ipv6_enabled = false
}

ssh_key = {
  name = "bamboo-hanging-build-notifier"
  location = "~/.ssh/id_rsa.pub"
}
