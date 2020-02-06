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

variable "region" {
    default = "us-west-2"
}

variable "availability_zone" {
    default = "us-west-2a"
}

variable "db_ami" {
    default = "ami-06d51e91cea0dac8d" # Ubuntu 18.04 LTS official ami
}
variable "db_instance" {
    default = "m5.4xlarge" # postgres.conf optimized 
}
variable "uma_processed_ip" {
    default = "10.10.3.10"
}

variable "dataprocessor_count" {
    # 20 % dataprocessor_count = 0
    default = "29"
    #default = "2"
}
variable "dataprocessor_ami" {
    default = "ami-06d51e91cea0dac8d" # Ubuntu 18.04 LTS official ami
}
variable "dataprocessor_instance" {
    default = "t2.micro"
}

