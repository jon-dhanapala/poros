# POROS
Simulation of a Costco Gas Station

## Assumptions:
  1. Simulation time is recorded in hours
  2. The simulation will strictly end at time `SIM_DURATION`. This means that if there are any vehicles that have arrived in the system, waiting or in service will terminate.
  3. The maximum length of any individual queue can be infinity
  4. If the minimum queue length of all queues has 10 or more cars waiting to be serviced, arrivals will only join a queue with a probability of 0.3
  5. Service times are inclusive of all time counted from the moment a vehicle stops in front of a pump to when it drives off from the pump after it has been serviced. This included filling the vehicle with gas, paying, etc
  6. Price of Costco membership is not needed to be accounted for in cost analysis

## Setting up:
Below are some important parameters to know:

```
NUM_REPLICATIONS=6
NUM_DISTRIBUTIONS=3
SIM_DURATION=0.5 # hours
NUM_GAS_PUMPS=2 # number of gas pumps per lane
NUM_GAS_LANES=8 # number of gas lanes per gas station
PROB_CARS_WAIT=0.3 # probability that a car will wait in queue if the minimum queue length is greater or equal than 12

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

```

## Running the Simulation

1. In your terminal run `python simulation.py`
2. Your results will be found in the csv files.
