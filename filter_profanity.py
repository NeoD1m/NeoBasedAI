from typing import List
import re


def ban_filter(message: str, ban_list: List[str]) -> str:
    ban_regex = r"|".join(ban_list)
    return re.sub(ban_regex, "БАН НА ТВИЧЕ", message)
