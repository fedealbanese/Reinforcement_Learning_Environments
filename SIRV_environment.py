import numpy as np
import gym
from gym import spaces
from gym.utils import seeding

class SIRV(gym.Env):
  """
  An open source epidemiological reinforcement learning environment compatible with OpenAI Gym's toolkit.    
  """
    def __init__(self, k, p_tot, p_0, r, beta, nu, ci, cv, max_t, delta_i = 100, delta_pi = 100):
        self.k = k #el grado del usuario
        self.p_tot = p_tot #cantidad de usuarios total de la poblcion
        self.p_0 = p_0 #proporcion de infectados a tiempo 0
        self.r = r #tasa de ifectividad
        self.beta = beta #tasa de recuperacion
        self.nu = nu #valor maximo de la tasa de vacunacion pi.
        self.ci = ci #costo de infeccion
        self.cv = cv #costo de vacunacion
        self.max_t = max_t #cantidad de iteraciones maxima
        
        self.delta_i = delta_i #cantidad de particiones que hago entre 0 y p_tot. Son los valores que puede tomar la cantida total de infectados p_i.
        self.delta_pi = delta_pi #cantidad de particiones que hago entre 0 y nu. Son los valores que puede tomar la tasa de vacunacion pi.
        
        self.action_space = spaces.Discrete(self.delta_pi)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(self.delta_i), #cantidad de usuarios infectados
            spaces.Discrete(4))) #mis estados que pueden ser R, S, I, V.

        self.seed()
        # Empieza el juego
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action)
        
        self.pi = action * self.nu / self.delta_pi
        
        #actualizo mi estado
        prob_me_quedo_en_S = np.exp(-(self.p_i * self.r + self.pi))
        prob_me_voy_a_I = 0 if (self.p_i * self.r + self.pi)==0 else (self.p_i * self.r) / (self.p_i * self.r + self.pi)
        #print("probas: ",prob_me_quedo_en_S ,prob_me_voy_a_I)
        if self.np_random.rand() < prob_me_quedo_en_S: #me quedo en S
            done = False
            self.reward += - self.cv*self.pi / self.nu
        else:
            if self.np_random.rand() < prob_me_voy_a_I: #me voy a I
                done = True
                self.reward += - self.ci * np.ceil(self.np_random.exponential(self.beta))
                self.estado = "R" #es R y no I porque ya estoy teniendo en cuenta en el costo, la infeccion
            else: #me voy a V
                done = True
                self.reward += - self.cv
                self.estado = "V"
        
        #actualizo la sociedad: fully connected. tener en cuenta que p_i solo puede tomar valores discretos
        # falta completar esto con lo de matt
        
        #Corto el experimento despues de max_t dias.
        self.t +=1
        if self.t > self.max_t:
            #print("la cago")
            done = True
        return self.get_obs(), self.reward, done, {}

    def get_obs(self):
        return (self.p_i, self.estado)
    
    def reset(self):
        self.t = 0 #el dia en que se empieza
        self.estado = "S" #empieza el usuario como susceptible. Puede tomar los valores: S, I, R o V.
        self.p_i = self.p_0 #proporcion de infectados a tiempo t
        self.pi = 0 #tasa de vacunacion
        self.reward = 0
        
        return self.get_obs()
