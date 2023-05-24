server = {
  name = "bamboo-hanging-build-notifier"
  image = "ubuntu-22.04"
  # 6.37 euros per month
  type = "cx21"
  ipv4_enabled = true
  ipv6_enabled = false
}

# The ssh_key with name main have to be created beforehand in the hetzner account
ssh_key = {
  name = "main"
}
