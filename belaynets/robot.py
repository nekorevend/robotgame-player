import rg
import random

class Robot:
    def act(self, game):
        # Goal: Leave the spawn point and/or attack any adjacent enemy.
        
        # if there are adjacent enemies, attack one.
        for loc, bot in game.get('robots').items():
            if bot.get('player_id') != self.player_id:
                # enemy bot
                if rg.dist(loc, self.location) <= 1:
                    # bot is adjacent
                    return ['attack', loc]
            
        if 'spawn' in rg.loc_types(self.location):
            # get possible move locations
            move_locs = rg.locs_around(self.location, filter_out=['obstacle', 'invalid'])
            
            move = rg.toward(self.location, rg.CENTER_POINT)
            if ('obstacle' in rg.loc_types(move) or 'invalid' in rg.loc_types(move)) and len(move_locs) > 0:
                move = move_locs[random.randint(0, len(move_locs)-1)]
            return ['move', move]
            
        return ['guard']
