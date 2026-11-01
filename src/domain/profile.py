from pydantic import BaseModel


class SearchQuery(BaseModel):
    """채용공고 검색에 사용할 조건."""

    keywords: str = ""
    location: str = ""
