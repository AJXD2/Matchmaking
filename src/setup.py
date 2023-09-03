import logging
from src.classes.Mainloop import MainLoop
from flask.logging import default_handler

mainloop = MainLoop()


def get_logger() -> logging.Logger:
    root = logging.getLogger()
    root.addHandler(default_handler)
    # root.addHandler(mail_handler)
    return root
