from uuid import UUID, uuid4
from fastapi import Request, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from httpx import AsyncClient


class Post(BaseModel):
    id: UUID | None
    title: str
    content: str


app = FastAPI()
posts: list[Post] = []

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello_world():
    return {"msg": "hello world"}


@app.get("/posts")
async def get_posts():
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post.id = uuid4()
    # add to db(mem)
    posts.append(post)
    # emit event
    async with AsyncClient() as ac:
        res = await ac.post(
            "http://localhost:8004/events",
            json={
                "type": "postCreated",
                "data": {"id": str(post.id), "title": post.title, "content": post.content},
            },
        )
    print("event bus: ", res.status_code)

    return {"msg": "post created successfully"}


@app.post("/events")
async def receive_event(req: Request):
    body = await req.json()
    print("event: ", body["type"])

    return {"msg": "event reached"}


@app.on_event("startup")
async def on_start():
    print("v2")
