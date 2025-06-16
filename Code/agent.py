## Agent class ##

import random
import math
from scipy.stats import bernoulli

class Agent:

	id_counter = 0

	def __init__(self, sex, pref):

		# agent ID 
		self.id = type(self).id_counter
		type(self).id_counter += 1

		# agent sex
		self.sex = sex

		# agent's friendship group
		self.friends = []

		# agent's preference for play
		self.pref = [pref]
		
		# decision to play today
		self.decision = [bernoulli.rvs(self.pref,1)-1]

		# rolling number of visits
		self.weekly_visits = []

		# 50% least active?
		self.activity_group = 0

	def no_weekly_visits(self):

		number = sum(self.decision[-7:])
		self.weekly_visits.append(number)
