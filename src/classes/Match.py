from uuid import uuid4
from src.classes.Player import Player


class Match:
    def __init__(self, level=None) -> None:
        self.level = level
        self.players = []
        self.ready = False
        self.code = str(uuid4())[:8]

    def add_player(self, player: Player):
        if not self.players:
            self.level = player.level
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(Player)

    def get_players(self):
        return self.players

    def start_game(self):
        raise NotImplementedError("Added soon, this feature will be.")

    def __iter__(self):
        return iter(self.players)


if __name__ == "__main__":
    m = Match("I")
    print(m.code)
