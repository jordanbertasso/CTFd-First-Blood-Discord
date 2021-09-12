from json.decoder import JSONDecodeError
from typing import Optional
from team import Team
from api_session import session as s


def get_team_by_user_id(user_id: int) -> Team:
    team_id = get_team_id(user_id)

    if team_id is None:
        return Team(-1, "Unknown")

    team_name = get_team_name(team_id)

    if team_name is None:
        return Team(team_id, "Unknown")

    return Team(team_id, team_name)


def get_team_id(user_id: int) -> Optional[int]:
    res = s.get(f"users/{user_id}", json=True)

    try:
        data = res.json()['data']
        return data['team_id']
    except (JSONDecodeError, KeyError) as e:
        print(e)
        return None


def get_team_name(team_id: int) -> Optional[str]:
    res = s.get(f"teams/{team_id}", json=True)

    try:
        data = res.json()['data']
        return data['name']
    except (JSONDecodeError, KeyError) as e:
        print(e)
        return None
