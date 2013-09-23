import Trainer
import time
import Banker
from neopapi.core import Time
from datetime import timedelta

tasks = []

plugins = [Trainer, Banker]

for plugin in plugins:
        time.sleep(1)
        tasks.append((Time.NST_time(), plugin))

while True:
    ordered_tasks = sorted(tasks, key=lambda x: x[0], reverse=True)
    first_task = ordered_tasks.pop()
    print('Plugin ' + first_task[1].__name__ + ' is first on the list')
    if first_task[0] > Time.NST_time():
        print('Waiting until %s NST (localtime: %s) to start %s' % (first_task[0].strftime('%x %X'), (first_task[0] + timedelta(hours=10)).strftime('%X'), first_task[1].__name__))
        time.sleep((first_task[0] - Time.NST_time()).total_seconds())
    print('Running ' + first_task[1].__name__)
    next_task_time = first_task[1].run()
    ordered_tasks.append((next_task_time, first_task[1]))
    tasks = ordered_tasks
