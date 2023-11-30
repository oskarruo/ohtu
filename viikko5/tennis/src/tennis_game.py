class TennisGame:
    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score_player_1 = 0
        self.m_score_player_2 = 0
        self.score = "Love-All"

    def won_point(self, player_name):
        match player_name:
            case self.player1_name:
                self.m_score_player_1 += 1
                self.update_score()
            case self.player2_name:
                self.m_score_player_2 += 1
                self.update_score()
            case _:
                raise ValueError("player doesn't exist")

    def update_score(self):
        if self.m_score_player_1 == self.m_score_player_2:
            if self.m_score_player_1 == 0:
                self.score = "Love-All"
            elif self.m_score_player_1 == 1:
                self.score = "Fifteen-All"
            elif self.m_score_player_1 == 2:
                self.score = "Thirty-All"
            else:
                self.score = "Deuce"

        elif self.m_score_player_1 >= 4 or self.m_score_player_2 >= 4:
            difference_for_player_1 = self.m_score_player_1 - self. m_score_player_2

            if difference_for_player_1 == 1:
                self.score = "Advantage player1"
            elif difference_for_player_1 == -1:
                self.score = "Advantage player2"
            elif difference_for_player_1 >= 2:
                self.score = "Win for player1"
            else:
                self.score = "Win for player2"

        else:
            match self.m_score_player_1:
                case 0:
                    self.score = "Love-"
                case 1:
                    self.score = "Fifteen-"
                case 2:
                    self.score = "Thirty-"
                case 3:
                    self.score = "Forty-"
            match self.m_score_player_2:
                case 0:
                    self.score = self.score + "Love"
                case 1:
                    self.score = self.score + "Fifteen"
                case 2:
                    self.score = self.score + "Thirty"
                case 3:
                    self.score = self.score + "Forty"
            

    def get_score(self):
        return self.score
