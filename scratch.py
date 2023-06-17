import weaviate
import json
import os

weaviate_key = os.environ.get("WEAVIATE_KEY")
cohere_key = os.environ.get("COHERE_API_KEY")

client = weaviate.Client(
    url = "https://vectorised-sandwiches-avj3xesi.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
    additional_headers={
        "X-Cohere-Api-Key": cohere_key,
    },
    timeout_config = (20, 240)
)

messages_class_object = {
    "class": "Messages",
    "description": "Slack messages",
    "vectorizer": "text2vec-cohere",
    "moduleConfig": {
        "text2vec-cohere": {
            "model": "multilingual-22-12",
            "truncate": "RIGHT"
        },
        "generative-cohere": {
            "model": "command-xlarge-nightly",
        }
    },
    "vectorIndexConfig": {
        "distance": "dot"
    },
    "properties": [
    {
        "name": "text",
        "dataType": [ "text" ],
        "description": "Text",
        "moduleConfig": {
            "text2vec-cohere": {
                "skip": False,
                "vectorizePropertyName": False
            }
        }
    },
    {
        "name": "source",
        "dataType": [ "text" ],
        "moduleConfig": { "text2vec-cohere": { "skip": True } }
    },
    {
        "name": "user_id",
        "dataType": [ "text" ],
        "moduleConfig": { "text2vec-cohere": { "skip": True } }
    },
    {
        "name": "channel_name",
        "dataType": [ "text" ],
        "moduleConfig": { "text2vec-cohere": { "skip": True } }
    },
    {
        "name": "message_timestamp",
        "dataType": [ "date" ],
        "moduleConfig": { "text2vec-cohere": { "skip": True } }
    },
    {
        "name": "thread_timestamp",
        "dataType": [ "date" ],
        "moduleConfig": { "text2vec-cohere": { "skip": True } }
    },
    {
        "name": "channel_id",
        "dataType": [ "text" ],
        "moduleConfig": { "text2vec-cohere": { "skip": True } }
    },
    ]
}

client.schema.delete_class("Messages")
client.schema.create_class(messages_class_object)

# messages_class_obj = {
#     "class": "Question",
#     "vectorizer": "text2vec-huggingface",
#     "moduleConfig": {
#         "text2vec-huggingface": {
#             "model": "sentence-transformers/all-MiniLM-L6-v2",
#             "options": {
#                 "waitForModel": True
#             }
#         }
#     }
# }

# client.schema.create_class(messages_class_obj)

import requests
url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

with client.batch(batch_size=100) as batch:
    for i, d in enumerate(data):
        print(f"importing messages: {i+1}")

        properties = {
            "source": d["__Source"],
            "user_id": d["User_ID"],
            "channel_name": d["Channel_Name"],
            "message_timestamp": d["Message_Timestamp"],
            "thread_timestamp": d["Thread_Timstamp"],
            "channel_id": d["Channel_ID"],
            "text": d["__Text"]
        }

        client.batch.add_data_object(
            properties,
            "Messages",
        )


# Making a query

nearText = {"concepts": ["biology"]}

response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=4))


# "__Source"
# "User_ID"
# "Channel_Name"
# "Message_Timestamp"
# "Thread_Timstamp"
# "Channel_ID"
# "__Text"