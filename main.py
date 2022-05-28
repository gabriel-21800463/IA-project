# Imports
import time
import numpy as np
import pandas as pd

class Node:

    # Construtor onde recebe os argumentos
    def __init__(self, parent=None, position=None, value=None):
        self.parent = parent
        self.position = position
        self.value = value

        self.g = 0
        self.h = 0
        self.f = 0

    # função onde compara posições e retorna um boolean
    def __eq__(self, other):
        return self.position == other.position

    # função onde retorna o custo total do node
    def __str__(self):
        return str(self.f)

def return_path(current_node, maze, visited_list):
    path = []
    values = []
    no_rows, no_columns = np.shape(maze)

    # aqui criamos o labirinto de resultados
    result = maze
    current = current_node

    # aqui é adicionado o caminho mais curto(SP) a lista path
    while current is not None:
        path.append(current.position)
        current = current.parent

    # Retorna o caminho invertido, pois precisamos mostrar do início ao fim do caminho
    path = path[::-1]
    path_total = 0

    #Calcula o custo total do caminho mais curto(SP)
    for i in range(len(path)):

        if result[path[i][0]][path[i][1]] == "T":
            path_total += 1
        elif result[path[i][0]][path[i][1]] == "A":
            path_total += 3

    #Escreve na matriz do resultado os nodes visitados
    for i in range(len(visited_list)):

        result[visited_list[i].position[0]][visited_list[i].position[1]] = "V"

    #Escreve na matriz resultado o caminho mais curto(SP)
    for i in range(len(path)):

        result[path[i][0]][path[i][1]] = "SP"

    #print(pathTotal)
    return result, path_total


def search(maze, start, end):
    # Cria o nó inicial e final com valores inicializados para g, h e f.
    start_node = Node(None, tuple(start), maze[0][0])
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end), maze[99][99])
    end_node.g = end_node.h = end_node.f = 0

    # Inicializa yet_to_visit e lista visitada
    # nesta lista vamos colocar todos os nós que são yet_to_visit para exploração.
    # A partir daqui, encontraremos o nó de menor custo para expandir em seguida
    yet_to_visit_list = []
    # nesta lista vamos colocar todos os nodos já explorados para não explorarmos novamente
    visited_list = []

    # Adiciona o nó inicial
    yet_to_visit_list.append(start_node)

    # Adicionando uma condição de parada. Isso é para evitar qualquer loop infinito e parar
    # execução após um número razoável de passos
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # (8 movimentos) de todas as posições
    move = [[-1, -1],  # diagonal para cima esquerda
            [-1, 0],  # para cima
            [-1, 1],  # diagonal para cima direita
            [0, -1],  # para esquerda
            [1, -1],  # diagonal para baixo esquerda
            [1, 0],  # para baixo
            [1, 1],  # diagonal para baixo direita
            [0, 1]]  # para direita

    # encontrar número de linhas e colunas
    no_rows, no_columns = np.shape(maze)

    # Loop até encontrar o final
    while len(yet_to_visit_list) > 0:

        # Toda vez que um nó é referido da lista yet_to_visit, o contador de operação de limite é incrementado
        outer_iterations += 1

        # Obtém o nó atual
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # se atingirmos este ponto, retorne o caminho, pois pode não haver solução ou
        # custo de computação é muito alto
        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return return_path(current_node, maze)

        # Retire o nó atual da lista ainda para visitar(yet_to_visit_list) e adicione à lista visitada(visited_list)
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # testa se a meta foi atingida ou não, se sim então retorna o caminho
        if current_node == end_node:
            return return_path(current_node, maze, visited_list)

        # Gera filhos de todos os quadrados adjacentes
        children = []
        for new_position in move:

            # Obtém a posição do nó
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Verifica o limite do labirinto
            if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            # Verifica o node adjacente para descobrir o tipo do node
            if maze[node_position[0]][node_position[1]] != "T" and maze[node_position[0]][node_position[1]] != "E" and \
                    maze[node_position[0]][node_position[1]] != "A" and maze[node_position[0]][node_position[1]] != "S":
                continue

            # Cria um novo node
            new_node = Node(current_node, node_position, maze[node_position[0]][node_position[1]])

            # Adicionar a lista dos filhos(children)
            children.append(new_node)

        # Loop através dos filhos
        for child in children:

            # o filho está na lista visitada (pesquise toda a lista visitada)
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Cria os valores de f, g e h
            if child.value == 'T':
                child.g = current_node.g + 1
            elif child.value == 'A':
                child.g = current_node.g + 3

            # Custos heurísticos calculados aqui, usando distância Manhattan
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # O filho já está na lista yet_to_visit e o custo g já é menor
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # Adiciona o filho à lista yet_to_visit
            yet_to_visit_list.append(child)


# Função Main()
if __name__ == '__main__':
    # Lemos o arquivo CSV para o dataframe
    df = pd.read_csv('sample-environment.csv', index_col=False)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # salvamos o dataframe numa lista:
    maze = df.values

    start = [0, 0]  # posicão inicial
    end = [99, 99]  # posição final

    start_time = time.time()

    path, path_total = search(maze, start, end)

    end_time = time.time()
    print(f"O Tempo de execução é de: {int(end_time - start_time)} segundos.")
    print(f"O custo Total do caminho mais curto é {path_total}.")


    print('\n'.join([''.join(["{:" ">4}".format(item) for item in row])
                     for row in path]))