import math

import pandas as pd


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            path[::-1]  # Return reversed path

            pathTotal = 0
            result = maze

            # Calcula o custo total do caminho mais rapido SP
            for i in range(len(path)):

                if result[path[i][0]][path[i][1]] == "T":
                    pathTotal += 1
                elif result[path[i][0]][path[i][1]] == "A":
                    pathTotal += 3

            # Escreve na matriz os Nodes Visitados
            #for i in range(len(visited_list)):
             #   result[visited_list[i].position[0]][visited_list[i].position[1]] = "V"

            # Escreve na matriz o caminho mais rapido SP
            for i in range(len(path)):
                result[path[i][0]][path[i][1]] = "SP"

            print(pathTotal)


            return result

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain


            if maze[node_position[0]][node_position[1]] != "T" and maze[node_position[0]][node_position[1]] != "E" and maze[node_position[0]][node_position[1]] != "A" and maze[node_position[0]][node_position[1]] != "S":
                continue

            # Create new node
            new_node = Node(current_node, node_position)


            print(maze[node_position[0]][node_position[1]])
            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            #child.h = math.sqrt(child.h)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)


def main():

    maze = [['S', 'F', 'F', 'F', 'F'],
            ['F', 'T', 'A', 'T', 'F'],
            ['F', 'T', 'B', 'T', 'F'],
            ['F', 'A', 'T', 'T', 'F'],
            ['F', 'F', 'F', 'F', 'E']]

    start = (0, 0)
    end = (4, 4)


    df = pd.read_csv('sample-environment.csv', index_col=False)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    #print(df)

    start = (0, 0)  # posicão inicial
    end = (4, 4)  # posição final
    cost = 1  # custo por movimento

    # salvamos o dataframe numa lista:
    #maze = df.values
    #print(maze[99][99])

    path = astar(maze, start, end)
    #print(path)

    print('\n'.join([''.join(["{:" ">4}".format(item) for item in row])
                     for row in path]))

if __name__ == '__main__':

    main()
