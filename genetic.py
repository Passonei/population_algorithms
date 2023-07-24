import numpy as np

coordinate_table = np.load("Tsp_data/coordinate_table.npy")

def dist(P, i, j):
    return np.sqrt((P[0][i]-P[0][j])**2+(P[1][i]-P[1][j])**2)

def calculate_distance(route):
    distance = 0
    for i in range(len(route)-1):
        distance += dist(coordinate_table,route[i],route[i+1])
    distance += dist(coordinate_table,route[-1],route[0])
    return distance


class Genetic_algorithm:
    def __init__(self, coordinate_table, generations, num_population, mutation_probability=0.05):
        self.coordinate_table = coordinate_table
        self.generations = generations
        self.population = self.generate_population(num_population)
        self.mutation_probability = mutation_probability
        self.best_result = np.inf
        self.best_route = []
        self.mutation_num=0

    def generate_population(self, num_population):
        population = []
        for _ in range(num_population):
            population.append([0]+list(np.random.permutation(len(self.coordinate_table[0])-1)+1))
        return population

    def selection(self, population):
        fitness = []
        for i in range(len(population)):
            fitness.append(1/calculate_distance(population[i]))
        fitness = np.array(fitness)
        fitness = fitness/fitness.sum()
        return np.random.choice(len(population), 2, p=fitness)

    def mutation(self, route):
        route = route[1:]
        i = np.random.randint(0, len(route))
        j = np.random.randint(0, len(route))
        route[i], route[j] = route[j], route[i]
        self.mutation_num+=1
        return [0] + route
    
    def crossover(self, parent1, parent2):
        parent1 = parent1[1:]
        parent2 = parent2[1:]
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
        return [0] + list(child.astype(int))

    def next_generation(self):
        new_population=[]
        for _ in range(len(self.population)//2):
            idx = self.selection(self.population)
            parent1, parent2 = self.population[idx[0]], self.population[idx[1]]
            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)
            if np.random.ranf()<self.mutation_probability:
                child1 = self.mutation(child1)
            if np.random.ranf()<self.mutation_probability:
                child2 = self.mutation(child2)
            new_population.append(child1)
            new_population.append(child2)
        return new_population
    
    def validate(self):
        for route in self.population:
            value = calculate_distance(route)
            if value<self.best_result:
                self.best_route = route
                self.best_result = value
                print(value)

    def cycle(self):
        for i in range(self.generations):
            self.validate()
            self.population = self.next_generation()
            print(i)
        print("best result: ",self.best_route, self.best_result) 

g = Genetic_algorithm(coordinate_table, 30, 200, mutation_probability=0.1)
a=g.cycle()
