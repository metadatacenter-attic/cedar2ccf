import os
import pycedar.CedarClient

user_id = os.getenv('CEDAR_USER_ID')
api_key = os.getenv('CEDAR_API_KEY')

client = CedarClient(user_id, api_key)


def get_instances():
    instances = client.get_instances(
        is_based_on='some template id',
        limit='an integer or blank')
    print(instances)
