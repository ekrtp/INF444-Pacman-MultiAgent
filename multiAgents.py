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
        "*** YOUR CODE HERE ***"

        def expectimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state), None

            numAgents = state.getNumAgents()

            if agentIndex == 0:  # Pacman - MAX düğümü
                bestValue = float('-inf')
                bestAction = None
                for action in state.getLegalActions(agentIndex):
                    successor = state.generateSuccessor(agentIndex, action)
                    nextAgent = (agentIndex + 1) % numAgents
                    nextDepth = depth + 1 if nextAgent == 0 else depth
                    value, _ = expectimax(successor, nextDepth, nextAgent)
                    if value > bestValue:
                        bestValue = value
                        bestAction = action
                return bestValue, bestAction

            else:  # Ghost - CHANCE düğümü
                totalValue = 0
                actions = state.getLegalActions(agentIndex)
                prob = 1.0 / len(actions) if actions else 0

                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    nextAgent = (agentIndex + 1) % numAgents
                    nextDepth = depth + 1 if nextAgent == 0 else depth
                    value, _ = expectimax(successor, nextDepth, nextAgent)
                    totalValue += prob * value

                return totalValue, None

        # Kök düğüm için aksiyonu al
        _, bestAction = expectimax(gameState, 0, 0)
        return bestAction


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:
    Bu değerlendirme fonksiyonu aşağıdaki faktörleri dikkate alır:
    1. Mevcut skor
    2. Kalan yiyecek sayısı (az olması iyi)
    3. En yakın yiyeceğe olan mesafe
    4. Tüm yiyeceklere olan ortalama mesafe
    5. Hayaletlere olan mesafe (korkmuş/korkmamış duruma göre)
    6. Kapsül sayısı (az olması iyi)
    7. Korkmuş hayaletlere yakınlık (avlanma fırsatı)
    """
    "*** YOUR CODE HERE ***"
    # Temel bilgileri al
    pacmanPos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    foodList = foodGrid.asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    # Temel skor
    score = currentGameState.getScore()

    # 1. Kalan yiyecek sayısı - az olması iyi
    foodCount = len(foodList)
    score -= foodCount * 10

    # 2. En yakın yiyeceğe olan mesafe - az olması iyi
    if foodCount > 0:
        minFoodDist = min([manhattanDistance(pacmanPos, food) for food in foodList])
        score += 15.0 / (minFoodDist + 1)

    # 3. Tüm yiyeceklere olan ortalama mesafe - az olması iyi
    if foodCount > 0:
        avgFoodDist = sum([manhattanDistance(pacmanPos, food) for food in foodList]) / foodCount
        score += 10.0 / (avgFoodDist + 1)

    # 4. Hayaletlere olan mesafe
    for i, ghostState in enumerate(ghostStates):
        ghostPos = ghostState.getPosition()
        dist = manhattanDistance(pacmanPos, ghostPos)
        scaredTimer = ghostState.scaredTimer

        if scaredTimer > 0:  # Korkmuş hayalet
            if dist < scaredTimer:  # Yakalanabilir mesafede
                score += 200.0 / (dist + 1)
            else:
                score += 50.0 / (dist + 1)  # Uzaktaysa normal davran
        else:  # Normal hayalet
            if dist == 0:
                score -= 10000  # Çarpışma - büyük ceza
            elif dist < 3:
                score -= 100.0 / (dist + 1)  # Çok yakınsa ceza
            else:
                score += 5.0 / (dist + 1)  # Uzaktaysa küçük ödül

    # 5. Kapsül sayısı - az olması iyi
    capsuleCount = len(capsules)
    score -= capsuleCount * 20

    # 6. En yakın kapsüle olan mesafe (eğer varsa)
    if capsuleCount > 0:
        minCapsuleDist = min([manhattanDistance(pacmanPos, capsule) for capsule in capsules])
        score += 30.0 / (minCapsuleDist + 1)

    # 7. Yiyeceklerin yoğunluğu (kümelenme)
    if foodCount > 1:
        # Yiyecekler arasındaki ortalama mesafe
        if foodCount > 1:
            foodDists = []
            for i in range(foodCount):
                for j in range(i + 1, foodCount):
                    foodDists.append(manhattanDistance(foodList[i], foodList[j]))
            if foodDists:
                avgFoodToFoodDist = sum(foodDists) / len(foodDists)
                score += 5.0 / (avgFoodToFoodDist + 1)  # Kümelenmiş yiyecekler iyi

    # 8. Oyun durumu bonusları
    if currentGameState.isWin():
        score += 10000
    if currentGameState.isLose():
        score -= 10000

    return score


# Abbreviation
better = betterEvaluationFunction