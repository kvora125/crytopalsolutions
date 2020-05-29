seed = None

def get_rand_int():
    # Use Python's PRNG to sleep for a random time period
    sleep(randint(40, 1000))
    # For testing purposes
    global seed
    seed = int(time())
    rand_int = MT19937(seed).extract_number()
    sleep(randint(40, 1000))
    return rand_int

def crack_seed():
    rand_int = get_rand_int()
    current_time = int(time())
    for seed in range(current_time, current_time - 2500, -1):
        if MT19937(seed).extract_number() == rand_int:
            return seed
    raise Exception('Could not crack MT19937 seed.')

print crack_seed()
# 1499970065
