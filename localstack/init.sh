#!/bin/bash

# Parameter File
PARAM_FILE="/etc/localstack/init/ready.d/.params.txt"

# Read file
while IFS='=' read -r NAME VALUE
do
    # SKip line
    if [[ -z "$NAME" || "$NAME" == \#* ]]; then
        continue
    fi

    # Put SSM Params
    awslocal ssm put-parameter --cli-input-json "{\"Name\":\"$NAME\", \"Value\":\"$VALUE\", \"Type\":\"String\"}" --region ap-northeast-1 --overwrite
    echo "Put prameter: $NAME=$VALUE"

done < "$PARAM_FILE"

echo "Complete init.sh"
