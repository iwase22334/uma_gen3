#####################################
## security group
#####################################

data "aws_subnet" "selected" {
    filter {
        name   = "tag:Name"
        values = ["${var.app_name}-private-subnet1"]       # insert value here
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
resource "aws_instance" "processed_db" {
    ami               = "${var.db_ami}"
    instance_type     = "${var.db_instance}"

    credit_specification {
      cpu_credits = "unlimited"
    }

    availability_zone = "${var.availability_zone}"
    vpc_security_group_ids = ["${data.aws_security_group.selected.id}"]
    subnet_id         = "${data.aws_subnet.selected.id}"
    private_ip        = "${var.uma_processed_ip}"
    key_name          = "${var.key_name}"

    associate_public_ip_address = "true"

    tags = {
        Name = "processed_db"
        Role = "processeddb"
    }
}

resource "aws_instance" "dataprocessor" {
    count = "${format("%d", var.dataprocessor_count)}"
    ami = "${var.dataprocessor_ami}"
    instance_type = "${var.dataprocessor_instance}"

    credit_specification {
      cpu_credits = "unlimited"
    }

    availability_zone = "${var.availability_zone}"
    vpc_security_group_ids = ["${data.aws_security_group.selected.id}"]
    subnet_id         = "${data.aws_subnet.selected.id}"
    private_ip        = "${format("10.10.3.1%02d", count.index + 1)}"
    key_name          = "${var.key_name}"

    associate_public_ip_address = "true"

    tags = {
        Name = "${format("dataprocessor_%02d", count.index + 1)}"
        Role = "dataprocessor"
        Peer = "${var.uma_processed_ip}"
        FromDate = "${format("%d", 19900000 + count.index * 10000) }"
        ToDate = "${format("%d", 19900000 + (count.index + 1) * 10000 - 1)}"
    }
}
