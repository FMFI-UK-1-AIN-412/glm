from datetime import datetime

class IssueComment:
    def __init__(self, body: str, creator: str, timestamp: float):
        self.body = body
        self.creator = creator
        self.datetime = datetime.fromtimestamp(timestamp)

    def __repr__(self) -> str:
        return f"{self.datetime.ctime()} - {self.creator}: {self.body}"
