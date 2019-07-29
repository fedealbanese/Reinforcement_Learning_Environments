# Reinforcement Learning Environments: SIRV

An open source epidemiological reinforcement learning environment compatible with OpenAI Gym's toolkit.

The SIRV model is a simple mathematical model of epidemics and it can be implemented as a Markov Chain process where each person can be in different states:
- S (Susceptible)
- I (Infected)
- R (Recovered)
- V (Vaccinated)

Two environment versions are uploaded to this repository where an agent can decide its vaccination rate depending on the percentage of infected persons. In the first version, the society vaccination rate is constant whereas the agent can modifies its own rate. On the other hand, the second version allows the user to provide a society time dependent policy.
