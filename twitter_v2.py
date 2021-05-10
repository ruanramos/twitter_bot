import requests
import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import json


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def get_rules(headers, bearer_token):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(headers, bearer_token, rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(headers, delete, bearer_token):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "from:ninfasupernova", "tag": "drielli"},
        {"value": "from:ruanframos", "tag": "ruan"}
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        headers=headers,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))


def get_stream(headers, set, bearer_token, api_key, api_secret, token, token_secret):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", headers=headers, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )

    print("STREAM IS UP")
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            tweet = json_response['data']
            rules = json_response['matching_rules']

            print("GOT A NEW TWEET")
            print(json.dumps(json_response, indent=4, sort_keys=True))

            print("LIKING TWEET")
            url = "https://api.twitter.com/1.1/favorites/create.json"

            querystring = {"id": tweet['id']}

            auth = OAuth1(api_key, api_secret, token, token_secret)
            headers = {
                "content-type": "application/json"
            }

            like_response = requests.request("POST", url, auth=auth, data="", headers=headers, params=querystring)

            if like_response != 200:
                print("ERROR LIKING TWEET")

            print("TWEET LIKED")


def main():
    load_dotenv()
    headers = create_headers(os.getenv('BEARER_TOKEN'))
    # set = set_rules(headers, None, os.getenv('BEARER_TOKEN'))
    # rules = get_rules(headers, os.getenv('BEARER_TOKEN'))
    # delete = delete_all_rules(headers, os.getenv('BEARER_TOKEN'), rules)
    get_stream(headers, None, os.getenv('BEARER_TOKEN'), os.getenv('API_KEY'), os.getenv('API_SECRET'),
               os.getenv('ACCESS_TOKEN_RUAN'), os.getenv('ACCESS_SECRET_RUAN'))


if __name__ == "__main__":
    main()
