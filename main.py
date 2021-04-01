from ast import literal_eval as make_tuple
from state_space import StateSpace
from heuristic_a import HeuristicA
from heuristic_b import HeuristicB
import sys


def read_file(path, list_of_tuples):
    input_file = open(path)
    lines = input_file.readlines()

    # print("Reading input file:")
    count = 0
    for line in lines:
        if len(line) > 1:
            tmp = make_tuple(line.strip().replace(';', ','))
            list_of_tuples.append(tmp)


if __name__ == '__main__':

    dir_path = sys.argv[1]

    list_of_tuples = []
    read_file(dir_path + "\\input.txt", list_of_tuples)

    # goal_tuple = ((1, 2, 3), (4, 5, 6), (7, 8, 9))
    goal_tuple = []

    available_numbers = []
    size = len(list_of_tuples[0])

    for n in range(1, (size * size) + 1):
        available_numbers.append(n)

    for k in range(0, size):
        tmp = []
        for j in range(0, size):
            tmp.append(available_numbers.pop(0))
        goal_tuple.append(tuple(tmp))

    goal_tuple = tuple(goal_tuple)

    for i in range(1, len(list_of_tuples)):
        print("Solving puzzle #{}: {}".format(i, list_of_tuples[i - 1]))
        state_space = StateSpace(list_of_tuples[i - 1], goal_tuple, i, dir_path + "\\")

        # Depth First Search
        # state_space.dfs(10)

        # Breadth First Search
        # state_space.bfs()

        # Heuristic A
        # heuristic_a = HeuristicA(list_of_tuples[i-1], goal_tuple, i, dir_path + "\\")
        # heuristic_a.start()

        # heuristic B
        heuristic_b = HeuristicB(list_of_tuples[i - 1], goal_tuple, i, dir_path + "\\")
        heuristic_b.start()
