from fastapi import FastAPI, Request
from httpx import AsyncClient


app = FastAPI()


@app.post("/events")
async def moderate(req: Request):
    body = await req.json()
    print("event: ", body["type"])

    if body["type"] == "commentCreated":
        status = "approved" if "nya" not in body["data"]["content"] else "reject"
        print("status: ", status)
        # emit event
        async with AsyncClient() as ac:
            res = await ac.post(
                "http://localhost:8004/events",
                json={
                    "type": "commentModerated",
                    "data": {
                        "id": body["data"]["id"],
                        "content": body["data"]["content"],
                        "postId": body["data"]["postId"],
                        "status": status,
                    },
                },
            )
        print("event bus: ", res.status_code)
    return {"msg": "event reached"}
