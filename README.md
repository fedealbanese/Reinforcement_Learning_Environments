# Reinforcement Learning Environments: SIRV

An open source epidemiological reinforcement learning environment compatible with OpenAI Gym's toolkit.

The SIRV model is a simple mathematical model of epidemics and it can be implemented as a Markov Chain process where each person can be in different states:
- S (Susceptible)
- I (Infected)
- R (Recovered)
- V (Vaccinated)

The agent learns to modifies its own vaccination rate in order to reduce the cost. On the other hand, the user provides to the society a time dependent policy as input. 
