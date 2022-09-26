import random


# networkx


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, other_node, weight=1):
        # permet de relier le node a un autre

        for i in self.edges:
            if i[0].name == other_node.name:
                raise ValueError("this edge already exist")
        self.edges.append((other_node, weight))

    def print_node(self):
        # permet de print une representation du graph

        print("[{}]: ".format(self.name), end="")
        for i in self.edges:
            print(str(i[0].name) + "({})".format(i[1]), end=" ")
        print()


class Graph:
    def __init__(self, directed=False):
        self.nodes = {}
        self.num_nodes = 0
        self.num_edges = 0
        self.is_directed = directed

    def add_node(self, new_node):
        # permet d'ajouter un node non existant dans le graph

        if not new_node in self.nodes:
            self.nodes[new_node] = Node(new_node)
            self.num_nodes += 1
        else:
            raise ValueError("this node already exist")

    def add_edge(self, node_1, node_2, weight=1):
        # permet d'ajouter un edge entre 2 node (cree les nodes s'ils n'existent pas)

        if node_1 != node_2:
            if not node_1 in self.nodes:
                self.add_node(node_1)
                self.num_nodes += 1

            if not node_2 in self.nodes:
                self.add_node(node_2)
                self.num_nodes += 1

            self.nodes[node_1].add_edge(self.nodes[node_2], weight)
            self.num_edges += 1

            if not self.is_directed:
                self.nodes[node_2].add_edge(self.nodes[node_1], weight)

    def represent_graph(self):
        # print une representation du graph sous forme de dictionnaire

        for node_name, node in self.nodes.items():
            node.print_node()

        if self.is_directed:
            print("directed", end=" ")
        else:
            print("undirected", end=" ")
        print("graph with {} nodes and {} edges".format(self.num_nodes, self.num_edges))

    def copy(self):
        # cree une copie du graph

        new_copy = Graph()
        for node_name, node in self.nodes.items():
            for node_neighbour in node.edges:
                try:
                    new_copy.add_edge(node.name, node_neighbour[0].name)
                except ValueError:
                    pass
        return new_copy

    def random_generation(self, nb_nodes, nb_edges):
        # genere un graph pseudo aleatoire (bibliotheque random) avec un nombre precis de node et de edge

        for i in range(nb_nodes):
            self.add_node(i)

        while self.num_edges < nb_edges:
            try:
                self.add_edge(random.choice(self.nodes).name, random.choice(self.nodes).name)
            except ValueError:
                pass

    def is_connex(self):
        # renvoit si le graph est connexe

        def rec_connex(curr_node, dico):
            dico[curr_node.name] = 1
            for neighbour in curr_node.edges:
                if dico[neighbour[0].name] == 0:
                    rec_connex(neighbour[0], dico)

        witness = {}
        for node in self.nodes:
            witness[node] = 0

        rec_connex(random.choice(self.nodes), witness)
        for node, value in witness.items():
            if value == 0:
                return False
        return True

    def is_dominating_set(self, solution):
        # renvoit si la solution est un dominating set du graph

        witness = {}
        result = True

        for node in self.nodes:
            witness[node] = 0

        for sol_node in solution:
            witness[sol_node] += 1
            for neighbour in self.nodes[sol_node].edges:
                witness[neighbour[0].name] += 1

        for node, num in witness.items():
            if num == 0:
                result = False
                break

        return result

    def find_dominating_set(self):
        # permet de trouver un dominating set relativement petit (on ajoute le node relié au plus de node,
        # on supprime ses voisins et on itére)

        # on cree une copie pour pouvoir modifier le dictionnaire de node a notre guise
        witness = self.copy().nodes
        solution = []

        # temps qu'il reste des noeuds qui reste a traiter
        while len(witness) > 0:
            node_index = (Node("Null"), -1)

            # trouve le node qui est relier au plus de node non traité
            for node_name, node in witness.items():
                if len(node.edges) > node_index[1]:
                    node_index = (node, len(node.edges))

            # on print des logs
            if node_index[1] > 0:
                print("On supprime le node {} car il est celui relie au plus de node ({})".format(node_index[0].name, node_index[1]))
            else:
                print("On supprime le node {} car il n'est plus relie a auncun autre node".format(node_index[0].name))

            # efface les nodes traités de la liste de voisinnage puis du dictionnaire temoin
            while len(node_index[0].edges) > 0:
                node_neighbour_1 = node_index[0].edges[0][0]
                while len(node_neighbour_1.edges) > 0:
                    node_neighbour_2 = node_neighbour_1.edges[0][0]
                    for i in range(len(node_neighbour_2.edges)):
                        if node_neighbour_2.edges[i][0].name == node_neighbour_1.name:
                            node_neighbour_2.edges.pop(i)
                            break

                    node_neighbour_1.edges.pop(0)
                witness.pop(node_neighbour_1.name)

            # ajoute le node au dominating set
            solution.append(node_index[0].name)

            # supprime le node ajouté du dictionnaire temoin
            witness.pop(node_index[0].name)

        return solution


if __name__ == '__main__':
    graph = Graph()
    graph.random_generation(1000, 15000)
    dominating_set = graph.find_dominating_set()
    print("Un dominating set a {} nodes a ete trouve:".format(len(dominating_set)), dominating_set)
    print("Le dominating set est correct:", graph.is_dominating_set(dominating_set))
