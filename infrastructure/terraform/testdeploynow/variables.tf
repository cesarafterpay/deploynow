variable "state_bucket" {
  description = "S3 bucket for storing terraform state."
}

variable "application_vars" {
  default = [
    {
      name = "TEST_ENV_VARIABLE"
      value = "test-environment-variable-value"
    }
  ]
}

variable "application_version" {
  default = "latest"
}

variable "account_id" {}

variable "accounts" {
  type = map
  description = "Allows us to map an account number to an account name"
  default = {
    "568431661506" = "alpha"
    "723236915308" = "beta"
    "687512651472" = "psi"
    "830726149330" = "omega"
    "361053881171" = "factory"
  }
}