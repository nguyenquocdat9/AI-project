# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # If agent takes this action there is a ghost that will eat the pacman,
        # so pacman should run and that's why we give the lowest score.
        for gp in newGhostStates:
            if manhattanDistance(newPos, gp.getPosition()) < 2:
                return -float('inf')

        # By taking this action, no ghost will eat our pacman.
        # If after doing this action the number of dots decreases,
        # it implies by taking this action pacman will eat a dot.
        # So do it and eat food!
        currentFoodNum = len(currentGameState.getFood().asList())
        newFoodList = newFood.asList()
        newFoodNum = len(newFoodList)
        if newFoodNum < currentFoodNum:
            return float('inf')

        # Pacman could not eat food yet! So he should try to find the closest one.
        # Find the closest food
        minFoodDist = float('inf')
        for food in newFoodList:
            foodDist = manhattanDistance(newPos, food)
            if foodDist < minFoodDist:
                minFoodDist = foodDist
        # The lower distance is, the higher the score will be
        return 1.0 / minFoodDist


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    """
    Finds best action by iterating and using minimax algorithm
    """
    def minimax(self, gameState, depth, agent):

        # If Pacman wins or loses, game is finished ,
        # Also when maximum depth is reached means recursion should be stopped
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return [self.evaluationFunction(gameState)]

        # One of the agents is pacman, so number of ghosts is all agents - pacman (1)
        ghostsNum = gameState.getNumAgents() - 1
        # Because agent increases each time
        agent = agent % (ghostsNum + 1)

        # It's one of the ghosts' turn and min value should be selected.
        if agent > 0:
            # If it's the final ghost, so depth should be decreased
            if agent == ghostsNum:
                depth -= 1

            minValue = float("inf")
            for action in gameState.getLegalActions(agent):
                successorGameState = gameState.generateSuccessor(agent, action)
                # Index 0 is the previous minValue and index 1 is the previous best Action
                # We should check next agent as next node
                newMinValue = self.minimax(successorGameState, depth, agent + 1)[0]

                # Update the minValue
                if newMinValue < minValue:
                    bestAction = action
                    minValue = newMinValue

            return minValue, bestAction

        # It's pacman's turn and max value should be selected.
        maxValue = -float("inf")
        for action in gameState.getLegalActions(agent):
            successorGameState = gameState.generateSuccessor(agent, action)
            # We should check next agent as next node
            newMaxValue = self.minimax(successorGameState, depth, agent + 1)[0]

            # Update the maxValue
            if newMaxValue > maxValue:
                maxValue = newMaxValue
                bestAction = action

        return maxValue, bestAction

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        Here are some method calls that might be useful when implementing minimax.
        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1
        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action
        gameState.getNumAgents():
        Returns the total number of agents in the game
        gameState.isWin():
        Returns whether or not the game state is a winning state
        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimax(gameState, self.depth, self.index)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    """
    Finds best action by iterating and using alpha beta algorithm
    """
    def alphaBeta(self, alfa, beta, gameState, depth, agent):

        # If Pacman wins or loses, game is finished ,
        # Also when maximum depth is reached means recursion should be stopped
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return [self.evaluationFunction(gameState)]

        # One of the agents is pacman, so number of ghosts is all agents - pacman (1)
        ghostsNum = gameState.getNumAgents() - 1
        # Because agent increases each time
        agent = agent % (ghostsNum + 1)

        # It's one of the ghosts' turn and min value should be selected.
        if agent > 0:
            # If it's the final ghost, so depth should be decreased
            if agent == ghostsNum:
                depth -= 1

            minValue = float("inf")
            for action in gameState.getLegalActions(agent):
                successorGameState = gameState.generateSuccessor(agent, action)
                # Index 0 is the previous minValue and index 1 is the previous best Action
                # We should check next agent as next node
                newMinValue = self.alphaBeta(alfa, beta, successorGameState, depth, agent + 1)[0]

                # Update the minValue and beta in case needed
                if newMinValue < minValue:
                    bestAction = action
                    minValue = newMinValue

                if minValue < alfa:
                    return minValue, bestAction

                beta = min(beta, minValue)

            return minValue, bestAction

        # It's pacman's turn and max value should be selected.
        maxValue = -float("inf")
        for action in gameState.getLegalActions(agent):
            successorGameState = gameState.generateSuccessor(agent, action)
            # We should check next agent as next node
            newMaxValue = self.alphaBeta(alfa, beta, successorGameState, depth, agent + 1)[0]

            # Update the maxValue and alfa in case needed
            if newMaxValue > maxValue:
                bestAction = action
                maxValue = newMaxValue

            if maxValue > beta:
                return maxValue, bestAction

            alfa = max(alfa, maxValue)

        return maxValue, bestAction

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alfa = -float("inf")
        beta = float("inf")
        return self.alphaBeta(alfa, beta, gameState, self.depth, self.index)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    """
    Finds best action by iterating and using expectimax algorithm
    """
    def expectimax(self, gameState, depth, agent):

        # If Pacman wins or loses, game is finished ,
        # Also when maximum depth is reached means recursion should be stopped
        if depth == 0 or gameState.isLose() or gameState.isWin():
            return [self.evaluationFunction(gameState)]

        # One of the agents is pacman, so number of ghosts is all agents - pacman (1)
        ghostsNum = gameState.getNumAgents() - 1
        # Because agent increases each time
        agent = agent % (ghostsNum + 1)

        # It's one of the ghosts' turn and min value should be selected.
        if agent > 0:
            # If it's the final ghost, so depth should be decreased
            if agent == ghostsNum:
                depth -= 1

            minValues = 0
            for action in gameState.getLegalActions(agent):
                successorGameState = gameState.generateSuccessor(agent, action)
                # Index 0 is the previous minValue and index 1 is the previous best Action
                # We should check next agent as next node and sum all nodes' values
                # in order to take the average of all available utilities
                minValues += self.expectimax(successorGameState, depth, agent + 1)[0]

            # Calculate the average of all available utilities
            minValuesAvg = minValues / len(gameState.getLegalActions(agent))
            return minValuesAvg, action

        # It's pacman's turn and max value should be selected.
        maxValue = -float("inf")
        for action in gameState.getLegalActions(agent):
            successorGameState = gameState.generateSuccessor(agent, action)
            # We should check next agent as next node
            newMaxValue = self.expectimax(successorGameState, depth, agent + 1)[0]

            # Update the maxValue
            if newMaxValue > maxValue:
                bestAction = action
                maxValue = newMaxValue

        return maxValue, bestAction

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimax(gameState, self.depth, self.index)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      DESCRIPTION:
      The following features are considered and combined:
        - Compute the maze distance to the closest food dot
        - Compute the maze distance to the closest capsule
        - If the ghost is scared and close, eat it
        - If the ghost is not scared and close, run away
        - Take into account score (the longer the game is, the lower the score will be)
    """
    "*** YOUR CODE HERE ***"
    # Same evaluation function as evaluationFunction
    # If ghost is scared pacman runs to the ghost and eats the ghost
    newFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodList = newFood.asList()

    # There is no food, so the game is finished and the score will not chang
    if not foodList:
        return currentGameState.getScore()

    # Find the closest and the furthest food
    minFoodDist = float('inf')
    maxFoodDist = -float('inf')
    for food in foodList:
        foodDist = manhattanDistance(newPos, food)
        if foodDist < minFoodDist:
            minFoodDist = foodDist
        if foodDist > maxFoodDist:
            maxFoodDist = foodDist

    # Find the closest ghost from the Pacman
    minGhostDist = float('inf')
    for gp in newGhostStates:
        ghostDist = manhattanDistance(newPos, gp.getPosition())
        if ghostDist < minGhostDist:
            minGhostDist = ghostDist

    # Calculate new score based on states
    score = currentGameState.getScore()

    # If Ghost is Scared, pacman runs to the ghost to eat that ghost
    if newScaredTimes[0] > 0:
        score += - minGhostDist - minFoodDist

    # If there is only one dot left then minFoodDist == maxFoodDist
    # If remained food is before the nearest ghost, the score increases,
    # otherwise pacman should pass the post first and obviously the score decreases
    # The lower food distance is, the higher the score will be
    elif len(foodList) == 1:
        score += minGhostDist - minFoodDist

    # There is more than one dot the score will change based on
    # nearest and furthest distance between pacman and remained dots
    else:
        score += minGhostDist - (maxFoodDist + minFoodDist)

    return score



# Abbreviation
better = betterEvaluationFunction