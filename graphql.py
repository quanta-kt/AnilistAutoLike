from typing import Iterable
import requests
import json


URL = "https://graphql.anilist.co/"

QUERY_FETCH_ACTIVITY = """
query($per_page: Int) {
  Page(perPage: $per_page) {
    activities(sort: ID_DESC) {
      __typename
      ...on TextActivity {
        id
        isLiked
      }
      ...on ListActivity {
        id
        isLiked
      }
      ...on MessageActivity {
        id
        isLiked
      }
    }
  }
}
"""

MUTATION_TOGGLE_LIKE = """
mutation($likeable_id: Int, $type: LikeableType) {
  ToggleLikeV2(id: $likeable_id, type: $type) {
    ...on TextActivity {
        id
      }
      ...on ListActivity {
        id
      }
      ...on MessageActivity {
        id
      }
  }
}
"""

class HttpException(Exception):
    def __init__(self, response) -> None:
        super().__init__(f"Http call returned status code {response.status_code}", response)

class GraphqlException(Exception):

    def __init__(self, errors: Iterable[dict]) -> None:
        messages = (
            GraphqlException.format_error(err)
            for err in errors
        )
        super().__init__("\n".join(messages))

    @staticmethod
    def format_error(err: dict) -> str:
        locations = err.get("locations")
        if locations:
            locations = "\nLocations:\n" + "\n".join(f"line: {loc['line']}\ncolumn: {loc['column']}" for loc in locations)
        else:
            locations = ""
        
        validations = err.get("validation")
        if validations:
            validations = "\nValidations:\n" + "\n".join(f"{v.key}: {v.value}" for v in validations)
        else:
            validations = ""

        return "Error: " + err["message"] + locations + validations


def query(query, headers=None, **variables) -> dict:
    response = requests.post(
        URL,
        headers=headers,
        json=dict(
            query=query,
            variables=variables,
        ),
    )

    if not response.ok:
        try:
            data = response.json()
            errors = data.get("errors")
        except json.JSONDecodeError:
            errors = None
        if errors:
            raise GraphqlException(errors)
        else:
            raise HttpException(response)

    data = response.json()
    return data["data"]
