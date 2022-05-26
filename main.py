import math

import pandas as pd
import numpy as np
from ipythonblocks import BlockGrid, colors

class Node:
    """
         Uma classe de nó para descoberta de caminho A*
         pai é pai do nó atual
         position é a posição atual do Node no labirinto
         g é o custo desde o início até o nó atual
         h é o custo estimado baseado em heurística para o nó atual para o nó final
         f é o custo total do nó presente, ou seja: f = g + h
    """

    def __init__(self, parent=None, position=None, value=None):
        self.parent = parent
        self.position = position
        self.value = value

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __str__(self):
        return str(self.f)

    def print_list(node):
        while node:
            print(node),
            node = node.next


# Esta função retorna o caminho da busca
def return_path(current_node, maze, visited_list):
    path = []
    values = []
    no_rows, no_columns = np.shape(maze)

    # aqui criamos o labirinto de resultados inicializado com -1 em cada posição
    result = maze  #[['F' for i in range(no_columns)] for j in range(no_rows)]
    current = current_node

    # print(current.position)
    # print(current.position[0])
    # print(current.position[1])

    while current is not None:
        # path.append(tuple((current.position[0], current.position[1])))
        path.append(current.position)
        current = current.parent


    # Retorna o caminho invertido, pois precisamos mostrar do início ao fim do caminho
    path = path[::-1]
    pathTotal = 0

    #Calcula o custo total do caminho mais rapido SP
    for i in range(len(path)):

        if result[path[i][0]][path[i][1]] == "T":
            pathTotal += 1
        elif result[path[i][0]][path[i][1]] == "A":
            pathTotal += 3

    #Escreve na matriz os Nodes Visitados
    for i in range(len(visited_list)):

        result[visited_list[i].position[0]][visited_list[i].position[1]] = "V"

    #Escreve na matriz o caminho mais rapido SP
    for i in range(len(path)):

        result[path[i][0]][path[i][1]] = "SP"

    #print(pathTotal)
    return result, pathTotal



def search(maze, cost, start, end):
    """
         Retorna uma lista de tuplas como um caminho desde o início até o final especificado no labirinto especificado
         :param labirinto:
         :param custo:
         :param start:
         :param end:
         :Retorna:
    """

    # Cria o nó inicial e final com valores inicializados para g, h e f.
    start_node = Node(None, tuple(start), maze[0][0])
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end), maze[4][4])
    end_node.g = end_node.h = end_node.f = 0

    # print(start_node.parent)

    # Inicializa yet_to_visit e lista visitada
    # nesta lista vamos colocar todos os nós que são yet_to_visit para exploração.
    # A partir daqui, encontraremos o nó de menor custo para expandir em seguida
    yet_to_visit_list = []
    # nesta lista vamos colocar todos os nodos já explorados para não explorarmos novamente
    visited_list = []

    # Adiciona o nó inicial
    yet_to_visit_list.append(start_node)
    # print(yet_to_visit_list[0].parent)

    # Adicionando uma condição de parada. Isso é para evitar qualquer loop infinito e parar
    # execução após um número razoável de passos
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # quais quadrados procuramos.
    # O movimento de busca é esquerda-direita-topo-inferior
    # (4 movimentos) de todas as posições

    move = [[-1, -1],  # diagonal cima esquerda
            [-1, 0],  # go up
            [-1, 1],  # diagonal cima direita
            [0, -1],  # go left
            [1, -1],  # diagonal baixo esquerda
            [1, 0],  # go down
            [1, 1],  # diagonal baixo direita
            [0, 1]]  # go right


    """
        1) Primeiro obtemos o nó atual comparando todos os custos f e selecionando o nó de custo mais baixo para expansão adicional
        2) Verifique a iteração máxima alcançada ou não. Definir uma mensagem e interromper a execução
        3) Remova o nó selecionado da lista yet_to_visit e adicione este nó à lista visitada
        4) Execute o teste de meta e retorne o caminho, caso contrário, execute as etapas abaixo
        5) Para o nó selecionado, descubra todos os filhos (use mover para encontrar filhos)
            a) obter a posição atual para o nó selecionado (este se torna o nó pai para os filhos)
            b) verificar se existe uma posição válida (o limite tornará alguns nós inválidos)
            c) se qualquer nó é uma parede, ignore isso
            d) adicionar à lista de nós filhos válida para o pai selecionado

            Para todos os nodos filhos
                a) se filho na lista visitada, ignore-o e tente o próximo nó
                b) calcular os valores do nó filho g, h e f
                c) se filho na lista yet_to_visit, ignore-o
                d) senão mova o filho para a lista yet_to_visit
    """

    # encontrar labirinto tem quantas linhas e colunas
    no_rows, no_columns = np.shape(maze)
    # print(no_rows)
    # print(no_columns)

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

#       print(len(yet_to_visit_list))
        # Retire o nó atual da lista yet_to_visit, adicione à lista visitada
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # print(visited_list[0].value)
        # print(len(visited_list))

        # testa se a meta foi atingida ou não, se sim então retorna o caminho

        # print(current_node == end_node)

        if current_node == end_node:
            return return_path(current_node, maze, visited_list)  # 0

        # Gera filhos de todos os quadrados adjacentes
        children = []
        for new_position in move:

            # Obtém a posição do nó
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Certifique-se dentro do alcance (verifique se dentro do limite do labirinto)
            if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

                # print(node_position[0])
            # print(node_position[1])
            # print(maze[node_position[0]][node_position[1]])
            # break

            # Certifique-se de que o terreno possa ser percorrido
            if maze[node_position[0]][node_position[1]] == 'F' or maze[node_position[0]][node_position[1]] == 'B':
                # print('Sou igual de F')
                continue

            # print(current_node.position[0])
            # print(current_node.position[1])
            # print(maze[node_position[0]][node_position[1]])
            # break

            # print(node_position[0])
            # print(node_position[1])

            # Cria um novo nó
            new_node = Node(current_node, node_position, maze[node_position[0]][node_position[1]])

            # print(new_node.parent)

            # Adicionar a lista
            children.append(new_node)

        # Loop através dos filhos
        for child in children:

            # A criança está na lista visitada (pesquise toda a lista visitada)
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # Cria os valores de f, g e h
            # child.g = current_node.g + cost

            # print(child.value)

            if child.value == 'T':
                child.g = current_node.g + 1
            elif child.value == 'A':
                child.g = current_node.g + 3

            # Custos heurísticos calculados aqui, usando distância euclidiana
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))  # adicionar a Raiz

            # Com Raiz quadara
            #raiz = math.sqrt(child.h)
            #print(int(raiz))

            #Numpy
            #dist = np.linalg.norm(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            #print(dist)


            child.f = child.g + child.h

            # A criança já está na lista yet_to_visit e o custo g já é menor
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # Adiciona o filho à lista yet_to_visit
            yet_to_visit_list.append(child)


if __name__ == '__main__':

    maze = [['S', 'F', 'F', 'F', 'F'],
            ['F', 'T', 'A', 'T', 'F'],
            ['F', 'T', 'B', 'T', 'F'],
            ['F', 'A', 'B', 'T', 'F'],
            ['F', 'F', 'F', 'F', 'E']]

    """
            [['S' 'F' 'F' 'F' 'F'],
             ['F' 'T' 'A' 'T' 'F'],
             ['F' 'T' 'B' 'T' 'F'],
             ['F' 'A' 'B' 'T' 'F'],
             ['F' 'F' 'F' 'F' 'E']]
    """

    df = pd.read_csv('sample-environment.csv', index_col=False)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    print(df)

    start = [0, 0]  # posicão inicial
    end = [99, 99]  # posição final
    cost = 1  # custo por movimento

    # salvamos o dataframe numa lista:

    #maze = df.values
    #print(maze)

    path, custoTotal = search(maze, cost, start, end)

    print(f"O custo Total do caminho mais rapido é {custoTotal}.")


    print('\n'.join([''.join(["{:" ">4}".format(item) for item in row])
                     for row in path]))

