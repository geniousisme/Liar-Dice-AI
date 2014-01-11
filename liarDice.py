#encoding:utf-8
# -*- coding: utf-8 -*- 
import sys
import dice
# from prob import ProbAgent
from newProb import ProbAgent
import time
# import game
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
      playerNumber = int( argList[ argList.index('-p') + 1 ] ) if '-p' in argList else 3  #-p: player
      diceNumber   = int( argList[ argList.index('-d') + 1 ] ) if '-d' in argList else 5  #-d: dice 
      trainingNumber = int( argList[ argList.index('-t') + 1 ] ) if '-t' in argList else 10 #-t: training
    return [ playerNumber, diceNumber, trainingNumber ] 
  
  def recordPlayerYell(self, playerOrder, yellNOneTuple):
    if self.playerYellHistory.has_key( playerOrder ):
      self.playerYellHistory[ playerOrder ].append( yellNOneTuple )
    else:
      self.playerYellHistory[ playerOrder ] = [ yellNOneTuple ]

  def recordCatchNLastPlayer(self, playerOrder, playerNumber):
    self.lastPlayer  = playerOrder - 1 if playerOrder != firstPlayerOrder else playerNumber
    self.catchPlayer = playerOrder

  def gameLoop(self, playerNumber, diceNumber, trainingNumber, playerToDiceStatusDict):
    playerOrder = firstPlayerOrder
    credibility_list = {1:0.15,2:0.1,3:0.13}
    hostile_player_num = playerNumber - 1
    dice_amount_per_player = diceNumber
    flag_one = False
    risk_rate = 0
    yell_threshold = 0.5
    catch_threshold = 0.2
    
    A_Agent = ProbAgent( playerToDiceStatusDict[ 1 ], hostile_player_num, dice_amount_per_player, 0.05, 0.2, 0.0, credibility_list )
    B_Agent = ProbAgent( playerToDiceStatusDict[ 2 ], hostile_player_num, dice_amount_per_player, 0.1,  0.2, 0.0, credibility_list )
    C_Agent = ProbAgent( playerToDiceStatusDict[ 3 ], hostile_player_num, dice_amount_per_player, 0.15, 0.2, 0.2, credibility_list )
    playerOrderToAgentDict = {1: A_Agent, 2: B_Agent, 3: C_Agent}
    print "playerOrderToAgentDict", playerOrderToAgentDict
    playerOrder = roundNumber = 1
    one_appear = False
    prevYell = None
    while True:
      # raw_input("...")
      print "Order of player", playerOrder, "Agent:", playerOrderToAgentDict[ playerOrder ]
      print "how many dice? 要不要抓?"
      print "prevYell:", prevYell
      if roundNumber == 1:
        decision = playerOrderToAgentDict[ playerOrder ].make_decision() 
      else:
        decision = playerOrderToAgentDict[ playerOrder ].make_decision(prevYell)
      print "decision:", decision
      yellTuple, Catch = decision
      prevYell = yellTuple
      print "yellTuple:", yellTuple, "Catch", Catch
      yellNOneTuple = self.buildYellNOneTuple( yellTuple )
      print yellNOneTuple, Catch
      self.recordPlayerYell(playerOrder, yellNOneTuple)
      if yellNOneTuple[2] and one_appear == False:
        print "ONE"
        for agent in playerOrderToAgentDict.values():
          agent.update_status(playerOrder, yellTuple, True)
        one_appear = True
      else:
        updateAgentList = [ agent for agent in playerOrderToAgentDict.values() if agent != playerOrderToAgentDict[ playerOrder ] ]
        # print "updateAgentList", updateAgentList
        for agent in updateAgentList:
          agent.update_status(playerOrder, yellTuple, False)

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
      roundNumber += 1

  def run(self):  
    playerNumber, diceNumber, trainingNumber = self.readCommand()
    print "playerNumber:", playerNumber, "diceNumber:", diceNumber
    self.playerToDiceStatusDict = dice.generate( self.playerToDiceStatusDict, playerNumber, diceNumber )
    # self.playerToDiceStatusDict = {1:[0,2,1,1,0,1,0], 2:[0,1,1,2,1,0,0], 3:[0,2,0,1,0,2,0]}
    self.allRealDiceStatus      = dice.allReallDiceStatusCount( self.playerToDiceStatusDict.values() )
    print "all dice status:", self.allRealDiceStatus
    self.gameLoop( playerNumber, diceNumber, trainingNumber, self.playerToDiceStatusDict )


if __name__ == '__main__':
  LiarDiceGame().run()
