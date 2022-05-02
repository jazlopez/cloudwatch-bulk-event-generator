# cloudwatch-bulk-event-generator

This repository contains a project whose purpose is to add dummy data for AWS cloudwatch metrics testing.
It writes dummy log events into a given log group. You can specify an existing log stream or let the program to
create a new log stream for you.

### CONFIGURATION

The program uses boto3 to access AWS Cloudwatch API. You should configure an AWS profile before run the script. Such profile is used
to authorize API operations over the specified log group and log stream.

By default the program uses ```default```profile; but can be overriden.

### INSTALLATION

Install required packages before running program

```shell
pip install -r requirements.txt
```

### BASIC USAGE

You need to pass at least one mandatory arguments

- ```--log-group-name YOUR_AWS_LOG_GROUP```

It creates a new log stream into specified log group using default AWS proile.

```shell
python main.py --log-group-name :YOUR_AWS_LOG_GROUP
```

### OPTIONAL ARGUMENTS

Specify a log stream.

- ```--log-stream-name YOUR_AWS_LOG_STREAM``` 

Specify an AWS profile name.  

- ```--profile YOUR_AWS_PROFILE```

### TEST EVENTS

By default it will post 10 new events with the following signature:
```
{'timestamp': 1651450731941, 'message': '{"log": "POST /de-eec-subscription/oauth2/token HTTP/1.1 500 - -"}'}
```

#### TEST EVENTS CUSTOMIZATIONS

Change the event URL that appear in the log message:

- ```--event-url http://some_url --event-status-code 404```

will change the log event message to the following:
  
  ```{'timestamp': 1651450731941, 'message': '{"log": "POST http://some_url HTTP/1.1 404 - -"}'}```  

You can also specify how many events you want to submit when you run the program:  

```--total-events 50```

### HELP

Run the help option to get program assistenance.

```shell
    python main.py --help
```



### CONTACT

[Jaziel Lopez](https://github.com/jazlopez)
