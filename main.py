import time
from typing import List

from fastapi import APIRouter, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from data import Data
from models import User, Group, UserMessage, GroupMessage

# Mock in-memory database
db = Data()

app = FastAPI(
    title="Mock chat server",
    description="A mock chat server for testing purposes and API prototyping",
)

userRouter = APIRouter(
    prefix="/users",
    tags=["User controller"],
    responses={404: {"description": "Not found"}},
)

groupRouter = APIRouter(
    prefix="/groups",
    tags=["Group controller"],
    responses={404: {"description": "Not found"}},
)

chatRouter = APIRouter(
    prefix="/chats",
    tags=["Chat controller"],
    responses={404: {"description": "Not found"}},
)


# User routes
@userRouter.get("/", tags=["users2"])
async def getAllUsers():
    return db.users


@userRouter.get("/me")
async def getCurrentUser():
    return db.getCurrentUser()


@userRouter.get("/{username}")
async def getUser(username: str):
    user = db.getUser(username)
    if user is not None:
        return user
    return Response(content="User not found", status_code=404)


@userRouter.get("/{username}/groups")
async def getJoinedGroups(username: str):
    user = db.getUser(username)
    if user is None:
        return Response(content="User not found", status_code=404)

    groups: List[Group] = []
    for group in db.getGroups():
        if user in group.members:
            groups.append(group)
    return groups


# Group routes
@groupRouter.get("/")
async def getAllGroups():
    return db.getGroups()


@groupRouter.get("/{id}")
async def getGroup(id: int):
    group = db.getGroup(id)
    if group is not None:
        return group
    return Response(content="Group not found", status_code=404)


@groupRouter.post("/")
async def createGroup(group: Group):
    db.getGroups().append(group)


@groupRouter.get("/{id}/members")
async def getGroupMembers(id: int):
    group = db.getGroup(id)
    if group is not None:
        return group.members
    return Response(content="Group not found", status_code=404)


@groupRouter.post("/{id}/members")
async def addGroupMember(id: int, user: User):
    group = db.getGroup(id)
    if group is not None:
        if user not in group.members:
            group.members.append(user)
            return Response(content="ok", status_code=201)
        return Response(content="User already in group", status_code=403)
    return Response(content="Group not found", status_code=404)


# chat controller


@chatRouter.get("/{id}/users")
async def getAllUserChats():
    return db.getUserChats()


@chatRouter.get("/{id}/groups")
async def getAllGroupChats():
    return db.getGroupChats()


@chatRouter.get("/users/{username1}/{username2}")
async def getUserChat(username1: str, username2: str):
    time.sleep(2)
    chats: List[UserMessage] = []
    for message in db.getUserChats():
        if (
            message.sender.username == username1
            and message.receiver.username == username2
        ) or (
            message.sender.username == username2
            and message.receiver.username == username1
        ):
            chats.append(message)
    return chats


@chatRouter.get("/groups/{id}")
async def getGroupChat(id: int):
    time.sleep(2)
    group = db.getGroup(id)
    if group is None:
        return Response(content=f"Group {id} not found", status_code=404)

    chats: List[GroupMessage] = []
    for message in db.getGroupChats():
        if message.receiver.id == id:
            chats.append(message)
    return chats


@chatRouter.post("/users")
async def sendUserMessage(message: UserMessage):
    time.sleep(2)

    db.getUserChats().append(message)
    return Response(content="ok", status_code=201)


@chatRouter.post("/groups")
async def sendGroupMessage(message: GroupMessage):
    time.sleep(2)

    db.getGroupChats().append(message)
    return Response(content="ok", status_code=201)


@app.get("/")
async def root():
    return Response(content="This is a mock server", status_code=200)


app.include_router(userRouter)
app.include_router(groupRouter)
app.include_router(chatRouter)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)
