import json
from uuid import UUID
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from httpx import AsyncClient


class Comment(BaseModel):
    id: UUID
    content: str
    status: str

    # def __init__(self, id: UUID, content: str) -> None:
    #     self.id = id
    #     self.content = content


class Post(BaseModel):
    id: UUID
    title: str
    content: str
    comments: list[Comment]

    # def __init__(self, id: UUID, title: str, content: str) -> None:
    #     self.id = id
    #     self.content = content
    #     self.title = title
    #     self.comments = []


def handle_events(body: dict):
    match body["type"]:
        case "postCreated":
            posts[UUID(body["data"]["id"])] = Post(
                id=UUID(body["data"]["id"]),
                title=body["data"]["title"],
                content=body["data"]["content"],
                comments=[],
            )
            return {"msg": "post created successfuly"}

        case "commentCreated":
            posts[UUID(body["data"]["postId"])].comments.append(
                Comment(
                    id=body["data"]["id"],
                    content=body["data"]["content"],
                    status=body["data"]["status"],
                )
            )
            return {"msg": "comment created successfuly"}

        case "commentUpdated":
            for i, comment in enumerate(posts[UUID(body["data"]["postId"])].comments):
                if comment.id == UUID(body["data"]["id"]):
                    posts[UUID(body["data"]["postId"])].comments[i].status = body["data"]["status"]
            return {"msg": "comment updated successfuly"}


app = FastAPI()
posts: dict[UUID, Post] = {}

origins = ["http://localhost:3000"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])


@app.get("/posts")
async def get_full_posts():
    return posts


@app.post("/events")
async def receive_event(req: Request):
    body = await req.json()

    handle_events(body)


@app.on_event("startup")
async def sync_data():
    async with AsyncClient() as ac:
        res = await ac.get("http://localhost:8004/events")
        events = res.json()

        for event in events:
            handle_events(json.loads(event))
