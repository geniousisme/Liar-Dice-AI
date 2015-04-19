from random import randrange
from operator import add

diceDotNumber = 6

def generate(playerToDiceStatusDict, playerNumber, diceNumber):
  for playerOrder in xrange( 1, playerNumber + 1 ):
    diceStatusCount = [ 0 ]
    for i in xrange( 1, diceDotNumber + 1 ):
      if sum( diceStatusCount ) < diceNumber:
        if i < diceDotNumber:
          diceStatusCount.append( randrange( 0, diceNumber - sum( diceStatusCount ) ) )
        if i == diceDotNumber:
          diceStatusCount.append( diceNumber - sum( diceStatusCount ) )
      elif sum( diceStatusCount ) == diceNumber:
        diceStatusCount.append( 0 )
    playerToDiceStatusDict[ playerOrder ] = diceStatusCount
  # print "playerToDiceStatusDict:", playerToDiceStatusDict
  # print playerToDiceStatusDict.values()
  return playerToDiceStatusDict

def allReallDiceStatusCount(diceStatusCountArrayList):
  tmpDiceStatusCountArray = [0 for i in range( diceDotNumber + 1 )] #initialize [0,0,...,0]
  for diceStatusCountArray in diceStatusCountArrayList:
    tmpDiceStatusCountArray = map(add, tmpDiceStatusCountArray, diceStatusCountArray)
  return [ (diceStatusCount, diceStatus) for diceStatus, diceStatusCount in enumerate(tmpDiceStatusCountArray) ][1:] #drop the 0,0 case
  




