from typing import List
from pydantic import BaseModel
import random
import datetime


# User and groups


class Base(BaseModel):
    name: str
    avatarUrl: str


class User(Base):
    id: str
    username: str
    isOnline: bool

    def __hash__(self) -> int:
        return id.__hash__()

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if self is other:
            return True
        if not isinstance(other, User):
            return False
        return self.id == other.id


class Group(Base):
    id: int
    members: List[User] = []
    creator: User


# Messages
class Message(BaseModel):
    id: int
    sender: User
    content: str
    time: datetime.datetime
    read: bool = False
    delivered: bool = False


class UserMessage(Message):
    receiver: User


class GroupMessage(Message):
    receiver: Group
