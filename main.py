
import requests
import logging
import os
import discord

from dotenv import load_dotenv

load_dotenv()

log_format = "%(asctime)s %(filename)s:%(name)s:%(lineno)d [%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
)
logger = logging.getLogger(__name__)

def gather_daily_challenge() -> dict:
    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
    }
    query = """
        query getDailyProblem {
            activeDailyCodingChallengeQuestion {
                date
                link
                question {
                    questionFrontendId
                    title
                    isPaidOnly
                    difficulty
                    content
                }
            }
        }
    """

    response = requests.post(url, json={"query": query}, headers=headers)
    
    if response.status_code != 200:
        raise response.raise_for_status()
    
    return response.json()


def main() -> int:
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    INCLUDE_EXAMPLES = os.getenv("INCLUDE_EXAMPLES").lower() == "true"

    try:
        data = gather_daily_challenge()
    except Exception as e:
        logger.error(f"Failed to gather daily challenge: {e}")
        return 1
    
    discord.send_message(DISCORD_WEBHOOK_URL, data['data']['activeDailyCodingChallengeQuestion'], INCLUDE_EXAMPLES)

    return 0


if __name__ == "__main__":
    exit(main())
