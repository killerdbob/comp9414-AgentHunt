
class state():
    __instance = None
    def __init__(self):
        self.row=90
        self.col=90
        self.east = 2
        self.north = 1
        self.west = 0
        self.south = 3
        self.dirn = 1
        self.have_axe = 0
        self.have_key = 0
        self.have_raft = 0
        self.game_won = False
        self.game_lost = False
        self.have_treasure = False
        self.num_dynamites_held = 0
        self.simulate_mark=0
        self.refresh_place=False
    @staticmethod
    def get_instance():
        if state.__instance is None:
            state.__instance = state()
        return state.__instance