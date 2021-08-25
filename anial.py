"""
Likes top 32 anilist activities every 70 seconds
"""

from __future__ import annotations
import graphql
import logging
import os
import dotenv


dotenv.load_dotenv()
TOKEN = os.environ.get("TOKEN")
headers = {
    "Authorization": "Bearer " + TOKEN
}

logger = logging.getLogger("anial")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("logs.txt")
logger.addHandler(file_handler)


def fetch_global_activity() -> list[int] | None:
    """Fetches top 32 activities from anilist and returns a list IDs of activities which are not liked."""
    try:
        data = graphql.query(graphql.QUERY_FETCH_ACTIVITY, headers, per_page=32)
    except graphql.HttpException:
        logger.exception("HttpException while fetching activities")
        return None
    except graphql.GraphqlException:
        logger.exception("GraphqlException while liking an activities")
        return None

    return [
        act["id"]
        for act in data["Page"]["activities"]
        if not act["isLiked"]
    ]

def like_activities(activity_ids: list[int]) -> None:
    """Toggles like for each activity ID in `activity_ids`"""
    for id in activity_ids:
        try:
            data = graphql.query(graphql.MUTATION_TOGGLE_LIKE, headers, likeable_id=id, type="ACTIVITY")
            logger.info("Liked activity ID = %d", data["ToggleLikeV2"]["id"])
        except graphql.HttpException:
            logger.exception("HttpException while liking an activity")
        except graphql.GraphqlException:
            logger.exception("GraphqlException while liking an activity")


if __name__ == "__main__":
    import time

    while True:
        activity_ids = fetch_global_activity()
        if activity_ids:
            like_activities(activity_ids)

        # Cooldown is a minute, 10 additional seconds to stay safe
        time.sleep(70)
