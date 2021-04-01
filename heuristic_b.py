import time


class Node:
    def __init__(self, grid, parent, depth):
        self.grid = grid
        self.parent = parent
        self.depth = depth
        self.heuristic = self.calculate_heuristic()

    def swap(self, i, j):
        # creates a new tuple with the two slots swapped
        # print("swapping {}, and {}".format(i, j))
        # print(self.grid[int(i / len(self.grid))][i % 3])
        # print(self.grid[int(j / len(self.grid))][j % 3])

        length = len(self.grid)

        # convert into list
        l = list(self.grid)
        for k in range(0, length):
            l[k] = list(l[k])

        # swap
        tmp = l[int(i / length)][i % length]
        l[int(i / len(l))][i % length] = l[int(j / length)][j % length]
        l[int(j / len(l))][j % length] = tmp

        # convert back into tuple
        for i in range(0, length):
            l[i] = tuple(l[i])

        # calculate heuristic and return new node
        tmp_node = Node(tuple(l), self, self.depth + 1)
        return tmp_node

    def calculate_heuristic(self):
        length = len(self.grid)
        count = 0
        for i in range(0, length * length):
            # count += abs(self.grid[int(i / length)][i % length] - i+1)

            cur_x = int(i / length)
            cur_y = i % length
            val = self.grid[int(i / length)][i % length] - 1
            goal_x = int(val / length)
            goal_y = val % length

            count += abs(cur_x - goal_x) + abs(cur_y - goal_y)

        return count + self.depth


# create 12 new nodes based on current node
def expand_node(node):
    new_nodes = []
    """
    # horizontal swaps
    new_nodes.append(node.swap(0, 1))
    new_nodes.append(node.swap(1, 2))
    new_nodes.append(node.swap(3, 4))
    new_nodes.append(node.swap(4, 5))
    new_nodes.append(node.swap(6, 7))
    new_nodes.append(node.swap(7, 8))

    # vertical swaps
    new_nodes.append(node.swap(0, 3))
    new_nodes.append(node.swap(1, 4))
    new_nodes.append(node.swap(2, 5))
    new_nodes.append(node.swap(3, 6))
    new_nodes.append(node.swap(4, 7))
    new_nodes.append(node.swap(5, 8))
    """
    length = len(node.grid)
    for r in range(0, length):
        for c in range(0, length - 1):
            new_nodes.append(node.swap((r * length) + c, (r * length) + c + 1))

    for c in range(0, length):
        for r in range(0, length - 1):
            new_nodes.append(node.swap((r * length) + c, ((r + 1) * length) + c))

    return new_nodes


class HeuristicB:
    def __init__(self, start, goal, puzzle_number, file_path):
        self.goal_state = goal
        self.start_state = Node(start, None, 0)
        # this integer is used to number the output files for multiple input puzzles
        self.puzzle_number = puzzle_number
        self.file_path = file_path

        # moved the list of frontier nodes to an instance variable
        self.node_list = []

    # return the node with the highest heuristic value
    def select_node(self):
        # print("length of node list: {}".format(len(self.node_list)))

        if len(self.node_list) == 0:
            return None
        else:
            best_node_index = 0
            for i in range(1, len(self.node_list)):
                # if the current node has a better heuristic cost take its index
                if self.node_list[i].heuristic < self.node_list[best_node_index].heuristic:
                    best_node_index = i

            # print("index of best node: {}".format(best_node_index))

            return self.node_list.pop(best_node_index)

    def write_to_file(self, list_to_write, file_name):
        f = open(file_name, "w")

        f.write("{}\n".format(self.start_state.grid))

        for ln in list_to_write:
            f.write("{}\n".format(ln.grid))

        f.write("{}\n".format(self.goal_state))

        f.close()

    # breadth first search
    def start(self):
        start = time.time()

        current_node = self.start_state
        self.node_list = []

        # list of nodes already expanded (do not expand these nodes again)
        visited_nodes = []
        no_solution = False

        # 1- expand nodes from current node
        # 2- if none of the nodes are the goal node, move to the left most node
        while current_node.grid != self.goal_state and not no_solution:
            if time.time() - start > 60:
                no_solution = True
                break

            skip = False
            # print("Currently exploring node: {}, at depth {}, with heuristic {}".format(current_node.grid, current_node.depth, current_node.heuristic))
            # check if current node has already been expanded
            for n in visited_nodes:
                # if the same node has already been visited, go next
                if n.grid == current_node.grid:
                    current_node = self.select_node()
                    if current_node is None:
                        no_solution = True
                        break
                    skip = True
                    break

            if not skip:
                # The current Node has not been expanded
                # expand the current node
                expanded_nodes = expand_node(current_node)

                # once expanded add the current node to list of expanded nodes
                visited_nodes.append(current_node)

                # add the expanded nodes onto the stack
                for n1 in expanded_nodes:
                    # print("Child node {}, with heuristic {}".format(n1.grid, n1.heuristic))
                    if n1.heuristic <= current_node.heuristic + 2:
                        self.node_list.insert(0, n1)

                current_node = self.select_node()
                if current_node is None:
                    no_solution = True
                    break

        end = time.time()
        elapsed_time = end - start
        print("The length of the node queue is {}".format(len(self.node_list)))
        print("Heuristic B elapsed time: {}".format(elapsed_time))

        # path
        path = []
        c = current_node
        if c is not None:
            while c.parent is not None:
                path.append(c)
                c = c.parent

        if no_solution:
            f = open(self.file_path + "heuristic_b_solution_path_{}.txt".format(self.puzzle_number), "w")
            f.write("no_solution")
            f.close()

            f = open(self.file_path + "heuristic_b_search_path_{}.txt".format(self.puzzle_number), "w")
            f.write("no_solution")
            f.close()
        else:
            path.reverse()
            self.write_to_file(path, self.file_path + "heuristic_b_solution_path_{}.txt".format(self.puzzle_number))

            # output searched states
            self.write_to_file(visited_nodes, self.file_path + "heuristic_b_search_path_{}.txt".format(self.puzzle_number))
