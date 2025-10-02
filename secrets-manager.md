# AWS Secrets Manager tips

Find the ID of the key(s) planned for deletion use:

`aws --region <REGION> secretsmanager list-secrets --include-planned-deletion`

To force-delete the secret:

`aws secretsmanager delete-secret --secret-id "<arn>" --force-delete-without-recovery --region <region>`
