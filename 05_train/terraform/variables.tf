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
    default = "uma_trainer_gen02"
}

variable "availability_zone" {
    default = "us-west-2a"
}

variable "trainer_ami" {
    default ="ami-010a96c958f9ee5cf" 
}
variable "trainer_instance" {
    default = "m5.2xlarge"
}

