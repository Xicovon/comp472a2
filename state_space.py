import time


class Node:
    def __init__(self, grid, parent, depth):
        self.grid = grid
        self.parent = parent
        self.depth = depth

    def swap(self, i, j):
        # creates a new tuple with the two slots swapped
        # print("swapping {}, and {}".format(i, j))
        # print(self.grid[int(i / len(self.grid))][i % 3])
        # print(self.grid[int(j / len(self.grid))][j % 3])

        # convert into list
        l = list(self.grid)
        for k in range(0, len(l)):
            l[k] = list(l[k])

        # swap
        tmp = l[int(i / len(l))][i % 3]
        l[int(i / len(l))][i % 3] = l[int(j / len(l))][j % 3]
        l[int(j / len(l))][j % 3] = tmp

        # convert back into tuple
        for i in range(0, len(l)):
            l[i] = tuple(l[i])

        return tuple(l)


# create 12 new nodes based on current node
def expand_node(node):
    new_nodes = []

    # horizontal swaps
    new_nodes.append(Node(node.swap(0, 1), node, node.depth + 1))
    new_nodes.append(Node(node.swap(1, 2), node, node.depth + 1))
    new_nodes.append(Node(node.swap(3, 4), node, node.depth + 1))
    new_nodes.append(Node(node.swap(4, 5), node, node.depth + 1))
    new_nodes.append(Node(node.swap(6, 7), node, node.depth + 1))
    new_nodes.append(Node(node.swap(7, 8), node, node.depth + 1))

    # vertical swaps
    new_nodes.append(Node(node.swap(0, 3), node, node.depth + 1))
    new_nodes.append(Node(node.swap(1, 4), node, node.depth + 1))
    new_nodes.append(Node(node.swap(2, 5), node, node.depth + 1))
    new_nodes.append(Node(node.swap(3, 6), node, node.depth + 1))
    new_nodes.append(Node(node.swap(4, 7), node, node.depth + 1))
    new_nodes.append(Node(node.swap(5, 8), node, node.depth + 1))

    return new_nodes


class StateSpace:
    def __init__(self, start, goal, puzzle_number, file_path):
        self.goal_state = goal
        self.start_state = Node(start, None, 0)
        # this integer is used to number the output files for multiple input puzzles
        self.puzzle_number = puzzle_number
        self.file_path = file_path

    def write_to_file(self, list_to_write, file_name):
        f = open(file_name, "w")

        f.write("{}\n".format(self.start_state.grid))

        for ln in list_to_write:
            f.write("{}\n".format(ln.grid))

        f.write("{}\n".format(self.goal_state))

        f.close()

    # breadth first search
    def bfs(self):
        start = time.time()

        current_node = self.start_state
        node_queue = [current_node]

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
            # print("Currently exploring node: {}, at depth {}".format(current_node.grid, current_node.depth))
            # check if current node has already been expanded
            for n in visited_nodes:
                # if the same node has already been visited, go next
                if n.grid == current_node.grid:
                    # print("Node has already been expanded")
                    if len(node_queue) == 0:
                        no_solution = True
                        break
                    current_node = node_queue.pop()
                    skip = True
                    break

            if not skip:
                # expand the current node
                expanded_nodes = expand_node(current_node)

                # once expanded add the current node to list of expanded nodes
                visited_nodes.insert(0, current_node)

                # add the expanded nodes onto the stack
                for n1 in expanded_nodes:
                    # node_already_visited = False

                    # for n2 in visited_nodes:
                        # if the same node has already been visited, go next
                    #    if n1.grid == n2.grid:
                    #        node_already_visited = True

                    #if not node_already_visited:
                        node_queue.insert(0, n1)

                # pop the last node to move to
                if len(node_queue) == 0:
                    no_solution = True
                    break
                current_node = node_queue.pop()

        end = time.time()
        elapsed_time = end - start
        print("The length of the node queue is {}".format(len(node_queue)))
        print("BFS elapsed time: {}".format(elapsed_time))

        # path
        path = []
        c = current_node
        while c.parent is not None:
            path.append(c)
            c = c.parent

        if no_solution:
            f = open(self.file_path + "bfs_solution_path_{}.txt".format(self.puzzle_number), "w")
            f.write("no_solution")
            f.close()

            f = open(self.file_path + "bfs_search_path_{}.txt".format(self.puzzle_number), "w")
            f.write("no_solution")
            f.close()
        else:
            path.reverse()
            self.write_to_file(path, self.file_path + "bfs_solution_path_{}.txt".format(self.puzzle_number))

            # output searched states
            self.write_to_file(visited_nodes, self.file_path + "bfs_search_path_{}.txt".format(self.puzzle_number))

    # depth first search
    def dfs(self, depth):
        start = time.time()

        current_node = self.start_state
        node_stack = [current_node]

        # list of nodes already expanded (do not expand these nodes again)
        visited_nodes = []
        no_solution = False

        # print("Start state: {}".format(current_node.grid))

        # 1- expand nodes from current node
        # 2- if none of the nodes are the goal node, move to the left most node
        while current_node.grid != self.goal_state and not no_solution:
            if time.time() - start > 60:
                no_solution = True
                break

            skip = False
            # print("Currently exploring node: {}, at depth {}".format(current_node.grid, current_node.depth))
            # print("List of expanded nodes")

            # depth cutoff
            if current_node.depth > depth:
                # print("Node is too deep to expand")
                # the node is too deep and will not be expanded again
                visited_nodes.append(current_node)

                # move to the next node
                if len(node_stack) == 0:
                    no_solution = True
                    break

                current_node = node_stack.pop()
            else:
                # print("Node is not too deep to expand")
                # check if current node has already been expanded
                for n in visited_nodes:
                    # if the same node has already been visited, go next
                    if n.grid == current_node.grid and n.depth <= current_node.depth:
                        # print("Node has already been expanded")
                        if len(node_stack) == 0:
                            no_solution = True
                            break
                        current_node = node_stack.pop()
                        skip = True
                        break

                if not skip:
                    # print("Node has not been expanded")
                    # expand the current node
                    expanded_nodes = expand_node(current_node)

                    # once expanded add the current node to list of expanded nodes
                    visited_nodes.append(current_node)

                    # add the expanded nodes onto the stack
                    node_already_visited = False
                    for n1 in expanded_nodes:
                        node_already_visited = False

                        for n2 in visited_nodes:
                            # if the same node has already been visited, go next
                            if n1.grid == n2.grid and n1.depth >= n2.depth:
                                node_already_visited = True

                        if not node_already_visited:
                            node_stack.append(n1)

                    # pop the last node to move to
                    if len(node_stack) == 0:
                        no_solution = True
                        break
                    current_node = node_stack.pop()

        end = time.time()
        elapsed_time = end - start
        print("The length of the node queue is {}".format(len(node_stack)))
        print("DFS elapsed time: {}".format(elapsed_time))

        # path
        path = []
        c = current_node
        while c.parent is not None:
            path.append(c)
            c = c.parent

        if no_solution:
            f = open(self.file_path + "dfs_solution_path_{}.txt".format(self.puzzle_number), "w")
            f.write("no_solution")
            f.close()

            f = open(self.file_path + "dfs_search_path_{}.txt".format(self.puzzle_number), "w")
            f.write("no_solution")
            f.close()
        else:
            path.reverse()
            self.write_to_file(path, self.file_path + "dfs_solution_path_{}.txt".format(self.puzzle_number))

            # output searched states
            self.write_to_file(visited_nodes, self.file_path + "dfs_search_path_{}.txt".format(self.puzzle_number))