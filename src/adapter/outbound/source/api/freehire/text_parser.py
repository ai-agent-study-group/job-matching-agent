"""freehire 공고 본문(HTML)을 글자로 바꾸기."""

import re
from html.parser import HTMLParser

# 앞뒤로 줄을 바꾸는 태그. 목록 항목(li)과 br은 앞에서만 바꿈
BLOCKS = {"p", "div", "ul", "ol", "tr", "h1", "h2", "h3", "h4", "h5", "h6"}


class _TextParser(HTMLParser):
    """HTML에서 글자만 모은다. 문단 · 목록은 줄바꿈으로, 목록 항목은 "- "로."""

    def __init__(self):
        super().__init__()
        self.parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in BLOCKS or tag in ("li", "br"):
            self.parts.append("\n")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in BLOCKS:
            self.parts.append("\n")

    def handle_data(self, data):
        # HTML은 공백 · 줄바꿈을 한 칸으로 보여 줌
        self.parts.append(re.sub(r"\s+", " ", data))


def to_text(html: str) -> str:
    """HTML을 줄 구분이 살아 있는 글자로 바꾼다. 태그는 지우고 &amp; 같은 기호는 원래 글자로."""
    parser = _TextParser()
    parser.feed(html)
    parser.close()
    lines = [line.strip() for line in "".join(parser.parts).split("\n")]
    # 태그마다 넣은 줄바꿈이 겹친 곳은 빈 줄 하나로
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
