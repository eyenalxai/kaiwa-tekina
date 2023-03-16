def opening_tag(*, tag: str) -> str:
    return "<{tag}>".format(tag=tag)


def closing_tag(*, tag: str) -> str:
    return "</{tag}>".format(tag=tag)


def self_closing_tag_no_space(*, tag: str) -> str:
    return "<{tag}/>".format(tag=tag)


def self_closing_tag_space(*, tag: str) -> str:
    return "<{tag} />".format(tag=tag)
