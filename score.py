class Score:
    def __init__(self) -> None:
        self.score = 0

    def update_score(self):
        self.score += 1

    def get_score(self):
        return self.score
    
    def reset_score(self):
        self.score = 0
