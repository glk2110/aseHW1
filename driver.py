from __future__ import print_function
from heapq import heappush, heappop
import sys
import collections
import math
import time
import resource

maxValue = 0
done = 0

class State:
    def __init__(self, board, moves, cost=-1):
        self.board = board
        self.moves = moves
        self.cost = cost

    def __lt__(self, other):
        if self.cost != other.cost:
            return self.cost < other.cost
        else:
            if self.moves[len(self.moves)-1] == "Right":
                selfValue = 4
            elif self.moves[len(self.moves)-1] == "Left":
                selfValue = 3
            elif self.moves[len(self.moves)-1] == "Down":
                selfValue = 2
            elif self.moves[len(self.moves)-1] == "Up":
                selfValue = 1
            if other.moves[len(other.moves)-1] == "Right":
                otherValue = 4
            elif other.moves[len(other.moves)-1] == "Left":
                otherValue = 3
            elif other.moves[len(other.moves)-1] == "Down":
                otherValue = 2
            elif other.moves[len(other.moves)-1] == "Up":
                otherValue = 1
            return selfValue < otherValue
    
    def getBoard(self):
        return self.board

    def getMoves(self):
        return self.moves
        
    def getPossibleMovesBfs(self):
        pMoves = []
        n = int(math.sqrt(len(self.board)))
        for i in range(len(self.board)):
            if self.board[i] == 0:
                zeroPlace = i
        if  zeroPlace-n>=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-n]
            move[zeroPlace-n] = temp
            moves.append("Up")
            pMoves.append(State(move,moves))
        if  zeroPlace+n<n*n:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+n]
            move[zeroPlace+n] = temp
            moves.append("Down")
            pMoves.append(State(move,moves))
        if  zeroPlace%n!=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-1]
            move[zeroPlace-1] = temp
            moves.append("Left")
            pMoves.append(State(move,moves))
        if  zeroPlace%n!=n-1:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+1]
            move[zeroPlace+1] = temp
            moves.append("Right")
            pMoves.append(State(move,moves))
        return pMoves

    def getPossibleMovesDfs(self):
        pMoves = []
        n = int(math.sqrt(len(self.board)))
        for i in range(len(self.board)):
            if self.board[i] == 0:
                zeroPlace = i
        if  zeroPlace%n!=n-1:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+1]
            move[zeroPlace+1] = temp
            moves.append("Right")
            pMoves.append(State(move,moves))
        if  zeroPlace%n!=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-1]
            move[zeroPlace-1] = temp
            moves.append("Left")
            pMoves.append(State(move,moves))
        if  zeroPlace+n<n*n:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+n]
            move[zeroPlace+n] = temp
            moves.append("Down")
            pMoves.append(State(move,moves))
        if  zeroPlace-n>=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-n]
            move[zeroPlace-n] = temp
            moves.append("Up")
            pMoves.append(State(move,moves))
        return pMoves

    def getPossibleMovesAst(self):
        pMoves = []
        cost = -1
        n = int(math.sqrt(len(self.board)))
        for i in range(len(self.board)):
            if self.board[i] == 0:
                zeroPlace = i
        if  zeroPlace-n>=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-n]
            move[zeroPlace-n] = temp
            moves.append("Up")
            cost = getCost(move)
            cost+= len(moves)
            pMoves.append(State(move,moves,cost))
        if  zeroPlace+n<n*n:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+n]
            move[zeroPlace+n] = temp
            moves.append("Down")
            cost = getCost(move)
            cost+= len(moves)
            pMoves.append(State(move,moves,cost))
        if  zeroPlace%n!=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-1]
            move[zeroPlace-1] = temp
            moves.append("Left")
            cost = getCost(move)
            cost+= len(moves)
            pMoves.append(State(move,moves,cost))
        if  zeroPlace%n!=n-1:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+1]
            move[zeroPlace+1] = temp
            moves.append("Right")
            cost = getCost(move)
            cost+= len(moves)
            pMoves.append(State(move,moves,cost))
        return pMoves
    
    def getPossibleMovesIda(self):
        pMoves = []
        cost = -1
        n = int(math.sqrt(len(self.board)))
        for i in range(len(self.board)):
            if self.board[i] == 0:
                zeroPlace = i
        if  zeroPlace%n!=n-1:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+1]
            move[zeroPlace+1] = temp
            moves.append("Right")
            cost = getCost(move)
            cost+= len(moves)
            if cost <= maxValue:
                pMoves.append(State(move,moves,cost))
        if  zeroPlace%n!=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-1]
            move[zeroPlace-1] = temp
            moves.append("Left")
            cost = getCost(move)
            cost+= len(moves)
            if cost <= maxValue:
                pMoves.append(State(move,moves,cost))
        if  zeroPlace+n<n*n:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace+n]
            move[zeroPlace+n] = temp
            moves.append("Down")
            cost = getCost(move)
            cost+= len(moves)
            if cost <= maxValue:
                pMoves.append(State(move,moves,cost))
        if  zeroPlace-n>=0:
            move = list(self.board)
            moves = list(self.moves)
            temp = move[zeroPlace]
            move[zeroPlace] = move[zeroPlace-n]
            move[zeroPlace-n] = temp
            moves.append("Up")
            cost = getCost(move)
            cost+= len(moves)
            if cost <= maxValue:
                pMoves.append(State(move,moves,cost))
        return pMoves
    
    def isSolved(self):
        cnt = []
        for num in range(len(self.board)):
            cnt.append(num)
        if self.board == cnt:
            return True
        else:
            return False


def bfs(startBoard):
    runningtime = time.clock()
    output = open("output.txt", "w")
    list1 = []
    nodesExpanded = 0
    fringeSize = 0
    maxFringeSize = 0
    ff = 0
    maxSearchDepth = 0
    finalMaxSearchDepth = 0
    runningTime = 0
    maxRamUsage = 0
    itr = 0
    while itr < len(startBoard):
        if itr>=20:
            list1.append(int(startBoard[itr]+startBoard[itr+1]))
            itr += 1
        else:
            list1.append(int(startBoard[itr]))
        itr += 2
    initState = State(list1,[])
    currState =  State(initState.getBoard(),initState.getMoves())

    q = collections.deque([currState])
    qBoards = set()
    qBoards.add(str(currState.board))
    visited = set()
    while q:
        curr = q.popleft()
        ff += 1
        fringeSize = len(q)
        visited.add(str(curr.board))
        qBoards.add(str(curr.board))
        if(curr.isSolved()):
            print("path_to_goal:", end=" ",file = output)
            print(curr.getMoves(),file = output)

            print("cost_of_path:", end=" ",file = output)
            print(len(curr.getMoves()),file = output)

            print("nodes_expanded:", end=" ", file = output)
            print(ff-1,file = output)

            print("fringe_size:", end=" ", file = output)
            print(fringeSize,file = output)

            print("max_fringe_size:", end=" ", file = output)
            print(maxFringeSize,file = output)

            print("search_depth:", end=" ", file = output)
            print(len(curr.getMoves()),file = output)

            print("max_search_depth:", end=" ", file = output)
            print(maxSearchDepth,file = output)

            print("running_time:", end=" ", file = output)
            print("%s"%(time.clock()-runningTime),file = output)

            print("max_ram_usage:", end=" ", file = output)
            print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000,file = output)
            output.close()
            return
        
        for nextMove in curr.getPossibleMovesBfs():
            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
 #               nodesExpanded +=1
                q.append(nextMove)
                qBoards.add(str(nextMove.board))
                fringeSize = len(q)
                if len(nextMove.moves) > maxSearchDepth:
                    maxSearchDepth = len(nextMove.moves)
                if len(q) > maxFringeSize:
                    maxFringeSize = len(q)
 
    print("No Solution")
    output.close()

def dfs(startBoard):
    runningtime = time.clock()
    output = open("output.txt","w")
    list1 = []
    nodesExpanded = 0
    fringeSize = 0
    maxFringeSize = 0
    maxSearchDepth = 0
    oldNodesExpanded = 0
    runningTime = 0
    maxRamUsage = 0
    countr = 0
    ff = 0
    tempList = []
    itr = 0
    while itr < len(startBoard):
        if itr>=20:
            list1.append(int(startBoard[itr]+startBoard[itr+1]))
            itr += 1
        else:
            list1.append(int(startBoard[itr]))
        itr += 2
    initState = State(list1,[])
    currState =  State(initState.getBoard(),initState.getMoves())

    q = collections.deque([currState])
    qBoards = set()
    qBoards.add(str(currState.board))
    visited = set()
    while q:
        curr = q.pop()
        nodesExpanded += 1
        fringeSize = len(q)
        visited.add(str(curr.board))
        qBoards.remove(str(curr.board))
        if(curr.isSolved()):
            print("path_to_goal:", end=" ",file = output)
            print(curr.getMoves(),file = output)

            print("cost_of_path:", end=" ",file = output)
            print(len(curr.getMoves()),file = output)

            print("nodes_expanded:", end=" ",file = output)
            print(nodesExpanded-1,file = output)

            print("fringe_size:", end=" ",file = output)
            print(fringeSize,file = output)

            print("max_fringe_size:", end=" ",file = output)
            print(maxFringeSize,file = output)

            print("search_depth:", end=" ",file = output)
            print(len(curr.getMoves()),file = output)

            print("max_search_depth:", end=" ",file = output)
            print(maxSearchDepth,file = output)

            print("running_time:", end=" ",file = output)
            print("%s"%(time.clock()-runningTime),file = output)

            print("max_ram_usage:", end=" ",file = output)
            print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000,file = output)
            return
#        for nextMove in curr.getPossibleMovesBfs():
#            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
#                nodesExpanded +=1
#                tempList.append(nextMove.board)
#                print(nextMove.board)
#                q.append(nextMove)
 #               qBoards.add(str(nextMove.board))
        for nextMove in curr.getPossibleMovesDfs():
#            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
#                nodesExpanded += 1
 #               print(nodesExpanded)
#                tempList.append(nextMove)
 #               if len(nextMove.moves) > maxSearchDepth:
 #                   maxSearchDepth = len(nextMove.moves)

            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
                q.append(nextMove)
                qBoards.add(str(nextMove.board))
                fringeSize = len(q)
                if len(nextMove.moves) > maxSearchDepth:
                    maxSearchDepth = len(nextMove.moves)
                if len(q) > maxFringeSize:
                    maxFringeSize = len(q)
                    
#        for x in range(len(tempList)):
#            q.append(tempList[len(tempList)-1-x])
#            qBoards.add(str(tempList[len(tempList)-1-x].board))
#            fringeSize = len(q)
#            if len(q) > maxFringeSize:
##            if tempList[len(tempList)-x-1].isSolved():
#                finalFringeSize = fringeSize - x
#        tempList = []
    print("No Solution")

def getCost(listBoard):
    finalCost = 0
    for numb in range(len(listBoard)):
        if listBoard[numb] != 0:
            finalCost += getIndividualCost(numb,listBoard[numb])
    return finalCost

def getIndividualCost(place,value):
    x = place%3
    y = place/3
    properX = value%3
    properY = value/3
    return (abs(x-properX)+abs(y-properY))
    
def ast(startBoard):
    runningtime = time.clock()
    output = open("output.txt", "w")
    list1 = []
    nodesExpanded = 0
    fringeSize = 0
    maxFringeSize = 0
    ff = 0
    maxSearchDepth = 0
    finalMaxSearchDepth = 0
    runningTime = 0
    maxRamUsage = 0
    itr = 0
    startCost = -1
    while itr < len(startBoard):
        if itr>=20:
            list1.append(int(startBoard[itr]+startBoard[itr+1]))
            itr += 1
        else:
            list1.append(int(startBoard[itr]))
        itr += 2
    startCost = getCost(list1)
    initState = State(list1,[],startCost)
    currState =  State(initState.getBoard(),initState.getMoves(),startCost)

    q = [currState]
    qBoards = set()
    qBoards.add(str(currState.board))
    visited = set()
    while q:
        curr = heappop(q)
        ff += 1
        fringeSize = len(q)
        visited.add(str(curr.board))
        qBoards.remove(str(curr.board))
        if(curr.isSolved()):
            print("path_to_goal:", end=" ",file = output)
            print(curr.getMoves(),file = output)

            print("cost_of_path:", end=" ",file = output)
            print(len(curr.getMoves()),file = output)

            print("nodes_expanded:", end=" ", file = output)
            print(ff-1,file = output)

            print("fringe_size:", end=" ", file = output)
            print(fringeSize,file = output)

            print("max_fringe_size:", end=" ", file = output)
            print(maxFringeSize,file = output)

            print("search_depth:", end=" ", file = output)
            print(len(curr.getMoves()),file = output)

            print("max_search_depth:", end=" ", file = output)
            print(maxSearchDepth,file = output)

            print("running_time:", end=" ", file = output)
            print("%s"%(time.clock()-runningTime),file = output)

            print("max_ram_usage:", end=" ", file = output)
            print(maxRamUsage,file = output)
            output.close()
            return
        
        for nextMove in curr.getPossibleMovesAst():
            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
 #               nodesExpanded +=1
                heappush(q, nextMove)
                qBoards.add(str(nextMove.board))
                fringeSize = len(q)
                if len(nextMove.moves) > maxSearchDepth:
                    maxSearchDepth = len(nextMove.moves)
                if len(q) > maxFringeSize:
                    maxFringeSize = len(q)
                if nextMove.isSolved():
 #                   finalNodesExpanded = nodesExpanded
                    maxRamUsage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000
            elif str(nextMove.board) in qBoards:
                nextMove.cost = getCost(nextMove.board)
    print("No Solution")
    output.close()

def ida(startBoard):
    global done
    global maxValue
    runningtime = time.clock()
    output = open("output.txt","w")
    list1 = []
    nodesExpanded = 0
    fringeSize = 0
    maxFringeSize = 0
    maxSearchDepth = 0
    oldNodesExpanded = 0
    runningTime = 0
    maxRamUsage = 0
    countr = 0
    ff = 0
    tempList = []
    itr = 0
    while itr < len(startBoard):
        if itr>=20:
            list1.append(int(startBoard[itr]+startBoard[itr+1]))
            itr += 1
        else:
            list1.append(int(startBoard[itr]))
        itr += 2
    initState = State(list1,[])
    currState =  State(initState.getBoard(),initState.getMoves())
    while done == 0:
        q = collections.deque([currState])
        qBoards = set()
        qBoards.add(str(currState.board))
        visited = set()
        while q:
            curr = q.pop()
            nodesExpanded += 1
            fringeSize = len(q)
     #       visited.add(str(curr.board))
            qBoards.remove(str(curr.board))
            if(curr.isSolved()):
                done = 1
                print("path_to_goal:", end=" ",file = output)
                print(curr.getMoves(),file = output)

                print("cost_of_path:", end=" ",file = output)
                print(len(curr.getMoves()),file = output)

                print("nodes_expanded:", end=" ",file = output)
                print(nodesExpanded-1,file = output)

                print("fringe_size:", end=" ",file = output)
                print(fringeSize,file = output)

                print("max_fringe_size:", end=" ",file = output)
                print(maxFringeSize,file = output)

                print("search_depth:", end=" ",file = output)
                print(len(curr.getMoves()),file = output)

                print("max_search_depth:", end=" ",file = output)
                print(maxSearchDepth,file = output)

                print("running_time:", end=" ",file = output)
                print("%s"%(time.clock()-runningTime),file = output)

                print("max_ram_usage:", end=" ",file = output)
                print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000000,file = output)
                return
    #        for nextMove in curr.getPossibleMovesBfs():
    #            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
    #                nodesExpanded +=1
    #                tempList.append(nextMove.board)
    #                print(nextMove.board)
    #                q.append(nextMove)
     #               qBoards.add(str(nextMove.board))
            for nextMove in curr.getPossibleMovesIda():
    #            if str(nextMove.board) not in visited and str(nextMove.board) not in qBoards:
    #                nodesExpanded += 1
     #               print(nodesExpanded)
    #                tempList.append(nextMove)
     #               if len(nextMove.moves) > maxSearchDepth:
     #                   maxSearchDepth = len(nextMove.moves)

                #if str(nextMove.board) not in visited and
                if str(nextMove.board) not in qBoards:
                    q.append(nextMove)
                    qBoards.add(str(nextMove.board))
                    fringeSize = len(q)
                    if len(nextMove.moves) > maxSearchDepth:
                        maxSearchDepth = len(nextMove.moves)
                    if len(q) > maxFringeSize:
                        maxFringeSize = len(q)
    #        for x in range(len(tempList)):
    #            q.append(tempList[len(tempList)-1-x])
    #            qBoards.add(str(tempList[len(tempList)-1-x].board))
    #            fringeSize = len(q)
    #            if len(q) > maxFringeSize:
    ##            if tempList[len(tempList)-x-1].isSolved():
    #                finalFringeSize = fringeSize - x
    #        tempList = []
        maxValue += 1
if(sys.argv[1]=="bfs"):
    bfs(sys.argv[2])
elif(sys.argv[1]=="dfs"):
    dfs(sys.argv[2])
elif(sys.argv[1]=="ast"):
    ast(sys.argv[2])
elif(sys.argv[1]=="ida"):
    ida(sys.argv[2])
        
