# POROS - SIMULATION OF A COSTCO GAS STATION

## Assumptions:
  1. Simulation time is recorded in seconds
  2. The simulation will strictly end at time `SIM_DURATION`. This means that if there are any vehicles that have arrived in the system, waiting or in service will terminate.
  3. The maximum length of any individual queue can be infinity
  4. If the minimum queue length of all queues has 10 or more cars waiting to be serviced, arrivals will only join a queue with a probability of 0.3
  5. Service times are inclusive of all time counted from the moment a vehicle stops in front of a pump to when it drives off from the pump after it has been serviced. This included filling the vehicle with gas, paying, etc
  6. Price of Costco membership is not needed to be accounted for in cost analysis

## Setting up:
Below are some important parameters to know:

```
SIM_DURATION #
IA_MEAN=2.18 # mean for inter-arrival time (lognormal distribution)
IA_SIGMA=0.13 # sigma for inter-arrival time (lognormal distribution)
SERVICE_TIME_BETA=211.9 # beta for service time (exponential distribution)
NUM_GAS_PUMPS=2 # number of gas pumps per lane
NUM_GAS_LANES=8 # number of gas lanes per gas station
PROB_CARS_WAIT=0.3 # probability that a car will wait in queue if the minimum queue length is greater or equal than 12
```

## Running the Simulation

1. In your terminal run `python simulation.py`
2. Your results will be found in `results.csv`
