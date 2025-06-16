## System dynamics component ##

# Load relevant packages
import numpy as np
from scipy.integrate import odeint
import math

class SystemDynamics:

	def __init__(self, Q, decay, upgrade = False, growth = None, upgrade_date = None, 
				 upgrade_length = None, maintenance = False):

		self.Q = [Q] # quality of park
		self.growth = growth # rate of improvement by policy
		self.decay = decay # degradation rate
		self.upgrade = upgrade # policy in place? (bool)
		self.date = upgrade_date # start date of policy (in days)
		self.upgrade_length = upgrade_length # length of policy update (in days)
		self.maintenance = maintenance # policy in place? (bool)

	def differential_equation(self, Q, time_domain, N, t):

		if self.maintenance:

			if self.upgrade: 

				if self.date <= t < self.date + self.upgrade_length:
					dQ = self.growth * Q * (1 - Q/100) - \
					(self.decay/2) * N**(1/4) * Q

				else:
					dQ = - (self.decay/2) * N**(1/4) * Q

			else:
				dQ = - (self.decay/2) * N**(1/4) * Q

		else:
			if self.upgrade:
			
				if self.date <= t < self.date + self.upgrade_length:
					dQ = self.growth * Q * (1 - Q/100) - \
					self.decay * N**(1/4) * Q

				else:
					dQ = - self.decay * N**(1/4) * Q

			else:
				dQ = - self.decay * N**(1/4) * Q

		return dQ

	def solve(self, t, N):

		Q = self.Q[-1]
		result = odeint(self.differential_equation, Q, np.linspace(t-1,t,1000), args = (N,t))
		self.Q.append(result[-1][0])