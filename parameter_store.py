import boto3

# Call restored parameters in System Manager Prameter Store
def get_params(*args):
    ssm = boto3.client('ssm', 'ap-northeast-1')
    
    response = ssm.get_parameters(
        Names=list(args),
        WithDecryption=True
    )
    
    values = []
    for parameter in response['Parameters']:
        values.append(parameter['Value'])
    
    return values