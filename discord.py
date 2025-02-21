
import html2text

from discord_webhook import DiscordWebhook
from bs4 import BeautifulSoup

def send_message(discord_webhook_url: str, data: dict, include_examples: bool = False, include_constraints: bool = True) -> None:

    LENGTH_LIMIT = 2000 # Discord message length limit
    
    difficulty_highlight = {
        "Easy": "fix",
        "Medium": "prolog",
        "Hard": "ml",
    }

    date = data['date']
    link = data['link']
    id = data['question']['questionFrontendId']
    title = data['question']['title']
    is_paid_only = data['question']['isPaidOnly']
    difficulty = data['question']['difficulty']
    content = data['question']['content']

    # Split content
    question, examples, constraints = split_html(content)
    if include_examples:
        question += examples
    if include_constraints:
        question += constraints

    message = "# 🔥  LeetCode Daily Challenge!\n"
    message += "📅  {}\n".format(date)
    if is_paid_only:
        message += "# 🔒  Premium question\n"
    message += "## {}\n".format(id + ". " + title)
    message += "```{}\n{}\n```\n".format(difficulty_highlight[difficulty], difficulty)
    message += "{}".format(html_to_markdown(question))

    link_str = "\n🔗  [Link to the problem]({})".format("https://leetcode.com" + link)

    # Truncate message if it exceeds the limit
    if len(message) + len(link_str) > LENGTH_LIMIT: 
        clippingIndicator = "\n\n ⋯ \n"
        message = message[:LENGTH_LIMIT - len(link_str) - len(clippingIndicator)] + clippingIndicator
    
    message += link_str

    webhook = DiscordWebhook(url=discord_webhook_url, username="LeetCode Daily Challenge", content=message)
    webhook.execute()


def split_html(content: str):
    soup = BeautifulSoup(content, 'html.parser')
    problem, examples, constraints = "", "", ""
    segment = 1

    # Iterate over top-level elements
    for elem in soup.find_all(recursive=False):
        elem_html = str(elem)
        if segment == 1:
            if elem.find("strong", class_="example"):
                segment = 2
        elif segment == 2:
            if elem.find("strong", string=lambda t: t and t.strip() == "Constraints:"):
                segment = 3
        
        if segment == 1:
            problem += elem_html
        elif segment == 2:
            examples += elem_html
        else:
            constraints += elem_html

    return problem, examples, constraints


def html_to_markdown(html_string: str) -> str:
    h = html2text.HTML2Text()
    h.body_width = 0
    h.ignore_images = True
    markdown = h.handle(html_string)
    return markdown

