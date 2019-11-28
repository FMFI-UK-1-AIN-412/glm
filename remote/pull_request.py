class PullRequest:
    def __init__(self, user: str, source_branch: str, target_branch: str):
        self.user = user
        self.source_branch = source_branch
        self.target_branch = target_branch

    def __repr__(self):
        return f"{self.user}: {self.source_branch} -> {self.target_branch}"
