
from fastapi import APIRouter

router = APIRouter()

@router.get("/market")
def market_findings(sample: bool = True):
    sample_doc = {
        "source": "reddit",
        "thread_url": "https://www.reddit.com/r/example/thread/abc123",
        "title": "Pain point: vendor lock-in with XYZ tool",
        "signal": {"sentiment": -0.62, "intensity": 0.74, "tags": ["lock-in", "pricing", "support"]},
        "excerpts": [
            "We can't export data without paying an absurd fee.",
            "Support tickets sit for weeks."
        ]
    }
    return {"items": [sample_doc] if sample else []}
