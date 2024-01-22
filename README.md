
# AWS Lambda Passport Status Checker with Telegram Notifications

## Overview

This project involves deploying a Python script to AWS Lambda, which checks the status of a passport application at regular intervals and sends updates via Telegram. The script is triggered every 15 minutes to verify if there's a new update on the status page and notifies the user accordingly.

## Prerequisites

Before you start, you need to have the following:

- An AWS account.
- Basic understanding of AWS services, especially Lambda and CloudWatch.
- Terraform installed on your computer.
- Python installed on your computer.
- Telegram account and a Telegram bot. [Here's how to create a Telegram bot](https://core.telegram.org/bots#6-botfather).

## Setup and Deployment

### Step 0: Clone the Repository

1. **Clone the repository**:
   - Clone this repository to your local machine.

### Step 1: AWS Configuration

1. **AWS CLI Setup**:
   - Install AWS CLI: [AWS CLI Installation Guide](https://aws.amazon.com/cli/).
   - Configure AWS CLI with your credentials: Run `aws configure` and enter your AWS Access Key, Secret Key, and default region.

### Step 2: Terraform Configuration

1. **Install Terraform**:
   - Follow the instructions [here](https://learn.hashicorp.com/tutorials/terraform/install-cli) to install Terraform.

2. **Initialize Terraform**:
   - In the directory with your Terraform files (`main.tf`, `variables.tf`, `terraform.tfvars`), run:
     ```
     terraform init
     ```

### Step 3: Setting Up Terraform Variables

1. **Create `terraform.tfvars`** file in the same directory as your Terraform files.:
   - Open `terraform.tfvars`.
   - Set the values for `telegram_token`, `telegram_chat_id`, `passport_series`, and `passport_number` with your own values.

### Step 4: Deploying with Terraform

1. **Run Terraform Apply**:
   - Execute:
     ```
     terraform apply
     ```
   - Review the plan and type `yes` to proceed.

### Step 5: Verification

1. **Check AWS Lambda**:
   - Log into your AWS Console.
   - Go to the Lambda service and check if your function (`UAPassportCheck`) exists.
   - You can test the function manually here.

2. **Check CloudWatch Events**:
   - In the AWS Console, navigate to CloudWatch.
   - Verify that there's a rule set to trigger your Lambda function every 15 minutes.

3. **Check Telegram Bot**:
   - Send a message to your Telegram bot.
   - Ensure you receive updates from the Lambda function.

## Troubleshooting

- **Lambda Function Errors**: Check the logs in CloudWatch for any errors during Lambda execution.
- **Terraform Errors**: Ensure all Terraform configuration files are correct and all required values are provided.
- **Telegram Bot Issues**: Verify that the bot token and chat ID are correct.

## Conclusion

Your AWS Lambda Passport Status Checker is now set up and will notify you via Telegram every 15 minutes if there's an update on the passport status page.
