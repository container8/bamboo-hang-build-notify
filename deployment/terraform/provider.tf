# Configure the Hetzner Cloud Provider
terraform {
  backend "s3" {
    # mapped to the env vars through the Makefile
    # bucket = ${BUCKET_NAME}
    # key = ${BUCKET_KEY}
    # region = ${AWS_DEFAULT_REGION}
  }

  required_providers {
    hcloud = {
      source = "hetznercloud/hcloud"
      version = "1.39.0"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}
