# src/matchmaking.py

import logging
from time import sleep
from flask import Blueprint, request
from src.setup import mainloop
from src.classes.Player import Player
from src.matchmaking.queue_manager import QueueManager


matchmaking_bp = Blueprint("matchmaking", __name__)
queue_manager = QueueManager()
queue_manager.generate_matches()
mainloop.add_task(queue_manager.task)
mainloop.start()


@matchmaking_bp.route("/join_queue", methods=["POST"])
def join_queue():
    player_details = request.get_json()  # Get player details from the request
    player = Player(player_details["name"], player_details["rank"])
    queue_manager.add_player_to_queue(player)
    # Return a response indicating successful queueing
    return {"message": "ok", "pcode": player.uuid}, 200


@matchmaking_bp.route("/get_players", methods=["GET"])
def get_players():
    players = queue_manager.get_all_players()
    return {"message": "ok", "players": players}, 200


@matchmaking_bp.route("/ready/<code>")
@matchmaking_bp.route("/ready")
def match_ready(code=None):
    if code is None:
        return {"error": "please provide a code"}

    p = queue_manager.search_matches_uuid(code)
    if p is None:
        return {"message": "failed", "error": "player_not_found"}
    if p.match is None:
        status = "waiting"
    if p.match is not None:
        status = p.match.ready
    return {"message": "ok", "match_status": status}
