import boto3
import sys
# print("Before Append:", sys.path)
#import utils
# sys.path.append('c:\\workspace\\bwprojects\\snowflakeDemo\\bw-des-retail-analytics\\utils')
# print("After Append:", sys.path)
from vaultUtil import VaultClient
from awsUtil import AWSConnector
from snowUtil import SnowflakeConnector

VAULT_URL = "http://127.0.0.1:8200"
ROLE_ID = "2dabf32f-c39c-54f8-e083-6d7c7f31f5e7"
SECRET_ID = "0b5b40c7-b87c-eb23-8a09-87b7835ade2b"
SECRET_PATH = "secret/data/aws"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")


aws_access_key = secret_data['data']['accesskey']
aws_secret_key = secret_data['data']['secretkey']

region = 'us-east-1'  # Replace with your preferred AWS region


client='iam'
aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

# Access the S3 client through the instance
iam_client = aws_connector.aws_client_conn

# Now you can use s3_client to perform S3 operations
response = iam_client.list_groups()

print("IAM groups:", response)



# Replace these with your Snowflake account details
account = 'bjb35914.us-east-1'

SECRET_PATH = "secret/data/snow"

vault_client = VaultClient(VAULT_URL, ROLE_ID, SECRET_ID, SECRET_PATH)
token = vault_client.authenticate_with_approle()

if token:
    secret_data = vault_client.get_secret(token)
    if secret_data:
        print("Secret data:", secret_data)
    else:
        print("Failed to retrieve secret.")
else:
    print("Failed to authenticate with AppRole.")


user = secret_data['data']['serviceusername']
password = secret_data['data']['serviceuserpassword']


# user = 'Kunal-kolhe'
# password = 'Kunal@6772'
warehouse = 'COMPUTE_WH'
database = 'SNOWFLAKE_SAMPLE_DATA'
schema = 'TPCH_SF1'

# Create an instance of SnowflakeConnector
snowflake_conn = SnowflakeConnector(account, user, password, warehouse, database, schema)

# Connect to Snowflake
snowflake_conn.connect()

# Execute a query
query_result = snowflake_conn.execute_query("SELECT * from SUPPLIER LIMIT 5")

# Print the result
print("Current Date in Snowflake:", query_result)

# Close the connection
snowflake_conn.close_connection()