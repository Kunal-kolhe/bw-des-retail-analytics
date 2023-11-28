import boto3
from utils.vaultUtil import authenticate_with_approle

test = authenticate_with_approle()
print(test)