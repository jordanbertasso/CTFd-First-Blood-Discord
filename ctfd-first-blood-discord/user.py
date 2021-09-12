from team import Team
from util import get_team_by_user_id


class User:
    id: int
    name: str
    team: Team

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

        self.team = get_team_by_user_id(self.id)
