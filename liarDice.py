#encoding:utf-8
# -*- coding: utf-8 -*- 
import sys
import dice
# from prob import ProbAgent
from newProb import ProbAgent

notOne = False
isOne  = True
firstPlayerOrder = 1

class LiarDiceGame:
  

  def  __init__(self):
    self.playerYellHistory       = {} # 
    self.allRealDiceStatus       = [] # ex. [(2,1),(3,2),(1,3),(1,4),(1,5),(1,6)]
    self.playerToDiceStatusDict  = {} # ex. {1:[(2,1),(3,2),(1,3),(1,4),(1,5),(1,6)],2:[(2,1),(3,2),(1,3),(1,4),(1,5),(1,6)]}
    self.lastPlayer        = None
    self.catchPlayer       = None
    self.prevYell          = None # add func to record

  def buildYellNOneTuple(self, yellTuple):
    return yellTuple + (isOne,) if yellTuple[1] == 1 else yellTuple + (notOne,)

  def readCommand(self):
    argList = sys.argv
    if len( argList ) >= 1:
      playerNumber = int( argList[ argList.index('-p') + 1 ] ) if '-p' in argList else 3 #-p: player
      diceNumber   = int( argList[ argList.index('-d') + 1 ] ) if '-d' in argList else 5 #-d: dice 
    return [ playerNumber, diceNumber ] 
  
  def recordPlayerYell(self, playerOrder, yellNOneTuple):
    if self.playerYellHistory.has_key( playerOrder ):
      self.playerYellHistory[ playerOrder ].append( yellNOneTuple )
    else:
      self.playerYellHistory[ playerOrder ] = [ yellNOneTuple ]

  def recordCatchNLastPlayer(self, playerOrder, playerNumber):
    self.lastPlayer  = playerOrder - 1 if playerOrder != firstPlayerOrder else playerNumber
    self.catchPlayer = playerOrder

  def gameLoop(self, playerNumber):
    playerOrder = firstPlayerOrder
    while True:
      print "Order of player", playerOrder
      yellTuple, Catch = input("how many dice? 要不要抓?")
      yellNOneTuple = self.buildYellNOneTuple( yellTuple )
      print yellNOneTuple, Catch
      self.recordPlayerYell(playerOrder, yellNOneTuple)
      if Catch:
        self.recordCatchNLastPlayer( playerOrder, playerNumber )
        print "Game Over, start showing result"
        print "catchPlayer:", self.catchPlayer
        print "lastPlayer:", self.lastPlayer
        print "playerYellHistory:", self.playerYellHistory
        break
      else:
        if playerOrder < playerNumber:
          playerOrder += 1 # go to next playerOrder
        else:
          playerOrder = firstPlayerOrder

  def run(self):  
    playerNumber, diceNumber = self.readCommand()
    print "playerNumber:", playerNumber, "diceNumber:", diceNumber
    self.playerToDiceStatusDict = dice.generate( self.playerToDiceStatusDict, playerNumber, diceNumber )
    self.allRealDiceStatus      = dice.allReallDiceStatusCount( self.playerToDiceStatusDict.values() )
    print "all dice status:", self.allRealDiceStatus
    self.gameLoop( playerNumber )


if __name__ == '__main__':
  LiarDiceGame().run()
