"""text_parser: 공고 본문 HTML을 글자로 바꾸기."""

from adapter.outbound.source.api.freehire.text_parser import to_text


def test_to_text_drops_script_and_style():
    """script · style 안의 내용은 버린다.

    목적: HTMLParser는 태그만 지우고 script · style 안의 CSS · JS 코드는 글자로 넘겨서,
    그대로 두면 본문에 코드가 섞임.
    기대 결과: style과 script 사이의 <p>Body</p> → "Body"만.
    """
    html = "<style>.x{color:red}</style><p>Body</p><script>alert(1)</script>"

    assert to_text(html) == "Body"
