# src/matchmaking/queue_manager.py

import queue
from src.classes.Match import Match
from src.classes.Player import Player
from src.config import MAX_MATCHES, MIN_MATCHES, MIN_PLAYERS, RANKS


class QueueManager:
    def __init__(self):
        self.matchmaking_queue = queue.Queue()
        self.matches = []

    def generate_match(self, level=None):
        if len(self.matches) >= MAX_MATCHES:
            return {
                "error": True,
                "msg": "max matches",
                "code": "",
            }

        m = Match(level)
        self.matches.append(m)
        return {"error": False}

    def generate_matches(self, num: int = MAX_MATCHES):
        print(num)
        for i in range(num):
            resp = self.generate_match()
            if resp.get("error", None) == True:
                break

    def remove_player_from_queue(self, player_name):
        players_in_queue = []
        removed_player = None

        while not self.matchmaking_queue.empty():
            player = self.matchmaking_queue.get()

            if player.username == player_name:
                removed_player = player  # Save the removed player
            else:
                players_in_queue.append(player)

        # Put back the remaining players into the queue
        for player in players_in_queue:
            self.matchmaking_queue.put(player)

        return removed_player

    def add_player_to_queue(self, player_details):
        self.matchmaking_queue.put(player_details)

    def get_all_players(self):
        players = []
        for i in range(self.get_queue_size()):
            player_d = self.matchmaking_queue.get()
            players.append(player_d)
            self.matchmaking_queue.put(player_d)
        return players

    def group_players_by_rank(players):
        grouped_players = {}

        for player in players:
            rank = player["rank"]
            if rank not in grouped_players:
                grouped_players[rank] = []
            grouped_players[rank].append(player)

        return grouped_players

    def task(self):
        players = self.get_all_players()
        for b in players:
            b: Player

            match_found = False
            for x in self.matches:
                if match_found:
                    break
                if x.ready:
                    print("denied", b.username, "a match")
                    continue
                x: Match
                if x.level is None:
                    x.add_player(b)
                    b.match = x
                    print(f"[*] Found empty game for: {str(b)}")
                    self.remove_player_from_queue(b.username)
                    match_found = True
                elif x.level == b.level:
                    x.add_player(b)
                    b.match = x
                    print(f"[*] Found game for: {str(b)}")
                    self.remove_player_from_queue(b.username)
                    match_found = True

                else:
                    print(f"[*] Waiting on a game for {str(b)}")

            # print(f"Processed player: {str(b)}")
        for i in self.matches:
            if i.ready:
                continue
            if len(i.players) - 1 >= MIN_PLAYERS:
                i.ready = True
                print("[*] Made match ready")

    def get_player_from_queue(self):
        try:
            q = self.matchmaking_queue.get()
            for i in list(q):
                self.matchmaking_queue.put(i)

            return q
        except queue.Empty:
            return None

    def get_by_name(self, name):
        for i in range(self.get_queue_size()):
            q = self.matchmaking_queue.get()
            if q.uuid == name:
                return q
            self.matchmaking_queue.put(q)

        return None

    def get_by_uuid(self, uuid):
        for i in range(self.get_queue_size()):
            q = self.matchmaking_queue.get()

            if q.uuid == uuid:
                return q
            self.matchmaking_queue.put(q)

        return None

    def search_matches_uuid(self, uuid):
        for i in self.matches:
            for x in i.players:
                print(x)
                if x.uuid == uuid:
                    return x

        return None

    def get_queue_size(self):
        return self.matchmaking_queue.qsize()
