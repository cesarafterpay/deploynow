module "testdeploynow" {
  source = "git@github.com:AfterpayTouch/afterpay-terraform-modules.git//ecs-service-public"
  application_name = "testdeploynow"
  image_ecr = "paylater/testdeploynow"
  image_version = var.application_version
  terraform_configuration = "testdeploynow"
  account_id = var.account_id
  state_bucket = var.state_bucket

  application_vars = var.application_vars
  container_port = "80"
  health_check_path = "health"

  task_min_count = "1"
  task_max_count = "1"
}

output "service_fqdn" {
  value = module.testdeploynow.service_endpoint
}

output "service_security_group" {
  value = module.testdeploynow.aws_security_group_id
}
