locals {
  terraform_configuration = "testdeploynow"
  account_name = lookup(var.accounts, var.account_id, "test")
}

terraform {
  required_version = "0.12.24"

  backend "s3" {
    key = "testdeploynow/testdeploynow.tfstate"
    encrypt = true
    dynamodb_table = "terraformstatelock"
    session_name = "terraform-testdeploynow-configuration"
    region = "ap-southeast-2"
  }
}

data "terraform_remote_state" "network" {
  backend = "s3"
  workspace = "${terraform.workspace}"
  config = {
    bucket = "${var.state_bucket}"
    key = "network/network.tfstate"
    encrypt = true
    dynamodb_table = "terraformstatelock"
    region = "ap-southeast-2"
    role_arn = "arn:aws:iam::${var.account_id}:role/terraform-state-manager"
    session_name = "terraform-testdeploynow-remote-state-network"
  }
}

provider "aws" {
  region = "${data.terraform_remote_state.network.outputs.region}"
  assume_role {
    role_arn = "arn:aws:iam::${var.account_id}:role/terraform-paylater-deploynow-ecs"
    session_name = "terraform-testdeploynow-aws-provider"
  }

  version = "~> 2.0"
}

data "aws_caller_identity" "current_account" {}
