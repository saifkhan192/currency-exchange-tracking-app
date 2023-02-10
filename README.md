# Currency Exchange Tracking Application
[![Author](http://img.shields.io/badge/author-@saifkhan192-blue.svg)](https://www.linkedin.com/in/saifullah-khan-02318086/)

A simple currency exchange tracking application using AWS Serverless environment and services.
Application relys on European Central Bank Data (https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

1. Exchange rates are fetched every day and stored in a dynamodb table
2. The application exposes a public REST API endpoint that provides current exchange rate information for all tracked currencies and their change compared to the previous day for all the tracked currencies.
3. So the customer can see current exchange rates
4. Customer can monitor exchange rate changes as compared to the previous day
4. To Do: Add single page web appliction to display the curency rates and a graph that shows the currency trends

## Language and Services being used

-   Python 3.9
-   AWS ApiGateway
-   AWS Lambda
-   AWS DynamoDB
-   AWS Events (Event Rules)
-   AWS Cloudformation
-   AWS SAM (Serverless Application Model)
-   AWS CloudWatch
-   AWS SAM CLI (v1.59.0)

## Project  structure
```sh
├── Makefile
├── README.md
├── daily.xml
├── functions
│   ├── __init__.py
│   ├── db.py
│   ├── handlers.py
│   ├── helper.py
│   ├── requirements.txt
│   └── samconfig.toml
├── pyproject.toml
├── samconfig.toml
├── template.yaml
└── tests
    ├── __init.py
    ├── __init__.py
    ├── integration
    │   ├── __init__.py
    │   └── test_api_gateway.py
    ├── requirements.txt
    └── unit
        ├── __init__.py
        └── test_handlers.py
```

## Setup
First Install SAM CLI on your system then you can deply the app on AWS cloud or run locally via `sam local start-api`

```bash
# creates venv and installs the `/functions/requirements.txt`
make setup_local 

# Paste your AWS access keys on the shell
export AWS_ACCESS_KEY_ID=<access-key>
export AWS_SECRET_ACCESS_KEY=<secret-key>
export AWS_DEFAULT_REGION=us-east-1
```

## Deploy application

```bash
# Paste your AWS access keys on the shell
export AWS_ACCESS_KEY_ID=<access-key>
export AWS_SECRET_ACCESS_KEY=<secret-key>
export AWS_DEFAULT_REGION=us-east-1

# Create new S3 bucket manually and update s3_bucket key in samconfig.toml file
# Run below command to build project usinng SAM and deploy
make build_and_deploy_dev
```

## Run Unit Tests

```bash
make run_unit_tests
```

## Run Integration Tests

```bash
make run_integration_tests
```

Note: Application should be deployed to AWS before running the tests
