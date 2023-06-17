import weaviate
import json
import os

weaviate_key = os.environ.get("WEAVIATE_KEY")

client = weaviate.Client(
    url = "https://vectorised-sandwiches-avj3xesi.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_key),
)

class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-huggingface",
    "moduleConfig": {
        "text2vec-huggingface": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "options": {
                "waitForModel": True
            }
        }
    }
}

client.schema.create_class(class_obj)

import requests
url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

with client.batch(batch_size=100) as batch:
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }

        client.batch.add_data_object(
            properties,
            "Question",
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