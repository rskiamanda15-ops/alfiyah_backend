from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse # New import
from sqlalchemy.orm import Session
import asyncio # New import
import json # New import

from app.core.database import get_db
from app.core.security import get_current_admin
from app.schemas.segment import SegmentItem
from app.services.segmentation import segment_customers, _broadcast_segments # Corrected import

router = APIRouter()


@router.get("/stream")
async def stream_segments(db: Session = Depends(get_db), _admin=Depends(get_current_admin)):
    """Defines an SSE endpoint that streams segment updates to clients."""

    async def event_generator():
        # Broadcast initial segments when a client connects
        try:
            _broadcast_segments(db) # Send current segments immediately
        except Exception as e:
            # Handle error if initial broadcast fails, but don't break the stream
            print(f"Error broadcasting initial segments: {e}")

        queue = await broadcaster.subscribe()
        try:
            while True:
                message = await queue.get()
                # Only send segment updates through this stream
                if message.get("type") == "segment_updated":
                    yield f"data: {json.dumps(message)}\n\n"
        except asyncio.CancelledError:
            await broadcaster.unsubscribe(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/", response_model=list[SegmentItem])
def list_segments(db: Session = Depends(get_db), _admin=Depends(get_current_admin)):
    try:
        results = segment_customers(db, k=4)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return [
        SegmentItem(
            user_id=point.user_id,
            name=point.name,
            recency=point.recency,
            frequency=point.frequency,
            monetary=point.monetary,
            cluster=label,
            customer_segment=segment_label,
        )
        for point, label, segment_label in results
    ]
