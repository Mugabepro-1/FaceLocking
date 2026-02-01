class ActionDetector:
    def __init__(self):
        self.prev_x = None

    def detect(self, bbox):
        actions = []
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) // 2

        if self.prev_x is not None:
            if center_x - self.prev_x > 15:
                actions.append("MOVE_RIGHT")
            elif self.prev_x - center_x > 15:
                actions.append("MOVE_LEFT")

        self.prev_x = center_x
        return actions
