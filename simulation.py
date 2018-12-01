import simpy
import numpy as np
import random
import pandas as pd

# initialize sim parameters
# np.random.seed(0)

SIM_DURATION=20*60 # minutes
IA_MEAN=2.18 # interarrival time mean
IA_SIGMA=0.13 # interarrival time sigma
SERVICE_TIME_BETA=211.9 # service time beta
NUM_GAS_PUMPS = 2

env = simpy.Environment()

# initializing result dataframe
d = {
'Vehicle': [],
'Interarrival Time': [],
'Min Queue Length': [],
'Max Queue Length': [],
'Service Duration': [],
'Wait Time': [],
'Sojurn Time': [],
}

env.df = pd.DataFrame(data=d)

# MQ: array of length 8 with 2 resources/queue
lanes = []
for i in range(8):
    lane = simpy.Resource(env, capacity=NUM_GAS_PUMPS)
    lanes.append(lane)
print lanes

""" MAIN FUNCTIONS """

# start simulation (generate arrival time)
def start_simulation(env):
    i = 0
    while True:
        result = {}
        i += 1
        arrival_time = __generate_interarrival_time()
        result['Vehicle'] = round(i, 1)
        result['Interarrival Time'] = arrival_time
        name = 'Vehicle %s' % i

        yield env.timeout(arrival_time)
        env.process(run_simulation(env, name, result))

# run simulation
def run_simulation(env, name, result):
    env.df = env.df
    arrival_time = env.now
    print ("%s arriving at %s" %(name, arrival_time))
    lane = __get_min_lane(lanes, result)

    car_waits = __should_car_wait(lane) # check if car should wait
    if (car_waits):
        wait_time_start = env.now

        # queue up for a gas pump
        with lane.request() as req:
            yield req
            wait_time_end = env.now
            wait_time = wait_time_end - wait_time_start
            result['Wait Time'] = wait_time

            # start service time
            print('%s starting service at %s' % (name, wait_time_end))
            service_time = __generate_service_time()
            result['Service Duration'] = service_time
            result['Sojurn Time'] = wait_time + service_time
            yield env.timeout(service_time)

            # end service time
            print('%s end service at %s' % (name, env.now))
            lane.release(req)
            __collect_stats(lane, result)

""" HELPEER FUNCTIONS """

# generate inter arrival time
def __generate_interarrival_time():
    return round(np.random.lognormal(mean=IA_MEAN, sigma=IA_SIGMA), 3)

# generate inter arrival time
def __generate_service_time():
    return round(np.random.exponential(211.9), 3)

# generate inter arrival time
def __generate_random_variable():
    return round(random.random(), 3)

# get lane with the minimum queue length
def __get_min_lane(lanes, result):
    min_queue = min(lanes, key=lambda x: len(x.queue))
    max_queue = max(lanes, key=lambda x: len(x.queue))
    result['Min Queue Length'] = len(min_queue.queue)
    result['Max Queue Length'] = len(max_queue.queue)
    return min_queue

# get stats at current time
def __collect_stats(resource, result):
    print("===========")
    print('Current Time: %s' % env.now)
    print ("QUEUES:")
    for index, lane in enumerate(lanes):
        print("lane %s queue size: %s" % (index, len(lane.queue)))
    print("===========")
    env.df = env.df.append(result, ignore_index=True)

# calculating the probabilty based on length of queue >= 12
def __should_car_wait(lane):
    if len(lane.queue) >= 12:
        x = __generate_random_variable()
        return True if (x < 0.3) else False
    else:
        return True

def main():
    env.process(start_simulation(env))
    env.run(until=SIM_DURATION)
    result = env.df.sort_values(by=['Vehicle'])
    result.to_csv('results.csv', index=False)

if __name__ == '__main__':
    main()
