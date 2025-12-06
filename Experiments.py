import random
import time

class Graph:
    def __init__(self, vertexes: int, density: float):
        self.vertexes = vertexes
        self.density = density
        self.matrix = []
        self.counter = 0


    def build_graph(self):

        for i in range(self.vertexes):
            self.matrix.append([0]*self.vertexes)

        for i in range(self.vertexes):
            for j in range(self.vertexes):

                if i == j:
                    continue

                if random.random() < self.density:
                    self.matrix[i][j] = 1




    def write_matrix(self):
        with open("experiments_data.txt", "w") as file:
            file.write("\n-----new matrix -----")
            file.write("\n")
            for e in self.matrix:
                file.write(f"{e}\n")
            file.write("\n")

    def algorithm(self):
        time1 = time.time()
        for start in range(self.vertexes):
            for end in range(self.vertexes):
                for transistor in range(self.vertexes):

                    self.matrix[start][end] = self.matrix[start][end] or (self.matrix[start][transistor] and self.matrix[transistor][end])
                    self.counter += 1
        time2 = time.time()
        exp_time = round(time2 - time1, 6)
        with open("experiments_data.txt", "a") as file:
            # file.write("\n-----matrix after the algorithm -----")
            # file.write("\n")
            # for e in self.matrix:
            #     file.write(f"{e}\n")
            file.write(f"\nTime consumed for algorithm: {exp_time}, number of iterations: {self.counter}, vertexes: {self.vertexes}, density: {self.density}")
            file.write("\n")
        file.close()

graph1 = Graph(200, 0.6)
graph1.build_graph()
print('###################')

i = 0
for i in range(0, 20):
    graph1.algorithm()
    i += 1







