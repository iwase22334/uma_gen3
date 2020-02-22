#####################################
## security group
#####################################
data "aws_subnet" "selected" {
    filter {
        name   = "tag:Name"
        values = ["${var.app_name}-private-subnet1"]
    }
}

data "aws_security_group" "selected_sg" {
    filter {
        name   = "tag:Name"
        values = ["all_ssh"]
    }
}

#####################################
## instance 
#####################################
resource "aws_instance" "trainer_gen3" {
  ami           = "${var.trainer_ami}"
  instance_type = "${var.trainer_instance}"

  key_name                  = "${var.key_name}"
  availability_zone         = "${var.availability_zone}"
  vpc_security_group_ids = ["${data.aws_security_group.selected_sg.id}"]
  subnet_id         = "${data.aws_subnet.selected.id}"

  associate_public_ip_address = "true"

  tags = {
    Name     = "trainer_gen3"
    Role     = "trainer"
  }
}

