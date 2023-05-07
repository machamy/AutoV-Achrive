import requests, json
from dataclasses import dataclass, field

"""
floor : 노래와 난이도, 점수, 맥콤 등 모든 데이터
"""

URL = 'https://v-archive.net/api/archive/'
BOARD_LIST = json.loads(requests.get('https://v-archive.net/db/boards.json').text)
print(f"{URL=}")
print(f"{BOARD_LIST=}")


class User:
    """
    V-ARCHIVE 상에 저장된 USER
    """
    def __init__(self, name, userNo = 0,token=None):
        """
        :param name: 유저의 ID
        :param token: 유저의 token(account.txt)
        """
        self.name = name
        self.token = token
        self.userNo = userNo
        floors = []

    def refresh(self, button, board):
        print(f"refesh {self.name}:{button}, {board}")
        obj = get(self.name, button, board)
        if not obj["success"]:
            print(f"{self.name}의 {button}키, {board} 난이도 데이터를 불러오는데 실패했습니다.")
            print(f"이유 : {obj['message']}")
            return
        floors = obj['floors']
        for f in floors:
            print(f['floorNumber'])
            for p in f['patterns']:
                if not p['score']:
                    continue
                print(p)

    def update(self):
        """
        미구현
        :return: 
        """
        if not self.token:
            print(f"{self.name}의 데이터 업데이트를 하는데 실패했습니다")
            print(f"이유 : token 없음")


class Board:
    pass

class Floor:
    def __init__(self, floorNumber: int = 0, patterns: list[dict] = list()):
        self.floorNumber = floorNumber
        self.patterns = patterns

    def add_pattern(self, pattern):
        self.patterns.append(pattern)

def get(name, button, board):
    button = str(button)
    board = str(board)

    headers = {'Content-Type': 'application/json'}
    if button not in [4, 5, 6, 8]:
        button = 6
    if board not in BOARD_LIST:
        board = BOARD_LIST[6]

    url = URL + f"{name}/board/{button}/{board}"
    result = json.loads(requests.get(url, headers).text)
    return result


def post(userNo,token, cleardata):
    """
    미구현
    :param userNo: 
    :param cleardata: 
    :return: 
    """
    header = {'Content-Type': 'application/json'
        , "Authorization": str(userNo)}
    body = {
        'name': '',
        'dlc': '',
        'composer':'',
        "button": 6,
        "pattern": "SC",
        "score": 90.9,
        "maxCombo": 0
    }
    url = f"{URL}/client/open/{userNo}/score"
    res = requests.post(url,body)
    print(res)

