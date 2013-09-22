from neopapi.main import User, Inventory
from neopapi.explore.world.island import TrainingSchool
import time
import datetime
from neopapi.shops import ShopWizard
from neopapi.explore.world.island.Exceptions import StatTooHighException

while True:
    if not User.is_logged_in("de_meester_1989"):
        print("User is not logged in. Logging in")
        User.login("de_meester_1989", "Ka8st9je")
    
    pet = "Icicle202"
    
    status = TrainingSchool.get_course_status(pet)
    if status == TrainingSchool.IDLE:
        print('Status is Idle, starting course')
        try:
            TrainingSchool.start_course(pet, TrainingSchool.STRENGTH)
            print('Started training Strength')
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
            cheapest = None
            for i in range(3):
                results = ShopWizard.search(stone)
                if cheapest is None or cheapest.price > results[0].price:
                    cheapest = results[0]
            cheapest.buy()
            print('Bought ' + stone + '@' + str(cheapest.price) + 'np')
        TrainingSchool.pay_course(pet)
        print('Course paid')
    elif status == TrainingSchool.TRAINING:
        print('Status is Training, waiting for course to finish')
        time_remaining = TrainingSchool.get_course_time_remaining(pet)
        print('Sleeping for ' + str(time_remaining) + ' until ' + (datetime.datetime.now() + time_remaining).strftime('%x %X'))
        time.sleep(time_remaining.total_seconds())
        print('Resuming')
    elif status == TrainingSchool.FINISHED:
        print('Status is Finished, finishing course')
        TrainingSchool.finish_course(pet)
        print('Finished course')
        