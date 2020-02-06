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

variable "fragmentgatherer_train_count" {
    default = "76"
}

variable "fragmentgatherer_eval_count" {
    default = "16"
}

variable "fragmentgatherer_ami" {
    default = "ami-06d51e91cea0dac8d" 
}

variable "fragmentgatherer_instance" {
    description = <<DESCRIPTION
        Constraints
         * np.save requests more than 32GB?16GB? of memory
    DESCRIPTION

    default =  "r5ad.xlarge"
}

