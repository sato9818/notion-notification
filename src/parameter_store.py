import os
import json
import boto3

# Call restored parameters in System Manager Prameter Store
def get_params(*args):
    try:
        if len(args) == 0:
            raise ValueError("Parametar name error. Please set parameter names.")

        ssm = boto3.client('ssm', endpoint_url=os.getenv("ENDPOINT_URL"))
        print(f"GET Params from SSM Parameter Store: {args}")
        response = ssm.get_parameters(
            Names=list(args),
            WithDecryption=True
        )

        if len(args) > 1:
            values = []
            for name in list(args):
                value = next((d["Value"] for d in response['Parameters'] if d["Name"] == name), None)
                values.append(value)
            return values

        else:
            value = response['Parameters'][0]["Value"]
            print(f"value: {value}")
            return value
    except Exception as e:
        print(f"An error occurred: {e}")
