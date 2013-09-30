import random

class Board:
   def __init__(self):
      #self.tiles = [[-1]*3]*3
      self.tiles = [[], [], []]
      self.emptyTile = -1
      self.possibleMoves = 0
      self.parent = None
      self.depth = 0
      self.signature = ""
      
   def __eq__(self, other):
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         if self.tiles[i][j] != other.tiles[i][j]:
           return False
      return True
   
   def __hash__(self):
      return hash(self.signature)

   def __str__(self):
      string = ""
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         string += str(self.tiles[i][j]) + " "
         if (k + 1) % 3 == 0:
            string += "\n"
      return string
   
   def computeSignature(self):
      self.signature = ""
      for row in self.tiles:
         for tile in row:
            self.signature += `tile`

   def getSignature(self):
      return self.signature

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
   
   def scrambleBoard(self, count):
      while count:
         numMoves = 4
         if self.possibleMoves != 8|4|2|1:
            numMoves -= 1
            if self.possibleMoves != 8|4|2 and self.possibleMoves != 8|4|1 and self.possibleMoves != 8|2|1 and self.possibleMoves != 4|2|1:
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

   def generateBoard(self, scrambleCount):
      for k in range(9):                  # Board size = 3
         i = k / 3
         j = k % 3
         self.tiles[i].append(3*i + j)
      self.emptyTile = 0
      self.possibleMoves = 2|4
      if scrambleCount:
         self.scrambleBoard(scrambleCount)
      
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

   def spawnChild(self, moveCode): # moveCode should be a valid move in self.possibleMoves
      child = self.copyBoard()
      child.moveTile(moveCode)
      child.parent = self
      child.depth += 1
      return child

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

class EightPuzzle:
   def __init__(self, root, goal):
      self.root = root
      self.goal = goal
      self.timeTaken = 0.0
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      self.goalFounded = False
      self.goalDepth = -1
      
   def printStats(self):
      print "Time taken = " + str(self.timeTaken)
      print "No. of tests done = " + str(self.numTestDone)
      print "Max. queue length = " + str(self.maxQueueLength)
      print "No. of duplicates found = " + str(self.numDuplicatesFound)
      print "Max. depth searched = " + str(self.maxDepthSearched)
      print "Path length = " + str(self.pathLength)
      print "Goal found = " + str(self.goalFounded)
      print "Goal depth = " + str(self.goalDepth)
      
   def bfs(self):
      queue = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      visitedBoards = set()
      visitedBoards.add(self.root)
      
      while queue:
         # Keep track of the max queue length
         if len(queue) > self.maxQueueLength:
            self.maxQueueLength = len(queue)
         
         # Retrieve the next candidate
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
         
         #Detect duplicates among children, increment count, add only non-duplicates to queue
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

   def dfs(self):
      stack = [self.root]
      self.numTestDone = 0
      self.maxQueueLength = 0
      self.numDuplicatesFound = 0
      self.maxDepthSearched = 0
      self.pathLength = 0
      
      visitedBoards = set()
      visitedBoards.add(self.root)
      
      while stack:
         # Keep track of the max stack length
         if len(stack) > self.maxQueueLength:
            self.maxQueueLength = len(stack)
         
         # Retrieve the next candidate
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
         
         #Detect duplicates among children, increment count, add only non-duplicates to stack
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
      
      visitedBoards = set()
      visitedBoards.add(self.root)
      
      while stack:
         # Keep track of the max stack length
         if len(stack) > self.maxQueueLength:
            self.maxQueueLength = len(stack)
         
         # Retrieve the next candidate
         candidate = stack.pop()
         print candidate, str(candidate.depth)
         if candidate.depth > depthLimit:
            print "Depth limit"
            continue
            #print "Depth limit reached. Goal not found."
            #return False
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
         
         #Detect duplicates among children, increment count, add only non-duplicates to stack
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
      
      visitedBoards = set()
      visitedBoards.add(self.root)
      
      depthLimit = 0
      while depthLimit < hardDepthLimit:
         depthLimit += 1
         while stack:
            # Keep track of the max stack length
            if len(stack) > self.maxQueueLength:
               self.maxQueueLength = len(stack)
            
            # Retrieve the next candidate
            candidate = stack.pop()
            if candidate.depth > depthLimit:
               print "Depth limit reached. Goal not found."
               return
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
            
            #Detect duplicates among children, increment count, add only non-duplicates to stack
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
      puzzle.bfs()
      #puzzle.dfs()
      #puzzle.dls(10)
      puzzle.printStats()
      print "Done"

run = Main()
run.main()
