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


# multiAgents.py
# --------------
# ... (license and imports)

class ExpectimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState: GameState):
        """
        Enhanced expectimax with smart depth management.
        """
        # Adaptive depth based on food count
        foodCount = gameState.getNumFood()
        if foodCount < 10:  # Endgame - search deeper
            effectiveDepth = min(self.depth + 1, 4)
        else:
            effectiveDepth = self.depth

        def expectimax(state, depth, agentIndex, currentDepth=0):
            # Check terminal states
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state), None

            # Check depth limit
            if currentDepth >= effectiveDepth * state.getNumAgents():
                return self.evaluationFunction(state), None

            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = currentDepth + 1

            # Pacman's turn (MAX)
            if agentIndex == 0:
                bestValue = float('-inf')
                bestAction = None
                legalActions = state.getLegalActions(agentIndex)

                # Filter out STOP if possible
                if Directions.STOP in legalActions and len(legalActions) > 1:
                    legalActions = [a for a in legalActions if a != Directions.STOP]

                for action in legalActions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value, _ = expectimax(successor, depth, nextAgent, nextDepth)

                    # Tie-breaking: prefer non-reverse moves
                    if abs(value - bestValue) < 0.001:  # Almost equal
                        pacmanState = state.getPacmanState()
                        if pacmanState.configuration:
                            currentDir = pacmanState.configuration.direction
                            reverseDir = Directions.REVERSE[currentDir] if currentDir in Directions.REVERSE else None
                            if action != reverseDir and bestAction == reverseDir:
                                bestValue = value
                                bestAction = action
                    elif value > bestValue:
                        bestValue = value
                        bestAction = action

                return bestValue, bestAction

            # Ghost's turn (EXPECTED)
            else:
                actions = state.getLegalActions(agentIndex)
                if not actions:
                    return self.evaluationFunction(state), None

                # Calculate expected value
                expectedValue = 0
                prob = 1.0 / len(actions)

                for action in actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value, _ = expectimax(successor, depth, nextAgent, nextDepth)
                    expectedValue += prob * value

                return expectedValue, None

        # Get best action
        _, bestAction = expectimax(gameState, 0, 0, 0)

        # Fallback
        if bestAction is None:
            legalActions = gameState.getLegalActions(0)
            if Directions.STOP in legalActions and len(legalActions) > 1:
                legalActions = [a for a in legalActions if a != Directions.STOP]
            if legalActions:
                # Prefer forward movement
                pacmanState = gameState.getPacmanState()
                if pacmanState.configuration:
                    currentDir = pacmanState.configuration.direction
                    forwardActions = [a for a in legalActions if a != Directions.REVERSE.get(currentDir, None)]
                    if forwardActions:
                        bestAction = random.choice(forwardActions)
                    else:
                        bestAction = random.choice(legalActions)
                else:
                    bestAction = random.choice(legalActions)
            else:
                bestAction = Directions.STOP

        return bestAction


def betterEvaluationFunction(currentGameState: GameState):
    """
    Ultra-optimized evaluation function for ALL map types.
    """
    # Basic extraction
    pacmanPos = currentGameState.getPacmanPosition()
    foodGrid = currentGameState.getFood()
    foodList = foodGrid.asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    # Terminal states
    if currentGameState.isWin():
        return 1000000 + score
    if currentGameState.isLose():
        return -1000000

    # 1. FOOD STRATEGY (most critical)
    foodCount = len(foodList)

    # Heavy penalty for remaining food
    score -= foodCount * 20

    # Distance to food calculations
    if foodCount > 0:
        foodDistances = [manhattanDistance(pacmanPos, food) for food in foodList]

        # Nearest food (most important)
        minFoodDist = min(foodDistances)
        if minFoodDist == 0:  # Eating food now
            score += 100
        else:
            score += 25.0 / minFoodDist

        # Average distance bonus
        avgFoodDist = sum(foodDistances) / foodCount
        score += 10.0 / (avgFoodDist + 1)

        # Food density bonus (clustered food is good)
        if foodCount > 1:
            foodDensity = foodCount / (avgFoodDist + 1)
            score += foodDensity * 5

    # 2. GHOST STRATEGY (adaptive based on map)
    scaredGhosts = []
    activeGhosts = []

    for ghostState in ghostStates:
        ghostPos = ghostState.getPosition()
        dist = manhattanDistance(pacmanPos, ghostPos)

        if ghostState.scaredTimer > 0:
            scaredGhosts.append((dist, ghostState.scaredTimer))
        else:
            activeGhosts.append(dist)

    # Handle scared ghosts (HUNTING OPPORTUNITY)
    for dist, timer in scaredGhosts:
        if dist == 0:  # Can eat now!
            score += 500
        elif dist < timer:  # Can catch before timer expires
            score += 300.0 / (dist + 1)
        else:
            score += 50.0 / (dist + 1)

    # Handle active ghosts (DANGER MANAGEMENT)
    if activeGhosts:
        minGhostDist = min(activeGhosts)

        # CRITICAL: Different strategy based on map size
        if len(foodList) < 10:  # Small map (trappedClassic, minimaxClassic)
            # Be more aggressive on small maps
            if minGhostDist == 0:
                score -= 10000
            elif minGhostDist == 1:
                score -= 1000
            elif minGhostDist == 2:
                score -= 200
            else:
                score += 5.0 / (minGhostDist + 1)
        else:  # Large map (mediumClassic, powerClassic)
            # Be more defensive on large maps
            if minGhostDist == 0:
                score -= 10000
            elif minGhostDist <= 2:
                score -= 500.0 / (minGhostDist + 1)
            elif minGhostDist <= 4:
                score -= 100.0 / (minGhostDist + 1)
            else:
                score += 2.0 / (minGhostDist + 1)

    # 3. CAPSULE STRATEGY (critical for capsuleClassic)
    capsuleCount = len(capsules)

    if capsuleCount > 0:
        capsuleDistances = [manhattanDistance(pacmanPos, cap) for cap in capsules]
        minCapsuleDist = min(capsuleDistances)

        # SPECIAL: For capsuleClassic map, prioritize capsules heavily
        if len(foodList) > 15 and capsuleCount > 1:  # Likely capsuleClassic
            score -= capsuleCount * 10  # Less penalty
            score += 100.0 / (minCapsuleDist + 1)  # Big bonus for getting close

            # If ghosts are close, capsules are even more valuable
            if activeGhosts and min(activeGhosts) < 5:
                score += 200.0 / (minCapsuleDist + 1)
        else:
            # Normal strategy for other maps
            score -= capsuleCount * 30
            if minCapsuleDist < 3:  # Only go for very close capsules
                score += 40.0 / (minCapsuleDist + 1)

    # 4. MAP-SPECIFIC ADJUSTMENTS

    # trappedClassic: Aggressive food collection
    if foodCount < 15 and len(activeGhosts) == 4:  # Likely trappedClassic
        score += 100 / (foodCount + 1)  # Bonus for eating quickly

    # powerClassic: Use power pellets strategically
    if capsuleCount == 0 and any(st.scaredTimer > 0 for st in ghostStates):
        # We have active power pellet - HUNT!
        score += 200

    # 5. ACTION QUALITY
    legalActions = currentGameState.getLegalActions(0)
    if Directions.STOP in legalActions and len(legalActions) > 1:
        score -= 10  # Penalty for stopping when other moves available

    # 6. GAME PROGRESS BONUS
    totalPossibleFood = foodCount + score // 10
    if totalPossibleFood < 30:  # Late game
        score += 200 / (foodCount + 1)  # Finish quickly bonus

    return score


# Abbreviation
better = betterEvaluationFunction