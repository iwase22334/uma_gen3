#####################################
## vpc
#####################################
resource "aws_vpc" "vpc_main" {
  cidr_block           = "${var.root_segment}"
  enable_dns_hostnames = true
  enable_dns_support   = true
  instance_tenancy     = "default"

  tags = {
    Name = "${var.app_name}-vpc"
    UsedBy = "uma_gen2"
  }
}

resource "aws_subnet" "vpc_main-private-subnet1" {
  vpc_id            = "${aws_vpc.vpc_main.id}"
  cidr_block        = "${var.segment_gen02}"
  availability_zone = "${var.availability_zone}"

  tags = {
    Name = "${var.app_name}-private-subnet1"
    UsedBy= "uma_gen2"
  }
}

resource "aws_internet_gateway" "gateway" {
  vpc_id = "${aws_vpc.vpc_main.id}"

  tags = {
    Name = "${var.app_name}-gateway"
    UsedBy = "uma_gen2"
  }

}

resource "aws_vpc_endpoint" "s3ep" {
  vpc_id       = "${aws_vpc.vpc_main.id}"
  service_name = "com.amazonaws.${var.region}.s3"

  tags = {
    Name = "${var.app_name}-vpc_endpoint"
    UsedBy = "uma_gen2"
  }
}

#####################################
## routing
#####################################
resource "aws_route_table" "routingtable" {
  vpc_id = "${aws_vpc.vpc_main.id}"
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = "${aws_internet_gateway.gateway.id}"
  }

  tags = {
    Name = "${var.app_name}-route-table"
    UsedBy = "uma_gen2"
  }
}

resource "aws_route_table_association" "subnet-association" {
  subnet_id      = "${aws_subnet.vpc_main-private-subnet1.id}"
  route_table_id = "${aws_route_table.routingtable.id}"
}

resource "aws_vpc_endpoint_route_table_association" "s3-association" {
  route_table_id  = "${aws_route_table.routingtable.id}"
  vpc_endpoint_id = "${aws_vpc_endpoint.s3ep.id}"
}

#####################################
## security group
#####################################
resource "aws_security_group" "all_ssh" {
  vpc_id      = "${aws_vpc.vpc_main.id}"
  name        = "terraform_security_group"

  # SSH access from anywhere
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "all_ssh"
    UsedBy = "uma_gen2"
  }
}

