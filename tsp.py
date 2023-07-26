import numpy as np
    
def generate_coordinates(num):
    coordinate = np.random.rand(2,num)*100
    return coordinate

if __name__ == "__main__":
    np.random.seed(1)
    print("Enter the number of nodes")
    num = int(input())
    coordinate_table = generate_coordinates(num)
    np.save("Tsp_data/coordinate_table",coordinate_table)