import rg
import random

class Robot:
    def act(self, game):
        # Goal: Leave the spawn point and/or attack any adjacent enemy.
        
        print "bot at", self.location
        
        # if there are enemies around, attack them
        for loc, bot in game.get('robots').items():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    print "attack", loc
                    return ['attack', loc]
            
        if 'spawn' in rg.loc_types(self.location):
            # get possible move locations
            move_locs = rg.locs_around(self.location, filter_out=('invalid', 'obstacle'))
            
            for loc, bot in game.get('robots').items():
                if loc in move_locs:
                    print "removing", loc, "from", move_locs
                    move_locs.remove(loc)
            
            move = rg.toward(self.location, rg.CENTER_POINT)
            print "default", move, "out of", move_locs
            if move not in move_locs:
                move = move_locs[random.randint(0, len(move_locs)-1)]
            print "move", move
            return ['move', move]
            
        return ['guard']
