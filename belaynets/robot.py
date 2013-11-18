import rg

class Robot:
    def act(self, game):
        # Goal: Stay away from the enemy. If no direction to escape, then attack.
        
        # get possible move locations
        move_locs = rg.locs_around(self.location, filter_out=['spawn', 'obstacle', 'invalid'])
        adjacent_bots = []
        
        # if there are enemies adjacent, try to escape.
        for loc, bot in game.get('robots').items():
            if bot.get('player_id') != self.player_id:
                # enemy bot
                # if enemy bot is adjacent to a move location, remove that location from possibilities.
                for move in move_locs:
                    if rg.dist(loc, move) <= 2:
                        move_locs.remove(move)
                        
                if rg.dist(loc, self.location) <= 1:
                    # bot is adjacent
                    adjacent_bots.append((loc, bot))
        
        if len(adjacent_bots) > 0:
            # there is an adjacent enemy
            # try to run
            if len(move_locs) > 0:
                return ['move', move_locs[0]]   
            # couldn't run, attack weakest enemy
            lowest_hp = 50
            attack_loc = None
            for loc, bot in adjacent_bots:
                if lowest_hp > bot.get('hp'):
                    lowest_hp = bot.get('hp')
                    attack_loc = loc
            if attack_loc:
                return ['attack', attack_loc]

        # nothing's going on
        if 'spawn' in rg.loc_types(self.location):
            return ['move', rg.toward(self.location, rg.CENTER_POINT)]
        else:
            return ['guard']
            
