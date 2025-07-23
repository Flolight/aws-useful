
## Lambda

Request a log group for specific request id
```
fields @message|
filter @requestId like /4f6b7964-d97e-4f4a-aa4e-e4f79bfe9b7e/
```

With exceptions
```
fields @message|
filter @message like /Exception/
```

The slowest requests
```
filter @type = “REPORT” |
fields @requestId, @billedDuration |
sort by @billedDuration desc
```

## Bedrock

```
fields @timestamp, @message
| filter @message like /\"type\"\s*:\s*\"thinking\"/
| filter @message like /assumed-role\/IAM\.ROLE\.LAMBDA\//
| sort @timestamp desc
```
