from uuid import uuid4


class Player:
    def __init__(self, username, level) -> None:
        self.username = username
        self.level = level
        self.uuid = str(uuid4())[:8]
        self.match = None

    def __repr__(self) -> str:
        return f"{self.username} ({self.level})"

    def to_dict(self):
        return {"name": self.username, "rank": self.level}

    def __str__(self) -> str:
        return f"{self.username} ({self.level})"
