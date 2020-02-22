#####################################
## security group
#####################################
data "aws_subnet" "selected" {
    filter {
        name   = "tag:Name"
        values = ["${var.app_name}-private-subnet1"]
    }
}

data "aws_security_group" "selected" {
    filter {
        name   = "group-name"
        values = ["allow_psql"]
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
  vpc_security_group_ids = ["${data.aws_security_group.selected.id}"]
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

