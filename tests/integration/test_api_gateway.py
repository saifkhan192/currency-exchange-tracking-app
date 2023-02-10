import os

import boto3
import pytest
import requests

stack_name = os.environ.get("AWS_SAM_STACK_NAME", "currency-exchange-tracking")
cloudformation = boto3.client("cloudformation")


class TestApiGateway:
    @pytest.fixture()
    def api_gateway_url(self):
        response = cloudformation.describe_stacks(StackName=stack_name)
        stack_outputs = response["Stacks"][0]["Outputs"]
        api_outputs = [
            output
            for output in stack_outputs
            if output["OutputKey"] == "GetCurrenciesUrl"
        ]
        return api_outputs[0]["OutputValue"]  # Extract url from stack outputs

    def test_get_currencies_handler(self, api_gateway_url):
        """Call the API Gateway endpoint and check the response"""
        print("Endpoint:", api_gateway_url)

        response = requests.get(api_gateway_url)
        data = response.json()

        assert response.status_code == 200
        assert "rates" in data
        assert "fluctuations" in data
        assert "USD" in data["rates"]
