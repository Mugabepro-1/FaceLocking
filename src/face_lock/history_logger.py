import time


class HistoryLogger:
    def __init__(self, identity: str):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.filename = f"{identity}_history_{timestamp}.txt"

    def log(self, action: str):
        t = time.strftime("%H:%M:%S")
        with open(self.filename, "a") as f:
            f.write(f"{t} | {action} | detected\n")
