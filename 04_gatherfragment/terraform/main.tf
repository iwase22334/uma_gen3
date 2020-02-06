#####################################
## security group
#####################################
data "aws_subnet" "selected" {
    filter {
        name   = "tag:Name"
        values = ["${var.app_name}-private-subnet1"]
    }
}

resource "aws_security_group" "allow_psql" {
    vpc_id      = "${data.aws_subnet.selected.vpc_id}"
    name        = "allow_psql"
    description = "Used in the terraform"

    # SSH access from anywhere
    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    # psql access from anywhere
    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        cidr_blocks = ["${data.aws_subnet.selected.cidr_block}"]
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

#####################################
## instance 
#####################################

resource "aws_instance" "fragmentgatherer" {
  ami           = "${var.fragmentgatherer_ami}"
  instance_type = "${var.fragmentgatherer_instance}"

  key_name          = "${var.key_name}"
  availability_zone      = "${var.availability_zone}"
  vpc_security_group_ids = ["${aws_security_group.allow_psql.id}"]
  subnet_id         = "${data.aws_subnet.selected.id}"
  private_ip        = "10.10.3.40"

  root_block_device {
    volume_size = 30
  }

  associate_public_ip_address = "true"

  tags = {
    Name     = "fragment_gatherer"
    Role     = "fragment_gatherer"
    TrainCount = "${format("%d", var.fragmentgatherer_train_count)}"
    EvalCount   = "${format("%d", var.fragmentgatherer_eval_count)}"
  }
}

