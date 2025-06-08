import requests
import json
import os
import parameter_store

class NotionApiClient:
    NOTION_API_TOKEN = parameter_store.get_params('NOTION_API_TOKEN')
    NOTION_DATABASE_QUERY_API_URL = os.getenv('NOTION_DATABASE_QUERY_API_URL')
    NOTION_VERSION='2022-06-28'
    
    def post_database_query(payload):
        headers = {'Authorization': f"Bearer {NotionApiClient.NOTION_API_TOKEN}", 'Notion-Version': NotionApiClient.NOTION_VERSION, 'Content-Type': 'application/json', 'accept': 'application/json'}
        
        print(f"Post Notion API : {NotionApiClient.NOTION_DATABASE_QUERY_API_URL}")
        print(f"payload: {payload}")
        res = requests.post(NotionApiClient.NOTION_DATABASE_QUERY_API_URL, json=payload, headers=headers)
        data = json.loads(res.text)
        return data
