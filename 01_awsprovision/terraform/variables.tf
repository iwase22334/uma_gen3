provider "aws" {
    version = "~> 2.0"
    region  = "us-west-2"
}

variable "key_name" {
    description = "Desired name of AWS key pair"
}

variable "public_key_path" {
    description = <<DESCRIPTION
    Path to the SSH public key to be used for authentication.
    Ensure this keypair is added to your local SSH agent so provisioners can
    connect.

    Example: ~/.ssh/terraform.pub
    DESCRIPTION
}

variable "app_name" {
    default = "uma_trainer_gen03"
}

variable "region" {
    default = "us-west-2"
}

variable "availability_zone" {
    default = "us-west-2a"
}

variable "root_segment" {
    default = "10.10.0.0/16"
}

variable "segment_gen02" {
    default = "10.10.3.0/24"
}

