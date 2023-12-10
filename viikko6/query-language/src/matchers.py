class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value


class All:
    def __init__(self):
        pass

    def test(self, player):
        return True


class Not:
    def __init__(self, condition):
        self._condition = condition

    def test(self, player):
        return not self._condition.test(player)


class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr
    
    def test(self, player):
        player_value = getattr(player, self._attr)
        
        return player_value < self._value


class Or:
    def __init__(self, *conditions):
        self.conditions = []
        for condition in conditions:
            self.conditions.append(condition)

    def test(self, player):
        for condition in self.conditions:
            if condition.test(player):
                return True
        return False


class QueryBuilder:
    def __init__(self):
        self._matcher = All()

    def playsIn(self, team):
        self._matcher = And(self._matcher, PlaysIn(team))
        return self

    def hasAtLeast(self, value, category):
        self._matcher = And(self._matcher, HasAtLeast(value, category))
        return self

    def hasFewerThan(self, value, category):
        self._matcher = And(self._matcher, HasFewerThan(value, category))
        return self

    def notPlaysIn(self, team):
        self._matcher = And(self._matcher, Not(PlaysIn(team)))
        return self

    def build(self):
        return self._matcher
