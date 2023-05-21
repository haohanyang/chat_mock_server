from typing import List
from pydantic import BaseModel
import random
import datetime


# User and groups


class Base(BaseModel):
    name: str
    avatar: str
    clientId: str

    def __hash__(self) -> int:
        return clientId.__hash__()

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, Base):
            return False
        return self.clientId == other.clientId


class User(Base):
    id: str
    username: str
    isOnline: bool


class Group(Base):
    id: int
    members: List[User] = []
    creator: User


class Membership(BaseModel):
    id: int
    member: User
    group: Group


# Messages
class Message(BaseModel):
    id: int
    sender: User
    content: str
    time: datetime.datetime = datetime.datetime.now().isoformat()
    read: bool = False
    delivered: bool = False


class UserMessage(Message):
    receiver: User


class GroupMessage(Message):
    receiver: Group
