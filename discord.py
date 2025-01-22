
import html2text

from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup


def send_message(discord_webhook_url: str, data: dict, include_examples: bool = False) -> None:

    LENGTH_LIMIT = 2000 # Discord message length limit

    date = data['date']
    link = data['link']
    id = data['question']['questionFrontendId']
    title = data['question']['title']
    is_paid_only = data['question']['isPaidOnly']
    difficulty = data['question']['difficulty']
    content = data['question']['content']
    if not include_examples:
        content = trim_examples(content)

    difficulty_highlight = {
        "Easy": "fix",
        "Medium": "prolog",
        "Hard": "ml",
    }

    message = "# 🔥  LeetCode Daily Challenge!\n"
    message += "📅  {}\n".format(date)
    if is_paid_only:
        message += "# 🔒  Premium question\n"
    message += "## {}\n".format(id + ". " + title)
    message += "```{}\n{}\n```\n".format(difficulty_highlight[difficulty], difficulty)
    message += "{}".format(html_to_markdown(content))

    link_str = "\n🔗  [Link to the problem]({})".format("https://leetcode.com" + link)

    if len(message) + len(link_str) > LENGTH_LIMIT:
        clippingIndicator = "\n\n ⋯ \n"
        message = message[:LENGTH_LIMIT - len(link_str) - len(clippingIndicator)] + clippingIndicator
    
    message += link_str

    webhook = DiscordWebhook(url=discord_webhook_url, username="LeetCode Daily Challenge", content=message)
    webhook.execute()


def trim_examples(content: str) -> str:
    soup = BeautifulSoup(content, 'html.parser')
    result = ""
    for tag in soup.contents:
        if tag.name:
            if tag.find(class_="example"):
                break
            result += str(tag)
    return result


def html_to_markdown(html_string: str) -> str:
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_images = True
    markdown = h.handle(html_string)
    return markdown

