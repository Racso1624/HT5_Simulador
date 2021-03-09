from Event import Event
from Queue import Queue
import simpy
import random

def simulation(env, events):
    for i in events:
        memory = random.randint(1,10)
        instructions = random.randint(1,10)
        event = Event(memory, instructions)

env = simpy.Environment()
ram = simpy.Container(env, init = 100, capacity = 100)