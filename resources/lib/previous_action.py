from typing import Dict
import datetime

class PreviousActions:
    def __init__(self) -> None:
        self.markedAsSeenHistory: Dict[int, datetime.datetime] = {}

    def canMarkAsSeen(self, id: int, progress: float) -> bool:
        if progress < 0.80:
            return False

        d = self.markedAsSeenHistory.get(id)

        if d and (datetime.datetime.now() - d).seconds < 12 * 60 * 60:
            return False

        self.markedAsSeenHistory[id] = datetime.datetime.now()

        return True
