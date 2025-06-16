## Network class ##

from agent import Agent
import random
from scipy.stats import beta
import math
import numpy as np

class Network:

	def generate_agents(target_no): 

		# List of agents created
		agent_list = []
		# Track no. of agents created
		agent_no = 0 
		
		while agent_no < target_no:

			# Generate a random sex
			sex = random.sample(['M', 'F'],1)[0]
			
			# Generate a random preference for play
			if sex == 'M':
				pref = beta.rvs(7, 4, size=1)
			else:
				pref = beta.rvs(4, 7, size=1)

			# Add new agent to list
			agent_list.append(Agent(sex, pref))
			
			# Update agent number tracker
			agent_no += 1

		return agent_list

	def assign_friends(agents, number):

		for i in range(len(agents)):
			
			agent = agents[i]

			while len(agent.friends) < number:

				possible_agents = [x for x in agents
								   if x != agent and
								   len(x.friends) < number and
								   x not in agent.friends]
				
				if len(possible_agents) == 0:
					break

				p = [(abs(agent.pref[-1]-x.pref))[0][0] for x in possible_agents]
				p = [1/x for x in p]

				if agent.sex == 'M':

					for j in range(len(possible_agents)):
						if possible_agents[j].sex == 'M':
							p[j] = p[j]*4

					p = [x/sum(p) for x in p]
					friends = np.random.choice(possible_agents, 
											   size = min(number - len(agent.friends), len(possible_agents)),
											   replace=False, p=p)
					for friend in friends:
						if friend not in agent.friends:
							agent.friends.append(friend)
						if agent not in friend.friends:
							friend.friends.append(agent)

				else:
					
					for j in range(len(possible_agents)):
						if possible_agents[j].sex == 'F':
							p[j] = p[j]*4
							
					p = [x/sum(p) for x in p]
					friends = np.random.choice(possible_agents, 
											   size = min(number - len(agent.friends), len(possible_agents)),
											   replace=False, p=p)
					for friend in friends:
						if friend not in agent.friends:
							agent.friends.append(friend)
						if agent not in friend.friends:
							friend.friends.append(agent)


	def assign_activity_groups(agents, target_no):

		sorted_agents = sorted([x for x in agents], key=lambda x: x.pref)

		for agent in agents: 
			if agent in sorted_agents[0:round(target_no/2)]:
				agent.activity_group = 1
			
