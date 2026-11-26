from unittest.mock import Mock

from fastapi import FastAPI

import observability


def test_configure_logfire_without_token_does_not_send(monkeypatch):
    configure = Mock()
    instrument_pydantic_ai = Mock()
    instrument_httpx = Mock()
    monkeypatch.setattr(observability.logfire, "configure", configure)
    monkeypatch.setattr(observability.logfire, "instrument_pydantic_ai", instrument_pydantic_ai)
    monkeypatch.setattr(observability.logfire, "instrument_httpx", instrument_httpx)

    observability.configure_logfire()

    configure.assert_called_once_with(
        service_name="job-matching-agent",
        send_to_logfire="if-token-present",
    )
    instrument_pydantic_ai.assert_called_once_with(include_content=False)
    instrument_httpx.assert_called_once_with(
        capture_request_body=False,
        capture_response_body=False,
    )


def test_fastapi_instrumentation_drops_parsed_request_arguments(monkeypatch):
    instrument = Mock()
    monkeypatch.setattr(observability.logfire, "instrument_fastapi", instrument)

    app = FastAPI()
    observability.instrument_fastapi(app)

    mapper = instrument.call_args.kwargs["request_attributes_mapper"]
    assert mapper(Mock(), {"values": {"body": {"resume_text": "private"}}}) == {}
