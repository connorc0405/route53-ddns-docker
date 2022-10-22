Easy DDNS deployment for home use!

Requirements:
* AWS credentials
* Hosted Zone ID (found in AWS console)

Here's a suggested IAM policy. It might contain one extra policy that's unnecessary, but it will get the job done:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "route53:GetChange",
                "route53:ChangeResourceRecordSets"
            ],
            "Resource": [
                "arn:aws:route53:::change/*",
                "arn:aws:route53:::hostedzone/<zoneid>"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "route53:ListHostedZones",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "route53:ListResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/<zoneid>
        }
    ]
}
```

Here's a suggested compose file:

```
version: "3.9"
  services:
    ddns:
      image: ddns:latest
      build: <path_to_repo>
      environment:
        - DOMAIN=<your_domain>
        - ZONEID=<your_zoneid>
      volumes:
        - /path/to/.aws:/root/.aws
      restart: always
```
