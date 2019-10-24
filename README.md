[![Build Status](https://travis-ci.org/dpetzold/aws-log-parser.svg?branch=master)](https://travis-ci.org/dpetzold/aws-log-parser)
[![Coverage Status](https://coveralls.io/repos/github/dpetzold/aws-log-parser/badge.svg?branch=master)](https://coveralls.io/github/dpetzold/aws-log-parser?branch=master)

# aws-log-parser

Parse AWS LoadBalancer and CloudFront logs into Python3 data classes.

## CloudFront Example

```python
    >>> from aws_log_parser import log_parser, LogType
    >>> log_data = ['''2014-05-23	01:13:11	FRA2	182	192.0.2.10	GET	d111111abcdef8.cloudfront.net	/view/my/file.html	200	www.displaymyfiles.com	Mozilla/4.0%20(compatible;%20MSIE%207.0;%20Windows%20NT%205.1)	-	zip=98101	RefreshHit	MRVMF7KydIvxMWfJIglgwHQwZsbG2IhRJ07sn9AkKUFSHS9EXAMPLE==	d111111abcdef8.cloudfront.net	http	-	0.001	-	-	-	RefreshHit	HTTP/1.1''']
    >>> entry = log_parser(log_data, LogType.CloudFront)[0]
    >>> entry
    CloudFrontWebDistributionLogEntry(
        date=datetime.date(2014, 5, 23),
        time=datetime.time(1, 13, 11),
        edge_location='FRA2',
        sent_bytes=182,
        client_ip='192.0.2.10',
        http_method='GET',
        host='d111111abcdef8.cloudfront.net',
        uri='/view/my/file.html',
        status_code=200,
        referrer='www.displaymyfiles.com',
        user_agent=mozilla_user_agent_fixture,
        uri_query=None,
        cookie='zip=98101',
        edge_result_type='RefreshHit',
        edge_request_id='MRVMF7KydIvxMWfJIglgwHQwZsbG2IhRJ07sn9AkKUFSHS9EXAMPLE==',
        host_header='d111111abcdef8.cloudfront.net',
        protocol='http',
        received_bytes=None,
        time_taken=0.001,
        forwarded_for=None,
        ssl_protocol=None,
        ssl_cipher=None,
        edge_response_result_type='RefreshHit',
        protocol_version='HTTP/1.1',
        fle_encrypted_fields='',
    )
    >>> entry.timestamp
    datetime.datetime(2014, 5, 23, 1, 13, 11, 0, tzinfo=datetime.timezone.utc)
    >>> entry.country
    'United States'
    >>> entry.hostname
    'rate-limited-proxy-66-249-91-41.google.com'
    >>> entry.network
    'Google'
    >>> str(entry.user_agent)
    'Other / Windows / Other'
```

## LoadBalancer Example

```python
    >>> from aws_log_parser import log_parser, LogType
    >>> log_data = ['''h2 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 10.0.1.252:48160 10.0.0.66:9000 0.000 0.002 0.000 200 200 5 257 "GET https://10.0.2.105:773/ HTTP/2.0" "curl/7.46.0" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 "Root=1-58337327-72bd00b0343d75b906739c42" "-" "-" 1 2018-07-02T22:22:48.364000Z "redirect" "https://example.com:80/" "-"''']
    >>> entry = log_parser(log_data, LogType.LoadBalancer)[0]
    >>> entry
    LoadBalancerLogEntry(
        http_type=HttpType('h2'),
        timestamp=datetime.datetime(
            2018, 7, 2, 22, 23, 0, 186641,
            tzinfo=datetime.timezone.utc,
        ),
        elb='app/my-loadbalancer/50dc6c495c0c9188',
        client=Host(ip='10.0.1.252', port=48160),
        target=Host(ip='10.0.0.66', port=9000),
        request_processing_time=0.000,
        target_processing_time=0.002,
        response_processing_time=0.000,
        elb_status_code=200,
        target_status_code=200,
        received_bytes=5,
        sent_bytes=257,
        http_request=HttpRequest(
            method='GET',
            url='https://10.0.2.105:773/',
            query={},
            protocol='HTTP/2.0',
        ),
        user_agent=curl_user_agent_fixture,
        ssl_cipher='ECDHE-RSA-AES128-GCM-SHA256',
        ssl_protocol='TLSv1.2',
        target_group_arn='arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067',
        trace_id='Root=1-58337327-72bd00b0343d75b906739c42',
        domain_name=None,
        chosen_cert_arn=None,
        matched_rule_priority=1,
        request_creation_time=datetime.datetime(
            2018, 7, 2, 22, 22, 48, 364000,
            tzinfo=datetime.timezone.utc,
        ),
        actions_executed=['redirect'],
        redirect_url='https://example.com:80/',
        error_reason=None,
    )
```
