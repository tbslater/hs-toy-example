## Hybrid Simulation ##

# Import relevant packages
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.stats import bernoulli
import random
import math

# Import relevant files
from agent import Agent
from network import Network
from sd import SystemDynamics

class HybridSimulation:

	def __init__(self, agents):

		self.agents = agents
		self.boys = [] # no. of boys
		self.girls = [] # no. of girls
		self.total = [] # total no.

	def simulation(self, sd, weights, tmax, tmin=1, interv = False):

		t = tmin

		while t <= tmax:

			if len(weights) != 3:
				print('Only 3 weights permitted')
				break
			
			if sum(weights) != 1:
				print('Weights must sum to 1')
				break
			
			# Total no. of children who played yday
			self.boys.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'M'))
			self.girls.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'F'))
			self.total.append(self.boys[-1] + self.girls[-1])

			# Solve SD component at time t
			sd.solve(t, N = self.total[-1])
			qualityt = sd.Q[t] / 100

			# Standardise decisions
			for agent in self.agents:
				agent.decision.append(0)
					
			for agent in self.agents: 

				# Social influence
				influence = sum(friend.decision[-2] for friend in agent.friends)/len(agent.friends)

				# Update preference for play
				agent.pref.append(weights[0]*agent.pref[-1] + weights[1]*qualityt + weights[2]*influence)
				
				# Decision whether or not to play
				agent.decision[-1] = (bernoulli.rvs(agent.pref[-1],1)-1)

				if t >= 6:

					# Update rolling number of visits in a week
					agent.no_weekly_visits()

			t += 1

		if interv == False:
		
			# Total no. of children who played yday
			self.boys.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'M'))
			self.girls.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'F'))
			self.total.append(self.boys[-1] + self.girls[-1])
				

	def intervention(self, sd, weights, tmax, start_time, effect_size, percentage):

		n = len([x for x in self.agents if x.sex == 'F'])
		target_no = round(n * percentage / 100)
		
		# Run simulation before intervention start time
		self.simulation(sd, weights, start_time-1, interv=True)

		# Run for after intervention start time
		t = start_time

		while t <= tmax:

			if t % 7 == 0:
			
				# Total no. of children who played yday
				self.boys.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'M'))
				self.girls.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'F'))
				self.total.append(self.boys[-1] + self.girls[-1])

				# Solve SD component at time t
				sd.solve(t, N = self.total[-1])
				qualityt = sd.Q[t] / 100

				sorted_agents = sorted([x for x in self.agents if x.sex == 'F'], key=lambda x: x.pref)

				# Standardise decisions
				for agent in self.agents:
					agent.decision.append(0)
					
				for agent in self.agents: 

					if agent in sorted_agents[0:target_no]:

						# Social influence
						influence = sum(friend.decision[-8] for friend in agent.friends)/len(agent.friends)

						# Update preference for play
						agent.pref.append(weights[0]*agent.pref[-1] + weights[1]*qualityt + weights[2]*influence)

						current_effect_size = effect_size ** ((t-start_time/7)+1)
						agent.pref[-1] = min(agent.pref[-1] + current_effect_size, 1)

					else:
						# Social influence
						influence = sum(friend.decision[-2] for friend in agent.friends)/len(agent.friends)

						# Update preference for play
						agent.pref.append(weights[0]*agent.pref[-1] + weights[1]*qualityt + weights[2]*influence)

					# Decision whether or not to play
					agent.decision[-1] = (bernoulli.rvs(agent.pref[-1],1)-1)	

					# Update rolling number of visits in a week
					agent.no_weekly_visits()

				t += 1

			
				# Total no. of children who played yday
				self.boys.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'M'))
				self.girls.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'F'))
				self.total.append(self.boys[-1] + self.girls[-1])

				# Solve SD component at time t
				sd.solve(t, N = self.total[-1])
				qualityt = sd.Q[t] / 100

				# Standardise decisions
				for agent in self.agents:
					agent.decision.append(0)
					
				for agent in self.agents: 

					# Update preference for play
					if agent in sorted_agents[0:target_no]:
						# Social influence
						influence = sum(friend.decision[-3] for friend in agent.friends)/len(agent.friends)
						agent.pref.append(weights[0]*agent.pref[-2] + weights[1]*qualityt + weights[2]*influence)
						
					else:
						# Social influence
						influence = sum(friend.decision[-2] for friend in agent.friends)/len(agent.friends)
						agent.pref.append(weights[0]*agent.pref[-1] + weights[1]*qualityt + weights[2]*influence)
				
					# Decision whether or not to play
					agent.decision[-1] = (bernoulli.rvs(agent.pref[-1],1)-1)

					# Update rolling number of visits in a week
					agent.no_weekly_visits()

				t += 1
				
			else: 
				self.simulation(sd, weights, min(t+4,tmax), tmin=t, interv=True)
				t += 5

		# Total no. of children who played yday
		self.boys.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'M'))
		self.girls.append(sum(agent.decision[-1] for agent in self.agents if agent.sex == 'F'))
		self.total.append(self.boys[-1] + self.girls[-1])
				