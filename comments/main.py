from uuid import UUID, uuid4
from fastapi import Request, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from httpx import AsyncClient


class Comment(BaseModel):
    id: UUID | None
    content: str
    status: str | None = "pending"


app = FastAPI()
commentsByPost: dict[UUID, list[Comment]] = {}

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/posts/{post_id}/comments")
async def get_comments(post_id: UUID):
    return commentsByPost[post_id] if post_id in commentsByPost else []


@app.post("/posts/{post_id}/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: UUID, comment: Comment):
    comment.id = uuid4()
    if post_id in commentsByPost:
        commentsByPost[post_id].append(comment)
    else:
        commentsByPost[post_id] = [
            comment,
        ]
    # emit event
    async with AsyncClient() as ac:
        res = await ac.post(
            "http://event-bus-svc:80/events",
            json={
                "type": "commentCreated",
                "data": {
                    "id": str(comment.id),
                    "content": comment.content,
                    "postId": str(post_id),
                    "status": comment.status,
                },
            },
        )
    print("event bus: ", res.status_code)

    return {"msg": "comment create successfully"}


@app.post("/events")
async def receive_event(req: Request):
    body = await req.json()
    print("event: ", body["type"])

    if body["type"] == "commentModerated":
        for i, comment in enumerate(commentsByPost[UUID(body["data"]["postId"])]):
            if comment.id == UUID(body["data"]["id"]):
                commentsByPost[UUID(body["data"]["postId"])][i].status = body["data"]["status"]

        async with AsyncClient() as ac:
            res = await ac.post(
                "http://event-bus-svc:80/events",
                json={
                    "type": "commentUpdated",
                    "data": {
                        "id": body["data"]["id"],
                        "content": body["data"]["content"],
                        "postId": str(body["data"]["postId"]),
                        "status": body["data"]["status"],
                    },
                },
            )
        print("event bus: ", res.status_code)

    return {"msg": "event_reached"}
