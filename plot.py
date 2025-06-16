from agent import Agent
from network import Network
from sd import SystemDynamics
from simulation import HybridSimulation

import numpy as np
import random
import matplotlib.pyplot as plt

class Plot:

	def __init__(self, upgrade = False, maintenance = False, weekly_session = False,
				 no_repeats = 10, seed_start = 0, max_agents = 500, no_friends = 8, 
				 initial_Q = 50, upgrade_rate = 0.3, degradation_rate = 0.001, 
				 policy_date = 365, upgrade_length = 180, weights = [0.995, 0.001, 0.004],
				 tmax = 365*3, effect_size = 0.2, target_percentage = 50):

		self.upgrade = upgrade
		self.maintenance = maintenance
		self.weekly_session = weekly_session
		self.no_repeats = no_repeats
		self.seed_start = seed_start
		self.max_agents = max_agents
		self.no_friends = no_friends
		self.initial_Q = initial_Q
		self.upgrade_rate = upgrade_rate
		self.degradation_rate = degradation_rate
		self.policy_date = policy_date
		self.upgrade_length = upgrade_length
		self.weights = weights
		self.tmax = tmax
		self.effect_size = effect_size
		self.target_percentage = target_percentage

		self.boys = np.zeros((self.tmax-5, self.no_repeats))
		self.girls = np.zeros((self.tmax-5, self.no_repeats))
		self.total = np.zeros((self.tmax-5, self.no_repeats))

		self.bottom = np.zeros((self.tmax-5, self.no_repeats))
		self.top = np.zeros((self.tmax-5, self.no_repeats))

		for i in range(self.no_repeats):

			random.seed(i+seed_start)
			agents = Network.generate_agents(self.max_agents)
			Network.assign_friends(agents, self.no_friends)
			Network.assign_activity_groups(agents, self.max_agents)

			sdobj = SystemDynamics(self.initial_Q, self.degradation_rate, self.upgrade, 
								   self.upgrade_rate, self.policy_date, self.upgrade_length, 
								   self.maintenance)
			model = HybridSimulation(agents)

			if self.weekly_session:
				model.intervention(sdobj, self.weights, self.tmax, self.policy_date, 
								   self.effect_size, self.target_percentage)
			else:
				model.simulation(sdobj, self.weights, self.tmax)

			boys = []
			index = 7

			while index <= len(model.boys):
				rolling_av = (sum(model.boys[index-7:index])*100*2)/(7*self.max_agents)
				boys.append(rolling_av)
				index += 1

			girls = []
			index = 7

			while index <= len(model.girls):
				rolling_av = (sum(model.girls[index-7:index])*100*2)/(7*self.max_agents)
				girls.append(rolling_av)
				index += 1

			total = []
			index = 7

			while index <= len(model.total):
				rolling_av = (sum(model.total[index-7:index])*100)/(7*self.max_agents)
				total.append(rolling_av)
				index += 1

			self.boys[:,i] = boys
			self.girls[:,i] = girls
			self.total[:,i] = total 

			bottom = []
			for j in range(len(agents[0].weekly_visits)):
				average = np.mean([x.weekly_visits[j] for x in agents if x.sex == 'F' and x.activity_group == 1])
				bottom.append(average)
				
			top = []
			for j in range(len(agents[0].weekly_visits)):
				average = np.mean([x.weekly_visits[j] for x in agents if x.sex == 'F' and x.activity_group == 0])
				top.append(average)

			self.bottom[:,i] = bottom
			self.top[:,i] = top

			print('Iteration ' + str(i+1) + ' complete.')

	def plot_users(self, filename):

		plt.plot(np.linspace(5, self.tmax, self.tmax-5), np.mean(self.boys, axis = 1), 
				 label = 'Boys', alpha = 0.75)
		plt.plot(np.linspace(5, self.tmax, self.tmax-5), np.mean(self.girls, axis = 1), 
				 color = 'red', label = 'Girls', alpha = 0.75)
		plt.plot(np.linspace(5, self.tmax, self.tmax-5), np.mean(self.total, axis = 1), 
				 color = 'purple', label = 'Total', alpha = 0.75)
		plt.axvline(x=365, color = 'black', linestyle = '--', alpha = 0.75)
		plt.ylim(0,100)
		plt.xlabel('Days')
		plt.ylabel('Weekly rolling average percentage \n of children at the park')
		plt.legend()
		plt.savefig(filename, dpi=300, bbox_inches='tight')
		plt.show()


	def plot_weekly_visits(self, filename):

		plt.plot(np.linspace(5, self.tmax, self.tmax-5), np.mean(self.top, axis = 1), 
				 color = 'green', label = 'Most active', alpha = 0.75)
		plt.plot(np.linspace(5, self.tmax, self.tmax-5), np.mean(self.bottom, axis = 1), 
				 color = 'red', label = 'Least active', alpha = 0.75)
		plt.axvline(x=365, color = 'black', linestyle = '--', alpha = 0.75)
		plt.ylim(0,7)
		plt.xlabel('Days')
		plt.ylabel('Average number of visits to the \n park per week for girls only')
		plt.legend()
		plt.savefig(filename, dpi=300, bbox_inches='tight')
		plt.show()



		