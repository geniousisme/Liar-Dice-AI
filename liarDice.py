#encoding:utf-8
# -*- coding: utf-8 -*- 
import sys
import dice
# from prob import ProbAgent
from newProb  import ProbAgent
from training import UpdateStatusClass
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
    self.lastPlayer              = None
    self.catchPlayer             = None
    self.prevYell                = None # add func to record
    self.playerWinStatistics     = {}
    self.playerLoseStatistics    = {}
    self.credibility_list        = {1:1,2:0.1,3:0.1}
    
  def buildYellNOneTuple(self, yellTuple, oneAppear):
    return (yellTuple, oneAppear)

  def readCommand(self):
    argList = sys.argv
    if len( argList ) >= 1:
      playerNumber   = int( argList[ argList.index('-p') + 1 ] ) if '-p' in argList else 3  #-p: player
      diceNumber     = int( argList[ argList.index('-d') + 1 ] ) if '-d' in argList else 5  #-d: dice 
      trainingNumber = int( argList[ argList.index('-t') + 1 ] ) if '-t' in argList else 1 #-t: training
    return [ playerNumber, diceNumber, trainingNumber ] 
  
  def recordPlayerYell(self, playerOrder, yellNOneTuple):
    if self.playerYellHistory.has_key( playerOrder ):
      self.playerYellHistory[ playerOrder ].append( yellNOneTuple )
    else:
      self.playerYellHistory[ playerOrder ] = [ yellNOneTuple ]

  def recordCatchNLastPlayer(self, playerOrder, playerNumber):
    self.lastPlayer  = playerOrder - 1 if playerOrder != firstPlayerOrder else playerNumber
    self.catchPlayer = playerOrder

  def catchPlayerWin(self, catchPlayer, lastPlayer, isTraining):
    if not isTraining:  print "Successfully Catch!! Player", catchPlayer, "win this game!!"
    return [ catchPlayer, lastPlayer ]

  def lastPlayerWin(self, lastPlayer, catchPlayer, isTraining):
    if not isTraining:  print "Oops!! Lousy Catch!! Player", lastPlayer,  "win this game!!"
    return [ lastPlayer, catchPlayer ]

  def isTraining(self, trainingNumber):
    return True if trainingNumber > 1 else False

  def diceDot(self, diceStatusTuple):
    return diceStatusTuple[1]

  def diceDotNumber(self, diceStatusTuple):
    return diceStatusTuple[0]

  def oneAppearRule(self, prevYell, allRealDiceStatus):
    return True if self.diceDotNumber( prevYell ) > self.diceDotNumber( allRealDiceStatus[ self.diceDot( prevYell ) - 1 ] ) + self.diceDotNumber( allRealDiceStatus[ 0 ] ) else False

  def commonRule(self, prevYell, allRealDiceStatus):
    return True if self.diceDotNumber( prevYell ) > self.diceDotNumber( allRealDiceStatus[ self.diceDot( prevYell ) - 1 ] ) else False

  def gameResult(self, oneAppear, prevYell, allRealDiceStatus, catchPlayer, lastPlayer, isTraining ):
    print "gameResult"
    return ( self.catchPlayer( catchPlayer, lastPlayer, isTraining ) if self.oneAppearRule( prevYell, allRealDiceStatus ) else self.lastPlayerWin( lastPlayer, catchPlayer, isTraining ) ) if not oneAppear else ( self.catchPlayer( catchPlayer, lastPlayer, isTraining ) if self.commonRule( prevYell, allRealDiceStatus ) else self.lastPlayerWin( lastPlayer, catchPlayer, isTraining ) )
  
  def gameJudge(self, prevYell, allRealDiceStatus, oneAppear, catchPlayer, lastPlayer, trainingNumber):
    if not self.isTraining( trainingNumber ):
      print "oneAppear?", oneAppear
      print "allRealDiceStatus", allRealDiceStatus
    # winPlayer, losePlayer = self.gameResult( oneAppear, prevYell, allRealDiceStatus, catchPlayer, lastPlayer, self.isTraining( trainingNumber ) )
    if not oneAppear:
      if self.oneAppearRule( prevYell, allRealDiceStatus ):
        winPlayer, losePlayer = self.catchPlayerWin( catchPlayer, lastPlayer, self.isTraining( trainingNumber ) )
      else:
        winPlayer, losePlayer = self.lastPlayerWin( lastPlayer, catchPlayer, self.isTraining( trainingNumber ) )
    else:
      if self.commonRule( prevYell, allRealDiceStatus ):
        winPlayer, losePlayer = self.catchPlayerWin( catchPlayer, lastPlayer, self.isTraining( trainingNumber ) )
      else:
        winPlayer, losePlayer = self.lastPlayerWin( lastPlayer, catchPlayer, self.isTraining( trainingNumber ) )
    if self.isTraining( trainingNumber ): 
      print "Winer:", winPlayer,"Loser:", losePlayer
    if self.playerWinStatistics.has_key( winPlayer ):
      self.playerWinStatistics[ winPlayer ] += 1
    else:
      self.playerWinStatistics[ winPlayer ] = 1
    if self.playerLoseStatistics.has_key( losePlayer ):
      self.playerLoseStatistics[ losePlayer ] += 1
    else:
      self.playerLoseStatistics[ losePlayer ] = 1
    
  def gameLoop(self, playerNumber, diceNumber, trainingNumber, playerToDiceStatusDict, allRealDiceStatus):
    playerOrder = firstPlayerOrder
    hostile_player_num = playerNumber - 1
    dice_amount_per_player = diceNumber
    flag_one = False
    risk_rate = 0
    yell_threshold = 0.5
    catch_threshold = 0.2
    
    # A_Agent = ProbAgent( playerToDiceStatusDict[ 1 ], hostile_player_num, dice_amount_per_player, 0.05, 0.2, 0.0, credibility_list )
    # B_Agent = ProbAgent( playerToDiceStatusDict[ 2 ], hostile_player_num, dice_amount_per_player, 0.1,  0.2, 0.0, credibility_list )
    # C_Agent = ProbAgent( playerToDiceStatusDict[ 3 ], hostile_player_num, dice_amount_per_player, 0.15, 0.2, 0.2, credibility_list )
    # playerOrderToAgentDict = {1: A_Agent, 2: B_Agent, 3: C_Agent}
    # print "playerOrderToAgentDict", playerOrderToAgentDict
    playerOrder = roundNumber = 1
    oneAppear = False
    prevYell = None
    while True:
      A_Agent = ProbAgent( playerToDiceStatusDict[ 1 ], hostile_player_num, dice_amount_per_player, 0.15, 0.2, 0.0, self.credibility_list )
      B_Agent = ProbAgent( playerToDiceStatusDict[ 2 ], hostile_player_num, dice_amount_per_player, 0.05,  0.2, 0.0, self.credibility_list )
      C_Agent = ProbAgent( playerToDiceStatusDict[ 3 ], hostile_player_num, dice_amount_per_player, 0.1, 0.2, 0.0, self.credibility_list )
      playerOrderToAgentDict = {1: A_Agent, 2: B_Agent, 3: C_Agent}
      if not self.isTraining( trainingNumber ):
        print "########## Order of player", playerOrder #"Agent:", playerOrderToAgentDict[ playerOrder ]
        print "how many dice? 要不要抓?"
        print "prevYell:", prevYell
      if roundNumber == 1:
        decision = playerOrderToAgentDict[ playerOrder ].make_decision() 
      else:
        decision = playerOrderToAgentDict[ playerOrder ].make_decision(prevYell)
      if not self.isTraining( trainingNumber ):  print "decision:", decision
      yellTuple, Catch = decision
      if not Catch: prevYell = yellTuple 
      if self.diceDot( yellTuple ) == 1 and oneAppear == False:
        for agent in playerOrderToAgentDict.values():
          agent.update_status(playerOrder, yellTuple, True)
        oneAppear = True
      else:
        updateAgentList = [ agent for agent in playerOrderToAgentDict.values() if agent != playerOrderToAgentDict[ playerOrder ] ]
        for agent in updateAgentList:
          agent.update_status(playerOrder, yellTuple, False)

      if not self.isTraining( trainingNumber ):  print "yellTuple:", yellTuple, "Catch", Catch
      yellNOneTuple = self.buildYellNOneTuple( yellTuple, oneAppear )
      if not self.isTraining( trainingNumber ):  print yellNOneTuple, Catch
      self.recordPlayerYell(playerOrder, yellNOneTuple)

      if Catch:
        self.recordCatchNLastPlayer( playerOrder, playerNumber )
        if not self.isTraining( trainingNumber ):
          print "Game Over, start showing result"
          print "catchPlayer:", self.catchPlayer
          print "lastPlayer:", self.lastPlayer
          print "playerYellHistory:", self.playerYellHistory
          print "prevYell", prevYell
        self.gameJudge( prevYell, allRealDiceStatus, oneAppear, self.catchPlayer, self.lastPlayer, trainingNumber )
        break
      else:
        if playerOrder < playerNumber:
          playerOrder += 1 # go to next playerOrder
        else:
          playerOrder = firstPlayerOrder
      roundNumber += 1

  def run(self):  
    playerNumber, diceNumber, trainingNumber = self.readCommand()
    for training in xrange( 1, trainingNumber + 1 ):
      if not self.isTraining( trainingNumber ):  
        print "playerNumber:", playerNumber, "diceNumber:", diceNumber
      else:
        print "training:", training
      self.playerToDiceStatusDict = dice.generate( self.playerToDiceStatusDict, playerNumber, diceNumber )
      self.allRealDiceStatus      = dice.allReallDiceStatusCount( self.playerToDiceStatusDict.values() )
      if not self.isTraining( trainingNumber ):  print "all dice status:", self.allRealDiceStatus
      self.gameLoop( playerNumber, diceNumber, trainingNumber, self.playerToDiceStatusDict, self.allRealDiceStatus )
    if self.isTraining( trainingNumber ): 
      print "playerWinStatistics:", self.playerWinStatistics
      for player, winNumber in self.playerWinStatistics.items():
        print "player:", player,",",winNumber,"/",trainingNumber," = ", float( winNumber )/ trainingNumber * 100,"%"
      print "playerLoseStatistics:", self.playerLoseStatistics
      for player, loseNumber in self.playerLoseStatistics.items():
        print "player:", player,",",loseNumber,"/",trainingNumber," = ", float( loseNumber )/ trainingNumber * 100,"%"


if __name__ == '__main__':
  LiarDiceGame().run()
