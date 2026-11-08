from types import SimpleNamespace

from pydantic_ai.messages import ModelResponse, ToolReturnPart

from adapter.inbound.agent.search import extract_jobs


def test_extract_jobs():
    postings = [
        {
            "source": "arbeitsagentur",
            "id": "123",
            "company": "Example GmbH",
            "title": "Data Analyst",
            "location": "Berlin",
        }
    ]

    result = SimpleNamespace(
        all_messages=lambda: [
            ModelResponse(
                parts=[
                    ToolReturnPart(
                        tool_name="search_jobs",
                        content=postings,
                        tool_call_id="test-123",
                    )
                ]
            )
        ]
    )

    jobs = extract_jobs(result)

    assert len(jobs) == 1
    assert jobs[0].title == "Data Analyst"
    assert jobs[0].source == "arbeitsagentur"
