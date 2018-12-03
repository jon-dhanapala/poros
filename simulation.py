import simpy
import numpy as np
import random
import pandas as pd

""" INITIALIZE SIM PARAMETERS """

# np.random.seed(0)
NUM_REPLICATIONS=5
NUM_RANKS=3
SIM_DURATION=0.5 # hours
NUM_GAS_PUMPS=2
NUM_GAS_LANES=8
PROB_CARS_WAIT=0.3

"""
Ranks of Distribution:

    rank0: ia: lognormal
    rank1: ia: gamma
    rank2: ia: exponential

    rank0: st: beta
    rank1: st: normal
    rank2: st: exponential
"""

# == DISTRIBUTION: NORMAL DISTRIBUTION === #

NORMAL_ST_MEAN=0.05442593 # mean
NOMRAL_ST_SD=0.02115479 # standard deviation

# === DISTRIBUTION: EXPONENTIAL DISTRIBUTION === #

EX_IA_BETA=0.00363975 # inter-arrival time beta
EX_ST_BETA=0.05442593  # inter-arrival time beta

# === DISTRIBUTION: LOGNORMAL DISTRIBUTION === #

LN_IA_MEAN=-6.007 # inter-arrival time mean
LN_IA_SIGMA=0.87 # inter-arrival time sigma

# === DISTRIBUTION: BETA DISTRIBUTION === #

BETA_ST_ALPHA=6.20435463 # service time alpha
BETA_ST_BETA=107.791954 # service time beta

# === DISTRIBUTION: GAMMA DISTRIBUTION === #
GAMMA_IA_1=0.9695866 # gamma param 1
GAMMA_IA_2=0.0037539 # gamma param 2

# == initializing result object for dataframe ==

d = {
'Event Type': [],
'Num Cars in the System': [],
'Vehicle': [],
'Clock Time': [],
'Arrival Clock Time': [],
'Interarrival Time': [],
'Service Duration': [],
'Wait Time': [],
'Sojurn Time': [],
'Queue 0 Size': [],
'Queue 1 Size': [],
'Queue 2 Size': [],
'Queue 3 Size': [],
'Queue 4 Size': [],
'Queue 5 Size': [],
'Queue 6 Size': [],
'Queue 7 Size': [],
}

""" MAIN FUNCTIONS """

# start simulation (generate arrival time)
def start_simulation(env, lanes, rank):
    vehicle_num = 0
    while True:
        result = {}
        vehicle_num+= 1
        inter_arrival_time = __generate_interarrival_time(rank) if vehicle_num > 25 else 0

        result['Vehicle'] = round(vehicle_num, 1)
        result['Interarrival Time'] = inter_arrival_time
        name = 'Vehicle %s' % vehicle_num

        yield env.timeout(inter_arrival_time)
        env.process(run_simulation(env, name, result, lanes, rank))

# run simulation
def run_simulation(env, name, result, lanes, rank):
    env.df = env.df
    env.num_arrivals += 1
    arrival_time = env.now
    print ("%s starting at %s" %(name, arrival_time))
    result['Arrival Clock Time'] = arrival_time
    lane_index = __get_min_index(lanes, result)
    lane = lanes[lane_index]

    car_waits = __should_car_wait(lane) # check if car should wait
    if (car_waits):
        wait_time_start = env.now

        # queue up for a gas pump
        print("gas pumps in use: %s" % lane.count)
        with lane.request() as req:
            __collect_num_system(env, arrival_time, lanes, "Arrival") # get num in the system
            yield req
            wait_time_end = env.now
            wait_time = wait_time_end - wait_time_start
            result['Wait Time'] = wait_time

            # === start service time ===
            print('%s starting service at %s' % (name, wait_time_end))
            service_time = __generate_service_time(rank) # generate servicetime
            print ("service time %s" % service_time)
            result['Service Duration'] = service_time
            result['Sojurn Time'] = wait_time + service_time
            yield env.timeout(service_time)

            # === end service time ===
            print('%s end service at %s' % (name, env.now))
            lane.release(req)
            env.num_departures += 1
            print("%s users: %s" % (name, lane.count))
            __collect_stats(env, result)
            __collect_num_system(env, env.now, lanes, 'Departure') # collect num in the system in departure

""" HELPEER FUNCTIONS """

# generate inter arrival time
def __generate_interarrival_time(rank):
    if rank == 0:
        return round(np.random.lognormal(mean=(LN_IA_MEAN), sigma=(LN_IA_SIGMA)), 3) # rank 0
    elif rank == 1:
        return (round(np.random.gamma(GAMMA_IA_1, GAMMA_IA_2), 3)) # rank 1
    else:
        return round(np.random.exponential(EX_IA_BETA), 3) # rank 2

# generate service time
def __generate_service_time(rank):
    if rank == 0:
        return round(np.random.beta(BETA_ST_ALPHA, BETA_ST_BETA), 3) # rank 0
    elif rank == 1:
        return abs(round(np.random.normal(loc=NORMAL_ST_MEAN, scale=NOMRAL_ST_SD), 3)) # rank 1
    else:
        return round(np.random.exponential(EX_ST_BETA), 3) # rank 2

# generate random variable time
def __generate_random_variable():
    return round(random.random(), 3)

# get lane with the minimum queue length
def __get_min_index(lanes, result):
    print ("QUEUES:")
    for index, lane in enumerate(lanes):
        print("lane %s queue size: %s, queue count: %s" % (index, len(lane.queue), lane.count))
    print("===========")

    values = []
    for l in lanes:
        values.append(len(l.queue) + l.count) # length of queue + num vehicles serving
    print (values)
    return values.index(min(values))

# get stats at current time
def __collect_stats(env, result):
    env.df = env.df.append(result, ignore_index=True)

# get num of vehicles in system at arrival or departure
def __collect_num_system(env, current_time, lanes, type):
    print("===========")
    print('Current Time: %s' % current_time)
    obj = { 'Event Type': type, 'Num Vehicles in System': env.num_arrivals - env.num_departures, 'Clock Time': current_time }
    for index, lane in enumerate(lanes):
        obj[('Queue %s Size' % index)] = (len(lane.queue) + lane.count)
    env.df = env.df.append(obj, ignore_index=True)

# calculating the probabilty based on length of queue >= 12
def __should_car_wait(lane):
    if len(lane.queue) >= 12:
        x = __generate_random_variable()
        return True if (x < PROB_CARS_WAIT) else False
    else:
        return True

# return name of inter-arrival distribution that's currently being simulated
def __get_ia_distribution_name(rank):
    if rank == 0:
        return "Lognormal Distribution"
    elif rank == 1:
        return "Gamma Distribution"
    else:
        return "Exponential Distribution"

# return name of service-time distribution that's currently being simulated
def __get__st_distribution_name(rank):
    if rank == 0:
        return "Beta Distribution"
    elif rank == 1:
        return "Normal Distribution"
    else:
        return "Exponential Distribution"

def main():
    for rank in range(NUM_RANKS):
        for rep in range(NUM_REPLICATIONS):
            env = simpy.Environment()
            columns=['Vehicle', 'Arrival Clock Time', 'Interarrival Time', 'Service Duration', 'Wait Time', 'Sojurn Time', 'Event Type', 'Clock Time', 'Num Vehicles in System', ' ', 'Queue 0 Size','Queue 1 Size','Queue 2 Size', 'Queue 3 Size', 'Queue 4 Size', 'Queue 5 Size', 'Queue 6 Size', 'Queue 7 Size']
            env.df = pd.DataFrame(data=d, columns=columns)
            env.num_arrivals = 0
            env.num_departures = 0

            # MQ: array of length 8 with 2 resources/queue
            lanes = []
            for i in range(NUM_GAS_LANES):
                lane = simpy.Resource(env, capacity=NUM_GAS_PUMPS)
                lanes.append(lane)
            print lanes

            env.process(start_simulation(env, lanes, rank))
            env.run(until=SIM_DURATION)

            csv_name = ('results_rank_%s_rep_%s.csv' % (rank, rep))
            print ("total num vechicles arrived: %s" % (env.num_arrivals))
            ia_distribution_name = __get_ia_distribution_name(rank)
            st_distribution_name = __get__st_distribution_name(rank)
            env.df = env.df.append({ 'Total Arriving Vehicles': env.num_arrivals, 'Total Simulation Time': SIM_DURATION, 'Inter-arrival Distribution Type': ia_distribution_name, 'Service Time Distribution Type': st_distribution_name, 'Rank': rank, 'Rep #': rep }, ignore_index=True)
            result = env.df.sort_values(by=['Vehicle'])
            result.to_csv(csv_name, index=False)

if __name__ == '__main__':
    main()
