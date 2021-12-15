# AWS useful

A nice list of useful remarks and tips for AWS builders
<!-- ## Table of content

* [Database](#database)
* * [RDS](#rds)

* Authent
* * Shibboleth

* API Gateway
* * Forward headers -->
# Table of content
- [AWS useful](#aws-useful)
- [Table of content](#table-of-content)
  - [Database](#database)
    - [RDS](#rds)
  - [Authent](#authent)
    - [Shibboleth](#shibboleth)
      - [I have Loadbalancer ip instead of client issue](#i-have-loadbalancer-ip-instead-of-client-issue)
  - [API Gateway](#api-gateway)
    - [Forward headers](#forward-headers)


## Database
### RDS

Calling aws_s3.query_export_to_s3 (pour ton export de data de rds vers s3):

https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/postgresql-s3-export.html#postgresql-s3-export-examples-basic



Same for import:

https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html



Possible RDS instance-types:
https://aws.amazon.com/rds/instance-types/

RDS Postgres pricing:

https://aws.amazon.com/rds/postgresql/pricing/?pg=pr&loc=3


## Authent

### Shibboleth

#### I have Loadbalancer ip instead of client issue

To map the ip of the client into the variable used on the server
<RequestMap REMOTE_ADDR="X-Forwarded-For">

```html
<Sessions lifetime="28800" timeout="3600" relayState="ss:mem" checkAddress="false" consistentAddresse=”false” handlerSSL="false" cookieProps="https">
<Sessions/>
```
  	  

## API Gateway

### Forward headers

To forward headers passed to API gateway to Lambda, use the following

```json
{
  "body" : $input.json('$'),
  "headers": {
    #foreach($param in $input.params().header.keySet())
    "$param": "$util.escapeJavaScript($input.params().header.get($param))" #if($foreach.hasNext),#end
    
    #end  
  }
}
```
