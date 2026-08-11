# README (Perfect Crime)

## Motivation and Metric

I was most interested in the Reputation simulations because of the potential for multiple sources
of chaos at once - dropped messages and malicious agents. I've heard that sometimes when training
in machine learning or computer vision it's actually beneficial to drop some of the training data,
such as randomly hiding some pixels from the AI as it learns to solve some computer vision task. 
Motivated by this, I started thinking about what the effect would be of changing the message_drop
field in the reputation.yaml file. Some of the metrics used to evaluate the reputation simulation 
seemed more natural to me than others, but I was interested in the worst case scenario: a malicious
agent successfully cheats against an honest agent (without the cheat message that the malicious agent
sends being dropped) but the malicious agent is not reported because the honest agent's report is
dropped. I call this a *perfect crime*. Any time a malicious agent sends a cheat message to an honest
agent, I call this a cheating *attempt*. To me, the metric that best describes the success of the
simulation is *perfect crime rate* = (number of *perfect crimes*)/(number of *attempts*). I 
abbreviate the metric by PCR and call the message drop probability P. 

## Reproduce the analysis 

```bash
for m in $(seq 0 0.05 0.95); do
  python3 summarize_attempts.py "$m"
done
```

```bash
python3 summarize_overall.py
```

```bash
python3 plot_perfect_crimes.py
```

Note that reproducing the creation of the 8000 .yaml files and running these simulations is very 
straightforward, but it takes around 40 minutes, so it is easiest to just use the files included in the 
pull request. 

## Scenario files

For each value of P in [0, 0.05, 0.1, ... , 0.9, 0.95] and each value of n in [1, 2, ... , 400], 
there is a file drop_P_seed_n_reputation.yaml in the scenarios folder. This only differs from the 
original reputation.yaml file in that it sets the random seed to n and sets the message_drop field to
P. The trace output from running reputation with this .yaml file is stored at 
traces/drop_P_seed_n_reputation.jsonl. 

## count_crimes.py

This file takes in a filename referring to a single trace, such as "drop_0.2_seed_137_reputation.jsonl"
and prints the number of *attempts* and the number of *perfect crimes" in that run of the simulation.

## summarize_attempts.py

This file takes in a value of P and looks at each file drop_P_seed_1_reputation.jsonl through 
drop_P_seed_400_reputation.jsonl, creating a 400 line file where each line is of the form A, PC.
On line n, A represents the number of attempts and PC represents the number of perfect crimes in the
simulation whose trace is drop_P_seed_n_reputation.jsonl. 

## summarize_overall.py

This file looks at the output of summarize_attempts.py applied to each value of P and creates a 20 line
file, overall_attempts.txt whose lines have the form P, TA, TPC, f where P is the probability of a 
message drop, TA is the total number of attempts in all 400 simulations with this P, TPC is the total 
number of perfect crimes, and f = TPC/TA is the perfect crime rate.

## plot_perfect_crimes.py

This file uses the output of summarize_overall.py to plot points (P, PCR) where P is the probability and
PCR is the perfect crime rate for that probability. On the same graph, this file plots the function 
PCR = P (1 - P). 

## Perfect_Crime_Rates.png

This is the output of plot_perfect_crimes.py. 