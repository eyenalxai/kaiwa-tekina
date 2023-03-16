from functools import reduce

from bs4 import BeautifulSoup
from markdown import markdown

from app.util.display.format import (
    closing_tag,
    opening_tag,
    self_closing_tag_no_space,
    self_closing_tag_space,
)
from app.util.display.tags import get_html_tags


def replace_img_with_a_tag_bs4(*, html_text: str) -> str:
    soup = BeautifulSoup(html_text, "html.parser")

    for img_tag in soup.find_all("img"):
        img_tag.name = "a"
        img_tag["href"] = img_tag["src"]
        del img_tag["alt"]  # noqa: WPS420 Found wrong keyword del
        del img_tag["src"]  # noqa: WPS420 Found wrong keyword del

    return str(soup)


def remove_tag(text: str, tag: str) -> str:
    replace_with = ""

    return (
        text.replace(opening_tag(tag=tag), replace_with)
        .replace(closing_tag(tag=tag), replace_with)
        .replace(self_closing_tag_no_space(tag=tag), replace_with)
        .replace(self_closing_tag_space(tag=tag), replace_with)
        .replace("<img", "<a")  # I'm sorry
    )


def remove_tags(*, text: str, tags_to_remove: list[str]) -> str:
    return reduce(remove_tag, tags_to_remove, text)


def replace_header_tag(text: str, tag: str) -> str:
    return text.replace(
        opening_tag(tag=tag),
        opening_tag(tag="b"),
    ).replace(
        closing_tag(tag=tag),
        closing_tag(tag="b"),
    )


def replace_header_tags(text: str, header_tags: list[str]) -> str:
    return reduce(replace_header_tag, header_tags, text)


def markdown_to_html(*, text: str) -> str:
    html = replace_img_with_a_tag_bs4(
        html_text=markdown(text, extensions=["fenced_code"]),
    )
    header_tags, tags_to_remove = get_html_tags()

    return replace_img_with_a_tag_bs4(
        html_text=replace_header_tags(
            text=remove_tags(text=html, tags_to_remove=tags_to_remove),
            header_tags=header_tags,
        ),
    )
