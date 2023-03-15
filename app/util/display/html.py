from functools import reduce

from markdown import markdown

from app.util.display.format import (
    closing_tag,
    opening_tag,
    self_closing_tag_no_space,
    self_closing_tag_space,
)
from app.util.display.tags import get_html_tags


def remove_tag(text: str, tag: str) -> str:
    replace_with = ""

    return (
        text.replace(opening_tag(tag=tag), replace_with)
        .replace(closing_tag(tag=tag), replace_with)
        .replace(self_closing_tag_no_space(tag=tag), replace_with)
        .replace(self_closing_tag_space(tag=tag), replace_with)
    )


def remove_tags(text: str, tags_to_remove: list[str]) -> str:
    return reduce(remove_tag, tags_to_remove, text)


def replace_tag(text: str, tag: str) -> str:
    replace_with = opening_tag(tag="b")

    return text.replace(
        opening_tag(tag=tag),
        replace_with,
    ).replace(
        closing_tag(tag=tag),
        replace_with,
    )


def replace_header_tags(text: str, header_tags: list[str]) -> str:
    return reduce(replace_tag, header_tags, text)


def markdown_to_html(text: str) -> str:
    html = markdown(text, extensions=["fenced_code"])
    header_tags, tags_to_remove = get_html_tags()

    return replace_header_tags(
        text=remove_tags(text=html, tags_to_remove=tags_to_remove),
        header_tags=header_tags,
    )
