from fastapi import FastAPI

app = FastAPI(title="job-matching-agent API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
