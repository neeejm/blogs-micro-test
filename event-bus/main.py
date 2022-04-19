from fastapi import Request, FastAPI
from httpx import AsyncClient


app = FastAPI()
events: list[dict] = []


@app.get("/events")
async def get_all_events():
    return events


@app.post("/events")
async def publish_event(req: Request):
    print("test")
    body = await req.body()
    events.append(body)
    print(body)

    async with AsyncClient() as ac:
        # publish event to posts service
        res = await ac.post("http://posts-svc:80/events", data=body)
        print("posts service: ", res.status_code)

        # publish event to comments service
        res = await ac.post("http://comments-svc:80/events", data=body)
        print("comments service: ", res.status_code)

        # publish event to query service
        res = await ac.post("http://query-svc:80/events", data=body)
        print("query service: ", res.status_code)

        # publish event to moderation service
        res = await ac.post("http://moderation:80/events", data=body)
        print("moderation service: ", res.status_code)

    return {"msg": "events published"}
