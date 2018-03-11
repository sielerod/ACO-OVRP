# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 23:24:42 2018
Authors: Lirielly Vitorugo Nascimento & Rafael Nascimento
E-mail: lvitorugo@gmail.com & rafael.correian@gmail.com
Date and hour: 02-01-2018 09:00:00 PM
"""

from ant import Ant
import numpy as np
import copy

class AntColony(object):
    def __init__(self, distances, distance_cost, n_ants, n_best, n_iterations, 
                 rho, alpha, beta, time_matrix, occupancies, vehicles):
        """
        Args:
            distances (2D numpy.array): Square matrix of distances. Diagonal is assumed to be np.inf.
            distance_cost: Cost of one unit of distance
            n_ants (int): Number of ants running per iteration
            n_best (int): Number of best ants who deposit pheromone
            n_iteration (int): Number of iterations
            rho (float): Rate it which pheromone decays. The pheromone value is multiplied by decay, so 0.95 will lead to decay, 0.5 to much faster decay.
            alpha (int or float): exponenet on pheromone, higher alpha gives pheromone more weight. Default=1
            beta (int or float): exponent on distance, higher beta give distance more weight. Default=1
            time_matrix (2D numpy.array): matrix of time of travel between pairs of nodes 
            occupancies (list): list of occupancy units of vehicles
            vehicles (list): list of vehicles
                  
        """
        self.distances = distances
        self.distance_cost = distance_cost
        self.pheromone = np.ones(self.distances.shape)
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.times = time_matrix
        self.occupancies = occupancies
        self.vehicles = vehicles
   
    
    def find_n_bests_ants(self, colony):
        '''
        Function to find the n ants that will update the pheromone trail
        '''
        colony.sort(key=lambda ant: ant.of())
        return colony[:self.n_best]
    
    
    def go_through_path(self, ant, factor):
        '''
        Function to calculate the amount of pheromone to be deposited in trail piece 
        '''
        current_node = ant.path[0]
        for i in range(len(ant.path) - 1):
            next_node = ant.path[i + 1]
            self.pheromone[current_node, next_node] += factor/ant.distance
    
    
    def update_pheromone(self, best_ant, n_bests_ants):
        '''
        Function to update the pheromone matrix
        '''
        self.pheromone *= self.rho
        
        for i in range(self.n_best):
            self.go_through_path(n_bests_ants[i], (self.n_best - i))
                
        self.go_through_path(best_ant, (self.n_best + 1))
        
        
    def run(self):
        '''
        Function to run the rank based Ant Colony Optimization algorithm
        '''       
        best_ant = Ant(0, 0, [])
        
        for i in range(self.n_iterations):
            print("Iteration: %d Best OF: %f" %(i, best_ant.of()))
            colony = []
            for j in range(self.n_ants):
                ant = Ant(0, self.distances.shape[0], copy.deepcopy(self.vehicles))
                for x in range(len(ant.vehicles)): 
                    ant.vehicles[x].put_node_path(0, self.occupancies, 
                                self.distances, self.times)
                ant.build_path(self.distances, self.times, self.occupancies,
                               self.pheromone, self.alpha, self.beta)
                ant.calculate_distance(self.distances)
                ant.objectve_function(self.distance_cost)
                colony.append(ant)    
            
            n_bests_ants = self.find_n_bests_ants(colony)
            
            if n_bests_ants[0].of() < best_ant.of():
                best_ant = n_bests_ants[0]
                
            self.update_pheromone(best_ant, n_bests_ants)
        return best_ant