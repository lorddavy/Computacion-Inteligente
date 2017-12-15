# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node:
    '*** OWN CLASS ***'
    def __init__(self, n, p, c, f):
        self.name = n
        self.path = p
        self.cost = c
        self.father = f

    def __repr__(self):
        return "Node()"

    def __str__(self):
        if self.father is not None:
            return "%s %s %s %s" % (self.name, self.path, self.cost, self.father.name)
        else:
            return "%s %s %s None" % (self.name, self.path, self.cost)
         #return "From str method of Test: a is %s, b is %s" % (self.a, self.b)

def nodeIsClosed(n, closedNodes):
    '*** OWN FUNCTION ***'
    for c in closedNodes:
        if (n.name == c.name):
            return True
    return False

def findPath(n):
    '*** OWN FUNCTION ***'
    path = list()
    while n.path != '':
        path.insert(0, n.path)
        n = n.father
    return path

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    #Creamos las estructuras de datos necesarias (stack y set)
    openNodes = util.Stack()
    closedNodes = set([])

    #Guardamos el nodo inicial
    node = Node(problem.getStartState(), '', 0, None)

    #Metemos el nodo en la pila
    openNodes.push(node)

    #Iteramos para cada nodo de la pila
    while True:
        if openNodes.isEmpty():
            break #ERROR: throw exception
        else :
            #Sacamos el nodo de arriba de la pila
            node = openNodes.pop()
            if problem.isGoalState(node.name):
                break
            else: #Expandimos los nodos sucesores del nodo n si no estan en closed
                for successor in problem.getSuccessors(node.name):
                    n, p, c = successor
                    succNode = Node(n, p, c, node)
                    if nodeIsClosed(succNode, closedNodes) is False:
                        #Metemos al sucesor en la pila
                        openNodes.push(succNode)
                #Metemos el nodo n en closed
                closedNodes.add(node)

    #Devolvemos el camino al Goal
    return findPath(node)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #Creamos las estructuras de datos necesarias (queue y set)
    openNodes = util.Queue()
    closedNodes = set([])

    #Guardamos el nodo inicial
    node = Node(problem.getStartState(), '', 0, None)

    #Metemos el nodo en la cola
    openNodes.push(node)

    #Iteramos para cada nodo de la pila
    while True:
        if openNodes.isEmpty():
            break #ERROR: throw exception
        else :
            #Sacamos el nodo de arriba de la pila
            node = openNodes.pop()
            if problem.isGoalState(node.name):
                break
            else: #Expandimos los nodos sucesores del nodo n si no estan en closed
                if nodeIsClosed(node, closedNodes) is False:
                    for successor in problem.getSuccessors(node.name):
                        n, p, c = successor
                        succNode = Node(n, p, c, node)
                        if nodeIsClosed(succNode, closedNodes) is False:
                            #Metemos al sucesor en la cola
                            openNodes.push(succNode)
                    #Metemos el nodo n en closed
                    closedNodes.add(node)

    #Devolvemos el camino al Goal
    return findPath(node)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #Creamos las estructuras de datos necesarias (priority queue y set)
    openNodes = util.PriorityQueue()
    closedNodes = set([])

    #Guardamos el nodo inicial
    node = Node(problem.getStartState(), '', 0, None)

    #Calculamos funcion heuristica y el coste acumulado para sacar la funcion de evaluacion del nodo inicial
    fn = problem.getCostOfActions(node.path) + nullHeuristic(node.name, problem);

    #Lo metemos en la cola con su funcion de evaluacion como prioridad
    openNodes.push(node, fn)

    #Iteramos para cada nodo
    while True:
        if openNodes.isEmpty():
            break #ERROR: throw exception
        else :
            #sacamos el nodo de arriba de la cola
            node = openNodes.pop()
            if problem.isGoalState(node.name):  #Comprobamos si el nodo es Goal. Si lo es terminamos.
                break
            else: #Expandimos los nodos sucesores del nodo si no estan en closed
                if nodeIsClosed(node, closedNodes) is False:
                    for successor in problem.getSuccessors(node.name):
                        n, p, c = successor
                        succNode = Node(n, p, c, node)
                        if nodeIsClosed(succNode, closedNodes) is False:
                            fn = problem.getCostOfActions(findPath(succNode)) + nullHeuristic(succNode.name, problem);
                            openNodes.push(succNode, fn)
                    #Metemos el nodo en closed
                    closedNodes.add(node)

    #Devolvemos el camino al Goal
    return findPath(node)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #Creamos las estructuras de datos necesarias (priority queue y set)
    openNodes = util.PriorityQueue()
    closedNodes = set([])

    #Guardamos el nodo inicial
    node = Node(problem.getStartState(), '', 0, None)

    #Calculamos funcion heuristica y el coste acumulado para sacar la funcion de evaluacion del nodo inicial
    fn = problem.getCostOfActions(node.path) + heuristic(node.name, problem);

    #Lo metemos en la cola con su funcion de evaluacion como prioridad
    openNodes.push(node, fn)

    #Iteramos para cada nodo
    while True:
        if openNodes.isEmpty():
            break #ERROR: throw exception
        else :
            #sacamos el nodo de arriba de la cola
            node = openNodes.pop()
            if problem.isGoalState(node.name):  #Comprobamos si el nodo es Goal. Si lo es terminamos.
                break
            else: #Expandimos los nodos sucesores del nodo si no estan en closed
                if nodeIsClosed(node, closedNodes) is False:
                    for successor in problem.getSuccessors(node.name):
                        n, p, c = successor
                        succNode = Node(n, p, c, node)
                        if nodeIsClosed(succNode, closedNodes) is False:
                            fn = problem.getCostOfActions(findPath(succNode)) + heuristic(succNode.name, problem);
                            openNodes.push(succNode, fn)
                    #Metemos el nodo en closed
                    closedNodes.add(node)

    #Devolvemos el camino al Goal
    return findPath(node)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
