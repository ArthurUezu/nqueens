import sys
import time
import multiprocessing 

QUEEN = -10
EMPTY = 0



def makeBoard( N ):
    """create a 2-D array of ints with dimension N
    Returns the 2D array"""
    board = []
    for i in range( N ):
        board.append( [] )
        for j in range( N ):
            board[i].append( EMPTY )
    return board
    
def goHome():
    sys.stderr.write( "\x1b[0;0H" )

def displaySolution( board ):
  """Display the solution as a list of column indexes"""
  list = []
  for i in range( len( board ) ):
      for j in range( len( board ) ):
          if board[ i ][ j ]==QUEEN:
              list.append( str( j ) )
  print "Solution (%2d queens): " % len( list ), ','.join( list ), ' '*20

def displayBoard( board, home=False ):
    """display the 2D array, showing empty cells as .
    and queens as Q"""
    if home: goHome()
    for i in range( len( board ) ):
        for j in range( len( board ) ):
            if board[i][j]==QUEEN: 
               print 'Q',
            else: 
               print '.',
        print
    displaySolution( board )
    
def markLowerBoard( board, row, col, offset ):
    """Once a queen is positioned at location (row,col), 
    all the cells on a lower diagonal and lower vertical
    of this queen must be marqued as unavailable so that
    another queen cannot be put in this place"""

    N = len( board )
    diagleft = col-1
    diagright = col+1
    # mark all lower rows on diagonals and vertical
    for r in range( row+1, N ):
        if diagleft >=0:  board[r][diagleft] += offset
        if diagright <N:  board[r][diagright] += offset
        board[r][col] += offset
        diagleft  -= 1
        diagright += 1

def tryRow( board, row,  N, foundOne, queue, display=False ):
    """ put a queen on give row, and recursively try all queens
    on successive rows"""
    if row >= N:
       return True #we found a solution!

    if display:
        displayBoard( board, True )

    for col in range( N ):
        # if a solution has been found, stop
        if foundOne.value == 1:
            return False
        if board[row][col] == EMPTY:
            # put a queen here
            board[ row ][ col ] = QUEEN
            markLowerBoard( board, row, col, +1 )
            ok = tryRow( board, row+1, N, foundOne, queue, display )
            if not ok:
                # backtrack
                board[ row ][ col ] = EMPTY
                markLowerBoard( board, row, col, -1 )
            else:
                return True
    return False           

def firstQueenAt( col, N, foundOne, queue ):
    board = makeBoard( N )
    board[0][col] = QUEEN
    markLowerBoard( board, 0, col, +1 )
    ok = tryRow( board, 1, N, foundOne, queue, False )
    if ok:
        foundOne.value = 1
        queue.put( board )
        #displayBoard( board )


def main():
    if len( sys.argv ) < 2:
        print "Syntax: nqueens.py N"
        print "        where N is the # of queens"
        return

    #--- get dimension, create board, and solve! ---
    N = int( sys.argv[1] )

    # set bool to True to display progress...
    list = []
    foundOne = multiprocessing.Value( 'i', 0 ) # create shared memory value
                                           # containing an int and set it
                                           # to false    
    queue = multiprocessing.Queue()

    for i in range( N ):
        p = multiprocessing.Process( target=firstQueenAt, args=( i, N, foundOne, queue ) )
        p.start()
        list.append( p )

    while foundOne.value == 0:
        time.sleep( 0.1 )

    board = queue.get()
    displayBoard( board )

    for p in list:
        p.join()
    
    print "\nDone!"

if __name__=="__main__":
    main()