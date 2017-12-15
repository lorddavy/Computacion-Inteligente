# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        for i in range(0, self.iterations):         #Recorrem totes les iteracions
            nextValues = util.Counter()                 #Inicialitzem un Counter auxiliar on guardarem els qValues que anem trobant
            for state in self.mdp.getStates():              #Recorrem tots els estats
                if not self.mdp.isTerminal(state):                  #Si l'estat no es terminal podem buscar les accions i el qValue
                    maxValue = -float('inf')                                #Inicialitzem maxValue a -infinit. maxValue sera el qValue mes gran que trobem en cada estat
                    for action in self.mdp.getPossibleActions(state):           #Recorrem totes les accions
                        qValue = self.getQValue(state, action)              #Computem el qValue
                        maxValue = max(qValue, maxValue)                #Actualitzem el maxValue
                    nextValues[state] = maxValue                    #Actualitzem el valor de nextValues en aquest estat
            self.values = nextValues.copy()                     #Al final de l'iteracio actualitzem self.values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"

        transitions = self.mdp.getTransitionStatesAndProbs(state, action)       #Per totes les transicions apliquem l'equacio de Belman (una mica modificada)
        summation = [prob * (self.mdp.getReward(state, action, succesor) + self.discount * self.getValue(succesor)) for succesor, prob in transitions]
        return sum(summation)       #Retornem la suma de totes les transicions


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"

        bestAction = None                       #Inicialitzem la millor accio possible i el qValue maxim
        maxValue = -float('inf')
        if self.mdp.isTerminal(state):          # Si l'estat es terminal, no podem aplicar cap accio
            return None
        for action in self.mdp.getPossibleActions(state):           # Per totes les accions
            qValue = self.getQValue(state, action)              # Calculem el seu qValue
            if qValue > maxValue:                       # Si el qValue d'una accio es superior al maxim, l'accio sera millor que la que teniem guardada
                maxValue = qValue                       # Actualitzar el maxim
                bestAction = action                     # Actualitzem la millor accio possible
        return bestAction                           # Retornem la millor accio possible


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
