import numpy as np

class Ants_colony:
    def __init__(self, coordinate_table, num_ants, alpha=1, 
                beta=1, evaporation_rate=0.5, q0=0.5):
        self.coordinate_table = coordinate_table
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q0 = q0
        self.num_nodes = len(coordinate_table[0])
        self.pheromone_table = np.ones((self.num_nodes ,self.num_nodes))
        self.best_result = np.inf
        self.best_route = []

    def dist(self, i, j):
        P = self.coordinate_table
        return np.sqrt((P[0][i]-P[0][j])**2+(P[1][i]-P[1][j])**2)

    def calculate_distance(self,route):
        distance = 0
        for i in range(len(route)-1):
            distance += self.dist(route[i],route[i+1])
        distance += self.dist(route[-1],route[0])
        return distance

    def generate_route(self, start_node):
        route = [start_node]
        nodes_to_visit = list(range(self.num_nodes))
        nodes_to_visit.remove(start_node)
        while nodes_to_visit:
            next_node = self.choose_next_node(route[-1], nodes_to_visit)
            route.append(next_node)
            nodes_to_visit.remove(next_node)
        return route
    
    def choose_next_node(self, current_node, nodes_to_visit):
        if np.random.rand() < self.q0:
            return self.greedy_choice(current_node, nodes_to_visit)
        else:
            return self.random_choice(current_node, nodes_to_visit)
    
    def greedy_choice(self, current_node, nodes_to_visit):
        return max(nodes_to_visit, key=lambda x: self.pheromone_table[current_node][x]**self.alpha * (1/self.dist(current_node,x))**self.beta)
    
    def random_choice(self, current_node, nodes_to_visit):
        probability = []
        for node in nodes_to_visit:
            probability.append(self.pheromone_table[current_node][node]**self.alpha * (1/self.dist(current_node,node))**self.beta)
        probability = probability/np.sum(probability)
        return np.random.choice(nodes_to_visit, p=probability)
    
    def update_pheromone_table(self, route, value):
        for i in range(len(route)-1):
            self.pheromone_table[route[i]][route[i+1]] += 1/value
        self.pheromone_table[route[-1]][route[0]] += 1/value

    def update_pheromone_table_evaporation(self):
        self.pheromone_table = (1-self.evaporation_rate)*self.pheromone_table

    def run(self, iterations):
        for i in range(iterations):
            for ant in range(self.num_ants):
                route = self.generate_route(np.random.randint(self.num_nodes))
                value = self.calculate_distance(route)
                self.update_pheromone_table(route,value)

                if value < self.best_result:
                    self.best_result = value
                    self.best_route = route
                    print("New min value",value)

            self.update_pheromone_table_evaporation()
            
            if i%(iterations//10)==0:
                print("Iteration: ",i)
                
        print("best result: ",self.best_route, self.best_result) 
        return self.best_route