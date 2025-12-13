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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
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
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState: GameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
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
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        def value(state, agentIndex, depth):
            # Cut off on win/lose
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)

            legal = state.getLegalActions(agentIndex)
            if not legal:
                return self.evaluationFunction(state)

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            
            # Depth represents how many times Pacman has moved in this branch
            # When we cycle back to Pacman (nextAgent == 0), we increment depth
            if nextAgent == 0:
                nextDepth = depth + 1
            else:
                nextDepth = depth

            # If we're at a Pacman node and we've reached the target depth, evaluate successors
            if agentIndex == 0 and depth == self.depth:
                return max(self.evaluationFunction(state.generateSuccessor(agentIndex, action))
                           for action in legal)

            if agentIndex == 0:
                # Pacman node: maximize expected value
                return max(value(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
                           for action in legal)
            else:
                # Ghost node: uniform expectation over legal actions
                return sum(value(state.generateSuccessor(agentIndex, action), nextAgent, nextDepth)
                           for action in legal) / float(len(legal))

        legalActions = gameState.getLegalActions(0)
        if not legalActions:
            return Directions.STOP

        # Ban STOP unless it is the only legal action
        filteredActions = [a for a in legalActions if a != Directions.STOP]
        if filteredActions:
            legalActions = filteredActions

        # Evaluate each action from the root; random tie-breaking among best
        scores = []
        for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            # Start depth at 0: depth represents how many times Pacman has moved in this branch
            # We've generated one successor, now look ahead self.depth more Pacman moves
            scores.append((value(successor, 1, 0), action))

        if not scores:
            return Directions.STOP

        bestScore = max(score for score, _ in scores)
        bestActions = [action for score, action in scores if score == bestScore]
        return random.choice(bestActions)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # Fast heuristics only (Manhattan-based). Weighted linear combination of:
    #   - base game score
    #   - food proximity + remaining food penalty
    #   - capsule proximity + remaining capsule penalty
    #   - scared ghost chasing bonus (when reachable in time)
    #   - active ghost safety penalty with a hard kill-avoidance gate
    if currentGameState.isWin():
        return float('inf')
    if currentGameState.isLose():
        return float('-inf')

    epsilon = 1e-3  # avoid divide-by-zero

    pac_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghost_states = currentGameState.getGhostStates()

    score = float(currentGameState.getScore())

    # Food: get closer to the nearest pellet and clear the board quickly
    if food_list:
        closest_food = min(manhattanDistance(pac_pos, food) for food in food_list)
        score += 9.0 / (closest_food + 1.0)  # strong pull toward nearby food
        score -= 4.5 * len(food_list)        # discourage leaving pellets behind

    # Capsules: high value when available to flip ghost danger -> opportunity
    if capsules:
        closest_cap = min(manhattanDistance(pac_pos, cap) for cap in capsules)
        score += 12.0 / (closest_cap + 1.0)
        score -= 8.0 * len(capsules)

    # Ghost handling
    active_penalty = 0.0
    scared_bonus = 0.0

    for ghost in ghost_states:
        gpos = ghost.getPosition()
        dist = float(manhattanDistance(pac_pos, gpos))
        scared_time = ghost.scaredTimer

        if scared_time > 0:
            if dist < 1.0:
                # Can eat immediately; big reward that scales with timer
                scared_bonus += 60.0 + 3.0 * scared_time
            else:
                # Only reward chasing if we can realistically reach before timer ends
                reachable_factor = max(scared_time - dist, 0.0)
                scared_bonus += (25.0 * reachable_factor) / (dist + epsilon)
        else:
            # Hard avoidance: being adjacent (or on) an active ghost is deadly
            if dist < 2.0:
                return -1e9
            # Softer penalty encouraging a safety buffer
            active_penalty += 18.0 / (dist + 1.0)

    score += scared_bonus
    score -= active_penalty

    return score

# Abbreviation
better = betterEvaluationFunction
