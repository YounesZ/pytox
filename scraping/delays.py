import time
from time import sleep
from numpy import random


RANDOM_DELAYS_LIMITS = [4, 10]


def random_delay(limits = RANDOM_DELAYS_LIMITS):
    # Generate random integer
    rint = random.choice(limits[1]-limits[0])

    # Sleep on it
    sleep(rint + limits[0])




if __name__ == '__main__':
    start = time.time()
    random_delay()
    finish = time.time()
    print(f'Took {finish-start} seconds to complete')