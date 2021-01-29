import json
import os
import requests


def main():
    SPACE_ID = os.environ["SPACE_ID"]
    ENVIRONMENT_ID = os.environ["SPACE_ID"]
    ACCESS_TOKEN = os.environ["MGNT"]
    BASE_URL = f"https://api.contentful.com/spaces/{SPACE_ID}/environments/{ENVIRONMENT_ID}"

    url = BASE_URL + "/content_types"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

    response = requests.get(url, headers=headers)
    content_types = json.loads(response.text)

    for content_type in content_types["items"]:
        content_type_id = content_type["sys"]["id"]
        entries_url = BASE_URL + f"/entries?content_type={content_type_id}"
        response = requests.get(entries_url, headers=headers)
        entries_collection = json.loads(response.text)
        print(
            content_type_id, ",", content_type["name"], ",", entries_collection["total"]
        )


if __name__ == "__main__":
    main()