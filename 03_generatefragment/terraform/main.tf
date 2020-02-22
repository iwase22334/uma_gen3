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
resource "aws_instance" "fragmentgenerator_train" {
  count         = "${format("%d", var.fragmentgenerator_train_count)}"
  ami           = "${var.fragmentgenerator_ami}"
  instance_type = "${var.fragmentgenerator_instance}"

  credit_specification {
    cpu_credits = "unlimited"
  }

  availability_zone      = "${var.availability_zone}"
  vpc_security_group_ids = ["${data.aws_security_group.selected.id}"]
  subnet_id         = "${data.aws_subnet.selected.id}"
  private_ip        = "${format("10.10.3.1%02d", count.index + 1)}"
  key_name          = "${var.key_name}"

  associate_public_ip_address = "true"

  tags = {
    Name     = "${format("fragment_generator_train_%02d", count.index + 1)}"
    Role     = "fragment_generator"
    FromDate = "${format("%d", 19950000 + floor(count.index / 4) * 10000 + (count.index % 4) * 300 + 100) }"
    ToDate   = "${format("%d", 19950000 + floor(count.index / 4) * 10000 + ((count.index % 4) + 1) * 300 + 100 - 1) }"
    OutName  = "${format("train_%02d", count.index + 1)}"
  }
}

resource "aws_instance" "fragmentgenerator_eval" {
  count         = "${format("%d", var.fragmentgenerator_eval_count)}"
  ami           = "${var.fragmentgenerator_ami}"
  instance_type = "${var.fragmentgenerator_instance}"

  credit_specification {
    cpu_credits = "unlimited"
  }

  availability_zone      = "${var.availability_zone}"
  vpc_security_group_ids = ["${data.aws_security_group.selected.id}"]
  subnet_id         = "${data.aws_subnet.selected.id}"
  private_ip        = "${format("10.10.3.2%02d", count.index + 1)}"
  key_name          = "${var.key_name}"

  associate_public_ip_address = "true"

  tags = {
    Name     = "${format("fragment_generator_eval_%02d", count.index + 1)}"
    Role     = "fragment_generator"
    FromDate = "${format("%d", 20150000 + floor(count.index / 4) * 10000 + (count.index % 4) * 300 + 100) }"
    ToDate   = "${format("%d", 20150000 + floor(count.index / 4) * 10000 + ((count.index % 4) + 1) * 300 + 100 - 1) }"
    OutName  = "${format("eval_%02d", count.index + 1)}"
  }
}
