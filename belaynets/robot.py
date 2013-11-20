import rg
import random

move_intents = set()
current_turn = None
    
class Robot:
    
    def act(self, game):
        # Goal: Leave the spawn point and/or attack any adjacent enemy.
        
        # avoid bots moving into each other
        global move_intents
        # print "intents", move_intents
        
        global current_turn
        if current_turn is None or current_turn != int(game.get('turn')):
            move_intents = set()
            current_turn = int(game.get('turn'))
        
        # print "bot at", self.location
        
        spawn_move = True if 'spawn' in rg.loc_types(self.location) else False
        
        # if there are enemies around, attack them
        for loc, bot in game.get('robots').items():
            if bot.player_id != self.player_id:
                if rg.dist(loc, self.location) <= 1:
                    # print "attack", loc
                    return ['attack', loc]
            else:
                if 'spawn' in rg.loc_types(loc) and rg.dist(loc, self.location) <= 2:
                    spawn_move = True
        
        if spawn_move:
            # get possible move locations
            move_locs = set(rg.locs_around(self.location, filter_out=('invalid', 'obstacle')))
            move_locs -= move_intents
            
            for loc, bot in game.get('robots').items():
                if loc in move_locs:
                    # print "removing", loc, "from", move_locs
                    move_locs.remove(loc)
            
            move = rg.toward(self.location, rg.CENTER_POINT)
            # print "default", move, "out of", move_locs
            if move not in move_locs and len(move_locs) > 0:
                move = random.choice(list(move_locs))
            # print "move", move
            move_intents.add(move)
            return ['move', move]
            
        return ['guard']
