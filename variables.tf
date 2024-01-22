variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "aws_credentials_file" {
  type    = list(string)
  default = ["$HOME/.aws/credentials"]
}

variable "aws_profile" {
  type    = string
  default = "default"
}

variable "telegram_token" {
  description = "Telegram bot token"
  type        = string
}

variable "telegram_chat_id" {
  description = "Telegram chat ID"
  type        = string
}

variable "passport_series" {
  type = string
}

variable "passport_number" {
  type = number
}
