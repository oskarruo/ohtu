import unittest
from statistics_service import StatisticsService, SortBy
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),
            Player("Lemieux", "PIT", 45, 54),
            Player("Kurri",   "EDM", 37, 53),
            Player("Yzerman", "DET", 42, 56),
            Player("Gretzky", "EDM", 35, 89)
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )
    
    def test_search(self):
        self.assertEqual(str(self.stats.search("Semenko")), "Semenko EDM 4 + 12 = 16")

    def test_wrong_player_search(self):
        self.assertEqual(self.stats.search("Bissonnette"), None)
    
    def test_team(self):
        self.assertEqual(str(self.stats.team("PIT")[0]), "Lemieux PIT 45 + 54 = 99")
    
    def test_top(self):
        self.assertEqual(str(self.stats.top(4)[2]), "Yzerman DET 42 + 56 = 98")
    
    def test_top_goals(self):
        self.assertEqual(str(self.stats.top(4, SortBy.GOALS)[2]), "Kurri EDM 37 + 53 = 90")
    
    def test_top_assists(self):
        self.assertEqual(str(self.stats.top(4, SortBy.ASSISTS)[0]), "Gretzky EDM 35 + 89 = 124")