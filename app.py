# app.py

from time import sleep
from src.classes.Player import Player
from src.setup import mainloop
from src.setup import get_logger

from flask import Flask
from src.matchmaking_bp import matchmaking_bp, queue_manager  # Import the blueprint


app = Flask(__name__)


queue_manager.add_player_to_queue(Player("testsubject1", "IRON"))
queue_manager.add_player_to_queue(Player("testsubject2", "IRON"))
print("Added player")
# Register the blueprint with a URL prefix
app.register_blueprint(matchmaking_bp, url_prefix="/matchmaking")

if __name__ == "__main__":
    app.run()
