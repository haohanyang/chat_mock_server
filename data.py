import datetime
import models
import requests
from typing import List
import random

# number of users to fetch from API
USER_COUNT = 30
# number of groups to create
GROUP_COUNT = 20
# number of messages per conversation
MESSAGE_COUNT = 20
RANDOM_API = f"https://randomuser.me/api/?results={USER_COUNT}"


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Data(Singleton):
    def __init__(self):
        # Fetch data from API
        response = requests.get(RANDOM_API)
        if response.status_code != 200:
            raise Exception("Error: API request unsuccessful.")

        results: List[dict] = response.json()["results"]

        # Set up users
        self.users = [
            models.User(
                id=item["login"]["uuid"],
                clientId="u" + item["login"]["uuid"],
                username=item["login"]["username"],
                name=item["name"]["first"] + " " + item["name"]["last"],
                avatar=item["picture"]["large"],
                isOnline=random.choice([True, False]),
            )
            for item in results
        ]

        self.user: models.User = random.choice(self.users)

        # Set up groups
        self.groups: List[models.Group] = []

        creators = random.sample(self.users, GROUP_COUNT)
        for i in range(GROUP_COUNT):
            creator = creators[i]
            # Randomly choose users to be in the group
            groupMembers = random.sample(self.users, random.randint(1, USER_COUNT))
            # groupMembersIds = [user.id for user in groupMembers]

            # Make sure the creator is in the group
            if creator not in groupMembers:
                groupMembers.append(creator)

            group = models.Group(
                id=i,
                clientId="g"+str(i),
                name=f"Group {i}",
                avatar=creator.avatar,
                creator=creator,
                members=groupMembers,
            )
            self.groups.append(group)

            # set up messages
            self.userMessages: List[models.UserMessage] = []
            self.groupMessages: List[models.GroupMessage] = []

            for i in range(len(self.users)):
                # Don't send messages to yourself
                if self.users[i].id == self.user.id:
                    continue
                for j in range(MESSAGE_COUNT):
                    content = (
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"
                        "incididunt ut labore et dolore magna aliqua"
                    )
                    if j % 2 == 0:
                        self.userMessages.append(
                            models.UserMessage(
                                id=len(self.userMessages),
                                sender=self.users[i],
                                receiver=self.user,
                                content=content,
                                time=datetime.datetime.now().isoformat(),
                            )
                        )
                    else:
                        self.userMessages.append(
                            models.UserMessage(
                                id=len(self.userMessages),
                                sender=self.user,
                                receiver=self.users[i],
                                content=content,
                                time=datetime.datetime.now().isoformat(),
                            )
                        )

            for i in range(len(self.groups)):
                group = self.groups[i]
                for j in range(MESSAGE_COUNT):
                    content = (
                        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor"
                        "incididunt ut labore et dolore magna aliqua"
                    )
                    self.groupMessages.append(
                        models.GroupMessage(
                            id=len(self.groupMessages),
                            sender=group.members[j % len(group.members)],
                            receiver=group,
                            content=content,
                            time=datetime.datetime.now().isoformat(),
                        )
                    )

    def getUsers(self):
        return self.users

    # Get the current authenticated user
    def getCurrentUser(self):
        return self.user

    def getUser(self, username: str):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def getGroups(self):
        return self.groups

    def getGroup(self, id: int):
        for group in self.groups:
            if group.id == id:
                return group
        return None

    def getUserChats(self):
        return self.userMessages

    def getGroupChats(self):
        return self.groupMessages
