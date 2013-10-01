import random
import math

# Class that abstracts the notion of the board
class Board:
   def __init__(self):
      self.tiles = [[], [], []]
      self.emptyTile = -1                 # Position of the empty tile
      self.possibleMoves = 0              # All possible moves, given the 
                                          #  position of the empty tile
      self.parent = None                  # The parent board from which this
                                          #  board was derived through a single
                                          #  move.
      self.depth = 0                      # Depth of this board from the root
      self.signature = ""                 # Signature for the board, unique to
                                          #  a particular configuration of 
                                          #  tiles.
   
   # Returns true if the boards are equal (with the same comfiguration)   
   def __eq__(self, other):
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         if self.tiles[i][j] != other.tiles[i][j]:
           return False
      return True
   
   # Returns a hash value for the board (unique to configirations)
   def __hash__(self):
      return hash(self.signature)
   
   # Returns a printable format of the board
   def __str__(self):
      string = ""
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         string += str(self.tiles[i][j]) + " "
         if (k + 1) % 3 == 0:
            string += "\n"
      return string
   
   # Compute the signature of the board, unique to its configuration
   def computeSignature(self):
      self.signature = ""
      for row in self.tiles:
         for tile in row:
            self.signature += `tile`
   
   # Return the signature of the board
   def getSignature(self):
      return self.signature
   
   # Move a the emtpy tile in the direction indicated by moveCode
   # moveCode = 1 --> Move the empty tile UP
   # moveCode = 2 --> Move the empty tile RIGHT
   # moveCode = 4 --> Move the empty tile DOWN
   # moveCode = 8 --> Move the empty tile LEFT
   def moveTile(self, moveCode):
      
      i = self.emptyTile / 3 # Board size = 3
      j = self.emptyTile % 3 # Board size = 3
      #print str(i) + " " + str(j) + " " + str(moveCode) + " " + str(self.possibleMoves)
      if moveCode == 1:                # Move the empty tile UP
         self.tiles[i][j] = self.tiles[i-1][j]
         self.tiles[i-1][j] = 0
         self.emptyTile -= 3           # Board size = 3
         self.possibleMoves |= 4
         if i - 1 == 0:                # If the empty tile is now at the 
                                       #  topmost row
            self.possibleMoves &= (~1)
      
      elif moveCode == 2:              # Move the empty tile RIGHT
         self.tiles[i][j] = self.tiles[i][j+1]
         self.tiles[i][j+1] = 0
         self.emptyTile += 1
         self.possibleMoves |= 8
         if j + 1 == 3 - 1:            # Board size = 3   
                                       # If the empty tile is now at the 
                                       #  rightmost column
            self.possibleMoves &= (~2)
      
      elif moveCode == 4:              # Move the empty tile DOWN
         self.tiles[i][j] = self.tiles[i+1][j]
         self.tiles[i+1][j] = 0
         self.emptyTile += 3           # Board size = 3
         self.possibleMoves |= 1
         if i + 1 == 3 - 1:            # Board size = 3; i + 2 == 3
                                       # If the empty tile is now at the 
                                       #  bottommost row
            self.possibleMoves &= (~4)
      
      elif moveCode == 8:              # Move the empty tile LEFT
         self.tiles[i][j] = self.tiles[i][j-1]
         self.tiles[i][j-1] = 0
         self.emptyTile -= 1
         self.possibleMoves |= 2
         if j - 1 == 0:                # Board size = 3; i + 2 == 3
                                       # If the empty tile is now at the 
                                       #  leftmost column
            self.possibleMoves &= (~8)
   
   # Scramble the board configuration for 'count' times, by making random movements
   # Used for generating random starting board configuration
   def scrambleBoard(self, count):
      while count:
         numMoves = 4
         if self.possibleMoves != 8|4|2|1:
            numMoves -= 1
            if     self.possibleMoves != 8|4|2 and self.possibleMoves != 8|4|1 
               and self.possibleMoves != 8|2|1 and self.possibleMoves != 4|2|1:
               numMoves -= 1
         rand = random.randint(1, numMoves)
         move = 1
         while rand:
            if self.possibleMoves & move:
               rand -= 1
            move <<= 1
         move >>= 1
         self.moveTile(move)
         count -= 1

   # Generate a board with a default configuration and then scramble it
   # by making 'scrambleCount' random moves
   # The default configuration would be:
   # 0 1 2
   # 3 4 5
   # 6 7 8
   def generateBoard(self, scrambleCount):
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         self.tiles[i].append(3*i + j)
      self.emptyTile = 0
      self.possibleMoves = 2|4            # Can move right or down from the
                                          #  top-left corner of the board
      if scrambleCount:
         self.scrambleBoard(scrambleCount)

   # Construct a board from the 'model' configuration
   def constructBoard(self, model):
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         self.tiles[i].append(model[i][j])
         #print "<" + str(self.tiles[i][j]) + ", " + str(model[i][j]) + ">"
         if model[i][j] == 0:
            self.emptyTile = k            # Board size = 3
            self.possibleMoves = 0
            if i != 0:
               self.possibleMoves |= 1
            if j != 2:                    # Board size = 3;
               self.possibleMoves |= 2
            if i != 2:                    # Board size = 3
               self.possibleMoves |= 4
            if j != 0:
               self.possibleMoves |= 8

   # Make a copy of this board, with depth set to 0
   def copyBoard(self):
      copy = Board()
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         copy.tiles[i].append(self.tiles[i][j])
      copy.emptyTile = self.emptyTile
      copy.possibleMoves = self.possibleMoves
      copy.parent = None
      copy.depth = self.depth
      copy.signature = self.signature
      #print
      #print self.tiles
      #print copy.tiles
      return copy

   # Create a child of this board by making a valid move
   # moveCode should be a valid move in self.possibleMoves
   def spawnChild(self, moveCode):
      child = self.copyBoard()
      child.moveTile(moveCode)
      child.parent = self
      child.depth += 1
      return child

   # Print the path of derivation from the root board to this board
   def printPath(self):
      pathLength = 0
      stack = []
      while self: # TODO: Check for error
         stack.append(self)
         self = self.parent
         pathLength += 1
      while stack:
         self = stack.pop()
         print self
      return pathLength - 1 # TODO: Check if correct

# Class that abstracts the notion of the 8Puzzle
class EightPuzzle:
   def __init__(self, root, goal):
      self.root = root              # Root board
      self.goal = goal              # Goal board
      self.timeTaken = 0.0          # Time taken for the search
      self.numTestDone = 0          # Number of tests against the goal board 
                                    #  done.
      self.maxQueueLength = 0       # Max. queue length
      self.numDuplicatesFound = 0   # Number of duplicates detected and 
                                    #  eliminated
      self.maxDepthSearched = 0     # Max depth searched
      self.pathLength = 0           # Length of the path from root to goal 
                                    #  board
      self.goalFounded = False      # Whether the search for the goal was 
                                    #  successful or not
      self.goalDepth = -1           # Depth at which the goal was found
      self.reverseIndex = {}        # Dictionary (Reverse index) of where each
                                    #  number in the goal state is located.
      for k in range(9):
         i = k / 3
         j = k % 3
         self.reverseIndex[self.goal.tiles[i][j]] = k

   # Print the stats for the search run
   def printStats(self):
      print "Time taken              = "  + str(self.timeTaken)
      print "No. of tests done       = "  + str(self.numTestDone)
      print "Max. queue length       = "  + str(self.maxQueueLength)
      print "No. of duplicates found = "  + str(self.numDuplicatesFound)
      print "Max. depth searched     = "  + str(self.maxDepthSearched)
      print "Path length             = "  + str(self.pathLength)
      print "Goal found              = "  + str(self.goalFounded)
      print "Goal depth              = "  + str(self.goalDepth)

   # Breadth First Search
   def bfs(self):
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      # While there are candidate boards in the queue
      while queue:
         # Keep track of the max queue length
         if len(queue) > self.maxQueueLength:
            self.maxQueueLength = len(queue)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         candidate = queue.pop(0)
         self.numTestDone += 1
         visitedBoards.add(self)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            print "Goal found at a depth of " + str(candidate.depth)
            self.goalFounded = True
            self.pathLength = candidate.printPath()
            self.goalDepth = candidate.depth
            return True
         
         # Detect duplicates among children, increment count, add only 
         #  non-duplicates to queue
         moves = candidate.possibleMoves
         mask = 1
         while mask != 16:
            if moves & mask:
               child = candidate.spawnChild(mask)
               if child in visitedBoards:
                  self.numDuplicatesFound += 1
               else:
                  queue.append(child)
            mask <<= 1;
      return False

   # Depth First Search
   def dfs(self):
      stack = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      # While there are candidate boards in the stack
      while stack:
         # Keep track of the max stack length
         if len(stack) > self.maxQueueLength:
            self.maxQueueLength = len(stack)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         candidate = stack.pop()
         self.numTestDone += 1
         visitedBoards.add(self)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath()
            self.goalFounded = True
            self.goalDepth = candidate.depth
            return True
         
         # Detect duplicates among children, increment count, add only 
         #  non-duplicates to queue
         moves = candidate.possibleMoves
         mask = 1
         while mask != 16:
            if moves & mask:
               child = candidate.spawnChild(mask)
               if child in visitedBoards:
                  self.numDuplicatesFound += 1
               else:
                  stack.append(child)
            mask <<= 1;
      return False

   def dls(self, depthLimit):
      stack = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      # While there are candidate boards in the stack
      while stack:
         # Keep track of the max stack length
         if len(stack) > self.maxQueueLength:
            self.maxQueueLength = len(stack)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         candidate = stack.pop()
         #print candidate, str(candidate.depth)
         self.numTestDone += 1
         visitedBoards.add(self)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath()
            self.goalFounded = True
            self.goalDepth = candidate.depth
            return True
         
         # Detect duplicates among children, increment count, add only 
         #  non-duplicates to queue
         moves = candidate.possibleMoves
         mask = 1
         while mask != 16:
            if moves & mask:
               child = candidate.spawnChild(mask)
               if child in visitedBoards:
                  self.numDuplicatesFound += 1
               else:
                  if child.depth <= depthLimit:
                     stack.append(child)
            mask <<= 1;
      return False

   def ids(self, hardDepthLimit):
      # TODO: Check if the stats you are keeping are correct
      stack = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      if not hardDepthLimit:
         hardDepthLimit = 100
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      depthLimit = 0
      while depthLimit < hardDepthLimit:
         depthLimit += 1
         # While there are candidate boards in the stack
         while stack:
            # Keep track of the max stack length
            if len(stack) > self.maxQueueLength:
               self.maxQueueLength = len(stack)
            
            # Retrieve the next candidate, mark it was visited, increment count 
            #  of tests
            candidate = stack.pop()
            self.numTestDone += 1
            visitedBoards.add(self)
            if self.maxDepthSearched < candidate.depth:
               self.maxDepthSearched = candidate.depth
            
            # Test if this is the goal
            if candidate == self.goal:
               print "Goal found at a depth of " + str(candidate.depth)
               self.pathLength = candidate.printPath()
               self.goalFounded = True
               self.goalDepth = candidate.depth
               return True
            
            # Detect duplicates among children, increment count, add only 
            #  non-duplicates to queue
            moves = candidate.possibleMoves
            mask = 1
            while mask != 16:
               if moves & mask:
                  child = candidate.spawnChild(mask)
                  if child in visitedBoards:
                     self.numDuplicatesFound += 1
                  else:
                     if child.depth <= depthLimit:
                        stack.append(child)
               mask <<= 1;
      return False   

   def h1(self, candidateBoard):
      difference = 0
      for k in range(9):
         i = k / 3
         j = k % 3
         if self.goal.tiles[i][j] != candidateBoard.tiles[i][j]:
            difference += 1
      return difference
   
   def h2(self, candidateBoard):
      manhattenDistance = 0
      for k in range(9):
         i = k / 3
         j = k % 3
         goalPosition = self.reverseIndex[candidateBoard.tiles[i][j]]
         l = goalPosition / 3
         m = goalPosition % 3
         manhattenDistance += math.fabs(i-l) + math.fabs(j-m)
      return manhattenDistance
   
   def estimatedCostH1(self, candidateBoard):
      return candidateBoard.depth + h1(candidateBoard)

   def estimatedCostH2(self, candidateBoard):
      return candidateBoard.depth + h2(candidateBoard)

   def greedy(self, heuristicFunctionFlag):
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      while queue:
         # Keep track of the max queue length
         if len(queue) > self.maxQueueLength:
            self.maxQueueLength = len(queue)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         if heuristicFunctionFlag:
            queue = sorted(queue, key = self.h1)
         else:
            queue = sorted(queue, key = self.h2)
         candidate = queue.pop(0)
         self.numTestDone += 1
         visitedBoards.add(self)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath()
            self.goalFounded = True
            self.goalDepth = candidate.depth
            return True
         
         # Detect duplicates among children, increment count, add only 
         #  non-duplicates to queue
         moves = candidate.possibleMoves
         mask = 1
         while mask != 16:
            if moves & mask:
               child = candidate.spawnChild(mask)
               if child in visitedBoards:
                  self.numDuplicatesFound += 1
               else:
                  queue.append(child)
            mask <<= 1;
      return False

   def astar(self, heuristicFunctionFlag):
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      while queue:
         # Keep track of the max queue length
         if len(queue) > self.maxQueueLength:
            self.maxQueueLength = len(queue)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         if heuristicFunctionFlag:
            queue = sorted(queue, key = self.estimatedCostH1)
         else:
            queue = sorted(queue, key = self.estimatedCostH2)
         candidate = queue.pop(0)
         self.numTestDone += 1
         visitedBoards.add(self)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath()
            self.goalFounded = True
            self.goalDepth = candidate.depth
            return True
         
         # Detect duplicates among children, increment count, add only 
         #  non-duplicates to queue
         moves = candidate.possibleMoves
         mask = 1
         while mask != 16:
            if moves & mask:
               child = candidate.spawnChild(mask)
               if child in visitedBoards:
                  self.numDuplicatesFound += 1
               else:
                  queue.append(child)
            mask <<= 1;
      return False

   def idastar(self, heuristicFunctionFlag, depthLimit):
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      while queue:
         # Keep track of the max queue length
         if len(queue) > self.maxQueueLength:
            self.maxQueueLength = len(queue)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         if heuristicFunctionFlag:
            queue = sorted(queue, key = self.estimatedCostH1)
         else:
            queue = sorted(queue, key = self.estimatedCostH2)
         candidate = queue.pop(0)
         self.numTestDone += 1
         visitedBoards.add(self)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath()
            self.goalFounded = True
            self.goalDepth = candidate.depth
            return True
         
         # Detect duplicates among children, increment count, add only 
         #  non-duplicates to queue
         moves = candidate.possibleMoves
         mask = 1
         while mask != 16:
            if moves & mask:
               child = candidate.spawnChild(mask)
               if child in visitedBoards:
                  self.numDuplicatesFound += 1
               else:
                  if child.depth <= depthLimit:
                     queue.append(child)     # Append to the queue iff it is
                                             #  within the depth limit
            mask <<= 1;
      return False

class Main:
   def main(self):
      goalArray = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
      rootArray = [[1, 3, 4], [8, 6, 2], [7, 0, 5]]
      root = Board()
      root.constructBoard(rootArray)
      goal = Board()
      goal.constructBoard(goalArray)
      
      print "Root"
      print root
      print "Goal"
      print goal
      puzzle = EightPuzzle(root, goal)
      #puzzle.bfs()
      #puzzle.dfs()
      #puzzle.dls(10)
      puzzle.greedy(True)
      puzzle.printStats()
      print "Done"

run = Main()
run.main()
