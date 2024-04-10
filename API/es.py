import config
from elasticsearch import Elasticsearch, helpers
from typing import Dict
import warnings

warnings.filterwarnings(action='ignore')

INDEX_NAME = config.INDEX_NAME
ESKNN_HOST = config.ESKNN_HOST

es = Elasticsearch(
    hosts=[ESKNN_HOST]
)

class ESKNN:

    def __init__(self) -> None:
        pass

    def create_index(self) -> None:

        body = {}

        try:
            result = es.indices.create(
                index=INDEX_NAME,
                body=body,
                ignore=400
            )
            if 'error' in result:
                return 2
            else:
                return 1
        except:
            return 0

    def search_document(self, query, field_name) -> Dict:

        result = es.search(
            request_timeout=30,
            index=INDEX_NAME,
            body={
                'query': {
                    'multi_match': {
                        'query': query,
                        'fields': field_name
                    }
                }
            }
        )

        return result

    def insert_document(self, document) -> None:
      
        try:
            result = es.index(
                index=INDEX_NAME,
                body=document
            )
            return result
        except Exception as e:
            print("Failed to insert document:", str(e))
