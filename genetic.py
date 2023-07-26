import numpy as np

class Genetic_algorithm:
    def __init__(self, coordinate_table, generations, num_population, mutation_probability=0.05):
        self.coordinate_table = coordinate_table
        self.generations = generations
        self.population = self.generate_population(num_population)
        self.mutation_probability = mutation_probability
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

    def generate_population(self, num_population):
        population = []
        greedy_route = [0]
        nodes_to_visit = list(range(len(self.coordinate_table[0])))
        nodes_to_visit.remove(0)
        while nodes_to_visit:
            next_node = max(nodes_to_visit, key=lambda x: (1/self.dist(greedy_route[-1],x)))
            greedy_route.append(next_node)
            nodes_to_visit.remove(next_node)
        population.append(greedy_route)
        for _ in range(num_population):
            population.append(list(np.random.permutation(len(self.coordinate_table[0]))))
        return population

    def selection(self, population):
        fitness = []
        for i in range(len(population)):
            fitness.append(1/(self.calculate_distance(population[i])**2))
        fitness = np.array(fitness)
        fitness = fitness/fitness.sum()
        return np.random.choice(len(population), 2, p=fitness)
    
    def choose_elite(self):
        fitness = []
        for i in range(len(self.population)):
            fitness.append(1/(self.calculate_distance(self.population[i])**2))
        fitness = np.array(fitness)
        fitness = fitness/fitness.sum()
        idx = np.argsort(fitness)[-int(len(self.population)*0.1):]
        return idx

    def mutation(self, route):
        i = np.random.randint(0, len(route))
        j = np.random.randint(0, len(route))
        route[i], route[j] = route[j], route[i]
        return route
    
    def crossover(self, parent1, parent2):
        child = np.ones(len(parent1))
        child[0] = parent1[0]
        for i in range(1, len(parent1)):
            if parent2[i] not in child:
                child[i] = parent2[i]
            else:
                for j in range(len(parent1)):
                    if parent1[j] not in child:
                        child[i] = parent1[j]
                        break
        return list(child.astype(int))
    
    def order_crossover(self, parent1, parent2):
        i = np.random.randint(0, len(parent1))
        j = np.random.randint(0, len(parent1))
        part_from_parent1=[]

        if i>j:
            i,j = j,i
        for k in range(i, j):
            part_from_parent1.append(parent1[k])

        part_from_parent2 = [x for x in parent2 if x not in part_from_parent1]
        child = part_from_parent1 + part_from_parent2
        return child
            
    def next_generation(self):
        new_population=[]
        for elite in self.choose_elite():
            new_population.append(self.population[elite])

        while len(new_population)<len(self.population)-1:
            idx = self.selection(self.population)
            parent1, parent2 = self.population[idx[0]], self.population[idx[1]]
            child1 = self.crossover(parent1, parent2)
            child1 = self.order_crossover(parent2, parent1)
            child2 = self.order_crossover(parent1, parent2)

            if np.random.ranf()<self.mutation_probability:
                child1 = self.mutation(child1)
            if np.random.ranf()<self.mutation_probability:
                child2 = self.mutation(child2)
                
            new_population.append(child1)
            new_population.append(child2)
        return new_population
    
    def validate(self):
        for route in self.population:
            value = self.calculate_distance(route)
            if value<self.best_result:
                self.best_route = route
                self.best_result = value
                print("New min value",value)

    def run(self):
        for i in range(self.generations):
            self.validate()
            self.population = self.next_generation()

            if i%(self.generations//10)==0:
                print("Generation ",i)
        
        print("best result: ",self.best_route, self.best_result) 
        return self.best_route