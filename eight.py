import random
import math
import argparse
import time
import sys
import gc


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
      self.move = -1                      # The move through which this board 
                                          #  is related to it's parent.
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
            if     self.possibleMoves != 8|4|2 and self.possibleMoves != 8|4|1 and self.possibleMoves != 8|2|1 and self.possibleMoves != 4|2|1:
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
         self.tiles[i].append(model[k])
         #print "<" + str(self.tiles[i][j]) + ", " + str(model[i][j]) + ">"
         if model[k] == 0:
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
      copy.move = -1
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
      child.move = moveCode
      return child

   # Print the path of derivation from the root board to this board
   def printPath(self, verbose):
      pathLength = 0
      stack = []
      moves = {1: "UP", 2: "RIGHT", 4: "DOWN", 8: "LEFT"}
      
      while self: # TODO: Check for error
         stack.append(self)
         stack.append(moves.get(self.move, ""))
         self = self.parent
         pathLength += 1
      
      print "=============================="
      print "Path is given below:"
      while stack:
         self = stack.pop()
         if verbose:
            print self
         else:
            if self and type(self) is str:
               print self,
      print "\n------------------------------"
      return pathLength - 1 # TODO: Check if correct

# Class that abstracts the notion of the 8Puzzle
class EightPuzzle:
   def __init__(self, root, goal, verbose, timer):
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
      self.verbose = verbose        # Whether to print the output verbosely
      self.hardDepthLimit = 50      # Hard depth limit for algorithms that 
                                    #  has a tendency to search at large depths
                                    #  unless stopped.
      self.algorithm = ""           # Algorithm used
      self.heuristic = None         # Heuristic used
      self.timer = timer
      for k in range(9):
         i = k / 3
         j = k % 3
         self.reverseIndex[self.goal.tiles[i][j]] = k

   # Print the stats for the search run
   def printStats(self):
      print "Algorithm               = "  + str(self.algorithm)
      if self.heuristic == True:
         print "Heuristic               = No. of states out of place"
      elif self.heuristic == False:
         print "Heuristic               = Manhatten distance"
      else:
         print "Heuristic               = None"
      print "Time taken              = "  + str(self.timeTaken)
      print "No. of tests done       = "  + str(self.numTestDone)
      print "Max. queue length       = "  + str(self.maxQueueLength)
      print "No. of duplicates found = "  + str(self.numDuplicatesFound)
      print "Max. depth searched     = "  + str(self.maxDepthSearched)
      #print "Path length             = "  + str(self.pathLength)
      print "Goal found              = "  + str(self.goalFounded)
      print "Goal depth/Path length  = "  + str(self.goalDepth)
      if self.algorithm == "ida*":
         print "Max. recursion depth    = "  + str(self.maxRecursionDepth)
      print "=============================="

   # Breadth First Search
   def bfs(self):
      self.algorithm = "bfs"
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
         if self.timer.getTime() > 300.0:
            print "Time expired"
            return False
         
         # Keep track of the max queue length
         if len(queue) > self.maxQueueLength:
            self.maxQueueLength = len(queue)
            
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         candidate = queue.pop(0)
         self.numTestDone += 1
         visitedBoards.add(candidate)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            #print "Goal found at a depth of " + str(candidate.depth)
            self.goalFounded = True
            self.pathLength = candidate.printPath(self.verbose)
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
      self.algorithm = "dfs"
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
         if self.timer.getTime() > 300.0:
            print "Time expired"
            return False
         
         # Keep track of the max stack length
         if len(stack) > self.maxQueueLength:
            self.maxQueueLength = len(stack)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         candidate = stack.pop()
         self.numTestDone += 1
         visitedBoards.add(candidate)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            #print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath(self.verbose)
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
                  if child.depth <= self.hardDepthLimit:
                     stack.append(child)
            mask <<= 1;
      return False

   def dls(self, depthLimit):
      self.algorithm = "dls"
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
         if self.timer.getTime() > 300.0:
            print "Time expired"
            return False
         
         # Keep track of the max stack length
         if len(stack) > self.maxQueueLength:
            self.maxQueueLength = len(stack)
         
         # Retrieve the next candidate, mark it was visited, increment count 
         #  of tests
         candidate = stack.pop()
         #print candidate, str(candidate.depth)
         self.numTestDone += 1
         visitedBoards.add(candidate)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            #print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath(self.verbose)
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

   def ids(self):
      # TODO: Check if the stats you are keeping are correct
      self.algorithm = "ids"
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      depthLimit = 0
      while depthLimit < self.hardDepthLimit:
         depthLimit += 1
         stack = [self.root]
         # While there are candidate boards in the stack
         while stack:
            if self.timer.getTime() > 300.0:
               print "Time expired"
               return False
            
            # Keep track of the max stack length
            if len(stack) > self.maxQueueLength:
               self.maxQueueLength = len(stack)
            
            # Retrieve the next candidate, mark it was visited, increment count 
            #  of tests
            candidate = stack.pop()
            self.numTestDone += 1
            visitedBoards.add(candidate)
            if self.maxDepthSearched < candidate.depth:
               self.maxDepthSearched = candidate.depth
            
            # Test if this is the goal
            if candidate == self.goal:
               #print "Goal found at a depth of " + str(candidate.depth)
               self.pathLength = candidate.printPath(self.verbose)
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
      return candidateBoard.depth + self.h1(candidateBoard)

   def estimatedCostH2(self, candidateBoard):
      return candidateBoard.depth + self.h2(candidateBoard)

   def greedy(self, heuristicFunctionFlag):
      self.algorithm = "greedy"
      self.heuristic = heuristicFunctionFlag
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      while queue:
         if self.timer.getTime() > 300.0:
            print "Time expired"
            return False
         
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
         visitedBoards.add(candidate)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            #print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath(self.verbose)
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
                  if child.depth <= self.hardDepthLimit:
                     queue.append(child)
            mask <<= 1;
      return False

   def astar(self, heuristicFunctionFlag):
      self.algorithm = "a*"
      self.heuristic = heuristicFunctionFlag
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      # Keeps track of the boards that have been visited
      visitedBoards = set()
      
      while queue:
         if self.timer.getTime() > 300.0:
            print "Time expired"
            return False
         
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
         visitedBoards.add(candidate)
         if self.maxDepthSearched < candidate.depth:
            self.maxDepthSearched = candidate.depth
         
         # Test if this is the goal
         if candidate == self.goal:
            #print "Goal found at a depth of " + str(candidate.depth)
            self.pathLength = candidate.printPath(self.verbose)
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
                  if child.depth <= self.hardDepthLimit:
                     queue.append(child)
            mask <<= 1;
      return False

   def DFSContour3(self, candidateBoard, fLimit, heuristicFunctionFlag, recursionDepth):
      recursionDepth += 1
      self.numTestDone += 1
      self.visitedBoards.add(candidateBoard)
      if self.maxDepthSearched < candidateBoard.depth:
         self.maxDepthSearched = candidateBoard.depth
      if self.maxRecursionDepth < recursionDepth:
         self.maxRecursionDepth = recursionDepth
      
      if self.timer.getTime() > 10.0:
         #print "Time expired"
         return 2000000.0

      fCost = self.estimatedCostH1(candidateBoard)
      
      if fCost > fLimit:
         self.solution = None
         return fCost
      
      if candidateBoard == self.goal:
         self.solution = candidateBoard
         return fCost
      
      # Detect duplicates among children, increment count, add only 
      #  non-duplicates to queue
      minimum = 2000000.0
      moves = candidateBoard.possibleMoves
      mask = 1
      while mask != 16:
         if moves & mask:
            child = candidateBoard.spawnChild(mask)
            if child in self.visitedBoards:
               self.numDuplicatesFound += 1
            else:
               newF = self.DFSContour3(child, fLimit, heuristicFunctionFlag, recursionDepth)     # Append to the queue iff it is
               if self.solution:
                  return fLimit
               if newF < minimum:
                  minimum = newF
         mask <<= 1;
      return minimum
      
   def idastar3(self, heuristicFunctionFlag):
      self.algorithm = "ida*"
      self.heuristic = heuristicFunctionFlag
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      self.maxRecursionDepth = 0
      self.solution = None
      
      # Keeps track of the boards that have been visited
      self.visitedBoards = set()
      
      if heuristicFunctionFlag:
         fLimit = self.estimatedCostH1(self.root)
      else:
         fLimit = self.estimatedCostH2(self.root)
      
      while True:
         fLimit = self.DFSContour3(self.root, fLimit, heuristicFunctionFlag, 0)
         if self.solution:
            self.pathLength   = self.solution.printPath(self.verbose)
            self.goalFounded  = True
            self.goalDepth    = self.solution.depth
            return True
         if fLimit > 1999999.0:
            return False

# Class to time each search operation
class Timer:
   """Class to time function calls - Counts the CPU time used"""
   # Start the timer
   def __init__(self, string, limit = 100, numBars = 100):
      self.string = string
      self.beginning = time.clock()
      self.time  = 0.0
      self.numBars = numBars
      self.oneBar = 0
      self.numBarsWritten = 0
      self.limit = limit
      self.progress = 0
      if self.numBars:
         #print self.string
         self.oneBar = int(math.ceil(limit/numBars))
         sys.stdout.write("[%s]" % (" " * numBars))
         sys.stdout.flush()
         sys.stdout.write("\b" * (numBars + 1))
   
   def start(self, string, limit = 100, numBars = 100):
      self.__init__(string, limit, numBars)
      
   def getTime(self):
      if self.beginning:
         return time.clock() - self.beginning + self.time
      else:
         return self.time

   def stop(self):
      """"Print the CPU secs used"""
      #if self.progress <= self.limit:
      #   sys.stdout.write('\x1b[2K')
      #   sys.stdout.write("\b" * (self.numBarsWritten + 2))
      #   self.progress = self.limit
      if self.beginning:
         timetaken = time.clock() - self.beginning + self.time
      else:
         timetaken = self.time
      #print "\033[92mTime taken for (%s) = %f\033[0m" % (self.string, time)
      self.string = None
      self.beginning = None
      self.time = None
      self.limit = 0
      self.progress = 0
      self.numBars = 0
      self.oneBar = 0
      return timetaken
      
   def tick(self):
      if self.beginning and self.progress < self.limit:
         self.progress += 1
         if self.oneBar and self.progress % self.oneBar == 0:
            if self.numBarsWritten < self.numBars:
               if (self.numBarsWritten + 1) % 10 == 0:
                  sys.stdout.write("|")
               else:
                  sys.stdout.write("-")
               sys.stdout.flush()
               self.numBarsWritten += 1
            else:
               self.progress = self.limit
               self.numBarsWritten = self.numBars
         #if self.progress == self.limit:
         #   sys.stdout.write('\x1b[2K')
         #   sys.stdout.write("\b" * (self.numBars + 2))
   
   def pause(self):
      if self.beginning:
         self.time += time.clock() - self.beginning
         self.beginning = None
   def unpause(self):
      if not self.beginning:
         self.beginning = time.clock()

class Main:
   def parseCommandLine(self):
      parser = argparse.ArgumentParser(prog = "python tile.py", description='8-Puzzle Program', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
      parser.add_argument('--version', action='version', version='8-Puzzle 1.0')
      parser.add_argument('-a', metavar='<algorithm>', type = str, nargs = 1, required = True,
                         choices = ["bfs", "dfs", "dls", "ids", "greedy", "a*", "ida*", "all"], default = "all",
                         help = 'Search algorithm to be used, could be one of "bfs", "dfs", "dls", "ids", "greedy", "a*" or "ida*"')
      parser.add_argument('-r', metavar='<tile>', type = str, nargs = '+', required = True, 
                         help = 'Root board to be used. Do not use commas or quotes Eg. "0 1 2 3 4 5 6 7 8 9"')
      parser.add_argument('-g', metavar='<tile>', type = str, nargs = '+', required = False, 
                         default=['1', '2', '3', '8', '0', '4', '7', '6', '5'], 
                         help = 'Goal board to be used. Do not use commas or quotes Eg. "0 1 2 3 4 5 6 7 8 9"')
      parser.add_argument('-d', metavar='<depth limit>', type = int, nargs = 1, required = False, 
                         default=25, 
                         help='Depth upto which to be searched. Required for dls, ida*. If not provided, default value of 25 would be used')
      parser.add_argument('-f', metavar='<heuristic function>', type = str, nargs = 1, required = False,
                         choices = ["h1", "h2"],
                         help='Heuristic function to be used. Should be within quotes. Eg. "h1" or "h2"')
      parser.add_argument('-v', action='store_true', help='Prints verbose output')

      args = parser.parse_args(sys.argv[1:])
      self.algorithm = args.a[0]
      
      self.rootModel = []
      for string in args.r:
         self.rootModel.append(int(string))
      
      if args.g:
         self.goalModel = []
         for string in args.g:
            self.goalModel.append(int(string))         
      else:
         self.goalModel = None
      
      if self.algorithm == "dls":
         if args.d:
            self.depthLimit = args.d[0]
         else:
            print "Depth limit is required if algorithm is dls"
            return False
      else:
         self.depthLimit = None
      if self.algorithm == "greedy" or self.algorithm == "a*" or self.algorithm == "ida*":
         if args.f:
            if args.f[0] == "h1":
               self.heuristicFunctionFlag = True
            else:
               self.heuristicFunctionFlag = False
         else:
            print "Heuristic function required if using one of the informed search algorithms (greedy, a*, ida*)"
            return False
      else:
         self.heuristicFunctionFlag = None
      if args.v:
         self.verbose = True
      else:
         self.verbose = False
      return True

   def doSearch(self):
      root = Board()
      root.constructBoard(self.rootModel)
      goal = Board()
      goal.constructBoard(self.goalModel)
      
      if self.verbose:
         print "Root"
         print root
         print "Goal"
         print goal
         print "------------------------------"
      timerSearch = Timer("Search algorithm", 0, 0)
      puzzle = EightPuzzle(root, goal, self.verbose, timerSearch)
      
      if self.algorithm == "bfs":
         puzzle.bfs()
      elif self.algorithm == "dfs":
         puzzle.dfs()
      elif self.algorithm == "dls":
         puzzle.dls(self.depthLimit)
      elif self.algorithm == "ids":
         puzzle.ids()
      elif self.algorithm == "greedy":
         puzzle.greedy(self.heuristicFunctionFlag)
      elif self.algorithm == "a*":
         puzzle.astar(self.heuristicFunctionFlag)
      elif self.algorithm == "ida*":
         puzzle.idastar3(self.heuristicFunctionFlag)
      puzzle.timeTaken = timerSearch.stop()
      puzzle.printStats()
      
   def main(self):
      gc.enable()
      if not self.parseCommandLine():
         return
      
      if not self.goalModel:
         self.goalModel = [1, 2, 3, 8, 0, 4, 7, 6, 5]
      if self.algorithm != "all":
         self.doSearch()
      else:
         rootModels = [[1, 3, 4, 8, 6, 2, 7, 0, 5], [2, 8, 1, 0, 4, 3, 7, 6, 5], [5, 6, 7, 4, 0, 8, 3, 2, 1]]
         #rootModels = [[1, 3, 4, 8, 6, 2, 7, 0, 5], [2, 8, 1, 0, 4, 3, 7, 6, 5]]
         #rootModels = [[5, 6, 7, 4, 0, 8, 3, 2, 1]]
         algorithms = ["bfs", "dfs", "dls", "ids", "greedy", "a*", "ida*"]
         heuristicFunctionFlags = [True, False]
         self.goalModel = [1, 2, 3, 8, 0, 4, 7, 6, 5]
         self.depthLimit = 25
         self.verbose = False
         for rootModel in rootModels:
            self.rootModel = rootModel
            print "Goal: " + str(rootModel)
            for algorithm in algorithms:
               self.algorithm = algorithm
               if self.algorithm == "greedy" or self.algorithm == "a*" or self.algorithm == "ida*":
                  for heuristic in heuristicFunctionFlags:
                     self.heuristicFunctionFlag = heuristic
                     self.doSearch()
               else:
                  self.doSearch()
          
run = Main()
run.main()
