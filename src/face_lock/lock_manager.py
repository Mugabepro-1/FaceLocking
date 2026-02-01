import time
from .action_detector import ActionDetector
from .history_logger import HistoryLogger


class FaceLockManager:
    def __init__(self, target_identity="John", timeout=3, min_similarity=0.66):
        self.target_identity = target_identity
        self.timeout = timeout
        self.min_similarity = min_similarity

        self.locked = False
        self.locked_bbox = None
        self.last_seen = 0

        self.action_detector = ActionDetector()
        self.logger = None

    def try_lock(self, name, similarity, bbox):
        if not self.locked:
            if name == self.target_identity and similarity >= self.min_similarity:
                self.locked = True
                self.locked_bbox = bbox
                self.last_seen = time.time()
                self.logger = HistoryLogger(name)
                print(f"✅ FACE LOCKED: {name}")

    def update_tracking(self, bbox):
        if self.locked:
            self.locked_bbox = bbox
            self.last_seen = time.time()

            actions = self.action_detector.detect(bbox)
            for act in actions:
                print("ACTION:", act)
                if self.logger:
                    self.logger.log(act)

    def check_unlock(self):
        if self.locked and (time.time() - self.last_seen > self.timeout):
            print("❌ FACE UNLOCKED")
            self.locked = False
            self.locked_bbox = None
            self.logger = None

    def is_locked(self):
        return self.locked
