from neopapi.main import Inventory
from neopapi.explore.world.island import TrainingSchool
from neopapi.shops import ShopWizard
from neopapi.explore.world.island.Exceptions import StatTooHighException
from neopapi.core import Time
from neopapi.shops.Exceptions import ItemOutOfStockException

def run():
    while True:
        pet = "Icicle202"
        
        status = TrainingSchool.get_course_status(pet)
        if status == TrainingSchool.IDLE:
            print('Status is Idle, starting course')
            stats = StatOptimizer(TrainingSchool.get_status(pet))
            next_stat = stats.get_next_stat_to_train()
            try:
                TrainingSchool.start_course(pet, next_stat)
                print('Started training ' + next_stat)
            except StatTooHighException:
                TrainingSchool.start_course(pet, TrainingSchool.LEVEL)
                print('Level too low, started training Level')
        elif status == TrainingSchool.AWAITING_PAYMENT:
            print('Status is Awaiting Payment, paying course')
            stones = TrainingSchool.get_course_cost(pet)
            print('Need ' + ', '.join(stones))
            stones_in_inventory = Inventory.contains(stones)
            for stone, stone_in_inventory in zip(stones, stones_in_inventory):
                if stone_in_inventory:
                    print(stone + ' already present in Inventory')
                    continue
                print('Looking for ' + stone)
                while True:
                    cheapest = None
                    for _ in range(3):
                        results = ShopWizard.search(stone)
                        if cheapest is None or cheapest.price > results[0].price:
                            cheapest = results[0]
                    try:
                        cheapest.buy()
                        break
                    except ItemOutOfStockException:
                        pass
                print('Bought ' + stone + '@' + str(cheapest.price) + 'np')
            TrainingSchool.pay_course(pet)
            print('Course paid')
        elif status == TrainingSchool.TRAINING:
            print('Status is Training, waiting for course to finish')
            time_remaining = TrainingSchool.get_course_time_remaining(pet)
            print('Training is done in %dh%dm%ds at %s' % ((time_remaining.seconds//3600), (time_remaining.seconds//60)%60, time_remaining.seconds%3600, (Time.NST_time() + time_remaining).strftime('%x %X')))
            return (Time.NST_time() + time_remaining)
        elif status == TrainingSchool.FINISHED:
            print('Status is Finished, finishing course')
            TrainingSchool.finish_course(pet)
            print('Finished course')

class StatOptimizer:
    
    level_brackets = [20,    40,     80,     100,    120,    150,    200,    250]
    
    bracket_margins = [2,     2,      3,      4,      4,      5,      6,      20]
    
    def __init__(self, pet_info):
        self.level = pet_info['level']
        self.defence = pet_info['defence']
        self.strength = pet_info['strength']
        self.movement = pet_info['movement']
        self.hp = pet_info['hp']
        
    def get_next_stat_to_train(self):
        # This is the maximum level in the current bracket
        cur_lvl = self.level
        max_lvl = self._get_max_bracket_level(self.level)
        margin = self._get_current_bracket_margin(self.level)
        
        if cur_lvl > 80:
            return TrainingSchool.LEVEL
        
        if cur_lvl < (max_lvl - 2*margin):
            return TrainingSchool.LEVEL
        
        elif cur_lvl < (max_lvl - margin):
            if self.defence > 2*cur_lvl or self.strength > 2*cur_lvl or \
               self.movement > 2*cur_lvl or self.hp > 2*cur_lvl:
                # If any stat is above its limits, level has to be trained.
                return TrainingSchool.LEVEL
            elif self.defence < 2*cur_lvl - margin:
                return TrainingSchool.DEFENCE
            elif self.strength < 2*cur_lvl - margin:
                return TrainingSchool.STRENGTH
            elif self.hp < 2*cur_lvl - margin:
                return TrainingSchool.HP
            return TrainingSchool.LEVEL
        
        else:
            next_max_lvl = self._get_max_bracket_level(max_lvl + 1)
            next_margin = self._get_current_bracket_margin(next_max_lvl)
            if self.defence > 2*cur_lvl or self.strength > 2*cur_lvl or \
               self.movement > 2*cur_lvl or self.hp > 3*cur_lvl:
                # If any stat is above its limits, level has to be trained.
                return TrainingSchool.LEVEL
            elif self.hp > 2*(next_max_lvl - 2*next_margin) - margin:
                if max_lvl <= 80:
                    return TrainingSchool.LEVEL
                return TrainingSchool.HP
            elif self.defence < 2*max_lvl - 2*margin:
                return TrainingSchool.DEFENCE
            elif self.strength < 2*max_lvl - 2*margin:
                return TrainingSchool.STRENGTH
            else:
                return TrainingSchool.HP
        
    def _get_max_bracket_level(self, level):
        brackets = self.level_brackets
        for bracket in brackets:
            if bracket >= level:
                return bracket
        return self.level_brackets[self.school][-1]*10
    
    def _get_current_bracket_margin(self, level):
        margins = self.bracket_margins
        bracket_max = self._get_max_bracket_level(level)
        if not bracket_max in self.level_brackets:
            return self.bracket_margins[-1]
        index = self.level_brackets.index(self._get_max_bracket_level(level))
        return margins[index]
