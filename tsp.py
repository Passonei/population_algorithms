import numpy as np

def generate_distance(num):
    table = np.random.rand(num,num)*100
    np.fill_diagonal(table, 0)
    return table
    
def generate_coordinates(num):
    coordinate = np.random.rand(2,num)*100
    return coordinate

if __name__ == "__main__":
    # najgorszy przypadek to O(n!)
    # (n-1)! kombinacji
    np.random.seed(2137)
    print("Enter the number of nodes")
    num = int(input())
    coordinate_table = generate_coordinates(num)
    np.save("Tsp_data/coordinate_table",coordinate_table)