import json
import os
import requests
import time


def main():
    SPACE_ID = os.environ["SPACE_ID"]
    ENVIRONMENT_ID = os.environ["ENVIRONMENT_ID"]
    ACCESS_TOKEN = os.environ["MGNT"]
    BASE_URL = (
        f"https://api.contentful.com/spaces/{SPACE_ID}/environments/{ENVIRONMENT_ID}"
    )

    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    url = BASE_URL + "/content_types"

    response = requests.get(url, headers=headers)
    content_types = json.loads(response.text)

    for content_type in content_types["items"]:
        time.sleep(0.5)
        content_type_id = content_type["sys"]["id"]
        content_type_name = content_type["name"]
        print(f"Examining {content_type_name}")

        entries_url = BASE_URL + f"/entries?content_type={content_type_id}"
        response = requests.get(entries_url, headers=headers)
        entries_collection = json.loads(response.text)
        total = entries_collection["total"]
        children = parse_all_entries(BASE_URL, content_type_id, entries_collection)

        print(f"{content_type_name} ({content_type_id}):")
        print(f"Entries: {total}, Children entries: {children}\n")


def parse_all_entries(BASE_URL, content_type_id, entries_collection):
    ACCESS_TOKEN = os.environ["MGNT"]
    total = entries_collection["total"]
    children = 0
    skip = 0
    while skip < total:
        time.sleep(0.5)
        entries_url = (
            f"{BASE_URL}/entries?content_type={content_type_id}&limit=100&skip={skip}"
        )
        response = requests.get(entries_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
        entries_collection = json.loads(response.text)
        children = children + get_children_entries_of_collection(entries_collection)
        skip = skip + 100
    return children


def get_children_entries_of_collection(entries_collection):
    children = 0
    for entry in entries_collection["items"]:
        for key, value in entry["fields"].items():
            val = value["en-US"]
            try:
                if isinstance(val, dict):
                    if val["sys"]["type"] == "Link":
                        children = children + 1
                elif isinstance(val, list):
                    for i in val:
                        if i["sys"]["type"] == "Link":
                            children = children + 1
            except Exception as e:
                pass
    return children


if __name__ == "__main__":
    main()