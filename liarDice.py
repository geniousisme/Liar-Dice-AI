#encoding:utf-8
# -*- coding: utf-8 -*- 
import sys
import dice
import params
# from prob import ProbAgent
from newProb  import ProbAgent
from training import *

import time
# import game
notOne = False
isOne  = True
firstPlayerOrder = 1
UpdateStatusTT = 1
UpdateStatusOO = 2
defaultDict = {1:0, 2:0, 3:0}

def dictSubstract(dict1, dict2):
  return { key: dict1[key] - dict2.get(key, 0) for key in dict1.keys() }

def dictAdd(dict1, dict2):
  return { key: dict1[key] + dict2.get(key, 0) for key in dict1.keys() }



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
    self.playerCatchWinStatistics      = {}
    self.playerCatchLoseStatistics     = {}
    self.playerToCredibilityDict  = { 1:0.1, 2:0.1, 3:0.1 } #1:0 代表其他agent完全不相信
    self.playerAToCredibilityDict = { 1:0.1, 2:0.1, 3:0.1 } 
    self.playerBToCredibilityDict = { 1:0.1, 2:0.1, 3:0.1 } 
    self.playerCToCredibilityDict = { 1:0.1, 2:0.1, 3:0.1 } 
    self.isQuite                 = False
    self.updateAgent             = 'all'

    
  def buildYellNOneTuple(self, yellTuple, oneAppear):
    return (yellTuple, oneAppear)

  def readCommand(self):
    argList = sys.argv
    if len( argList ) >= 1:
      playerNumber   = int( argList[ argList.index('-p') + 1 ] ) if '-p' in argList else 3  #-p: player
      diceNumber     = int( argList[ argList.index('-d') + 1 ] ) if '-d' in argList else 5  #-d: dice 
      trainingNumber = int( argList[ argList.index('-t') + 1 ] ) if '-t' in argList else 1  #-t: training
      isLearning     = True if '-l' in argList else False
      
      if isLearning: 
        self.learningSwitch = int( argList[ argList.index('-l') + 1 ] )
        self.updateAgent = argList[ argList.index('-a') + 1 ] if '-a' in argList else 'all'

      self.isQuite   = True if '-q' in argList else False
      
    return [ playerNumber, diceNumber, trainingNumber, isLearning ] 
  
  def recordPlayerYell(self, playerOrder, yellNOneTuple):
    if self.playerYellHistory.has_key( playerOrder ):
      self.playerYellHistory[ playerOrder ].append( yellNOneTuple )
    else:
      self.playerYellHistory[ playerOrder ] = [ yellNOneTuple ]

  def recordCatchNLastPlayer(self, playerOrder, playerNumber):
    self.lastPlayer  = playerOrder - 1 if playerOrder != firstPlayerOrder else playerNumber
    self.catchPlayer = playerOrder

  def recordStatistics(self, playerType, statisticsTypeDict):
    if self.statisticsTypeDict.has_key( playerType ):
      self.statisticsTypeDict[ playerType ] += 1
    else:
      self.statisticsTypeDict[ playerType ] = 1

  def recordWinStatics(self, winPlayer):
    if self.playerWinStatistics.has_key( winPlayer ):
      self.playerWinStatistics[ winPlayer ] += 1
    else:
      self.playerWinStatistics[ winPlayer ] = 1

  def recordLoseStatics(self, losePlayer):
    if self.playerLoseStatistics.has_key( losePlayer ):
      self.playerLoseStatistics[ losePlayer ] += 1
    else:
      self.playerLoseStatistics[ losePlayer ] = 1

  def recordCatchWinStatistics(self, catchWinPlayer):
    if self.playerCatchWinStatistics.has_key( catchWinPlayer ):
      self.playerCatchWinStatistics[ catchWinPlayer ] += 1
    else:
      self.playerCatchWinStatistics[ catchWinPlayer ] = 1

  def recordCatchLoseStatistics(self, catchLosePlayer):
    if self.playerCatchLoseStatistics.has_key( catchLosePlayer ):
      self.playerCatchLoseStatistics[ catchLosePlayer ] += 1
    else:
      self.playerCatchLoseStatistics[ catchLosePlayer ] = 1

  def catchPlayerWin(self, catchPlayer, lastPlayer, isTraining):
    if not isTraining:  
      print
      print "Successfully Catch!! Player", catchPlayer, "win this game!!"
      print "############"
      print "# Winer:", catchPlayer, "#"
      print "# Loser:", lastPlayer, "#"
      print "############"
    return [ catchPlayer, lastPlayer ]

  def lastPlayerWin(self, lastPlayer, catchPlayer, isTraining):
    if not isTraining:  
      print
      print "Oops!! Lousy Catch!! Player", lastPlayer,  "win this game!!"
      print "############"
      print "# Winer:", lastPlayer, "#"
      print "# Loser:", catchPlayer, "#"
      print "############"
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
    catchWinPlayer = catchLosePlayer = yellWinPlayer = yellLosePlayer = None
    if not oneAppear:
      if self.oneAppearRule( prevYell, allRealDiceStatus ):
        winPlayer, losePlayer = self.catchPlayerWin( catchPlayer, lastPlayer, self.isTraining( trainingNumber ) )
        self.recordCatchWinStatistics( winPlayer )
      else:
        winPlayer, losePlayer = self.lastPlayerWin( lastPlayer, catchPlayer, self.isTraining( trainingNumber ) )
        self.recordCatchLoseStatistics( losePlayer )
    else:
      if self.commonRule( prevYell, allRealDiceStatus ):
        winPlayer, losePlayer = self.catchPlayerWin( catchPlayer, lastPlayer, self.isTraining( trainingNumber ) )
        self.recordCatchWinStatistics( winPlayer )
      else:
        winPlayer, losePlayer = self.lastPlayerWin( lastPlayer, catchPlayer, self.isTraining( trainingNumber ) )
        self.recordCatchLoseStatistics( losePlayer )

    if self.isTraining( trainingNumber ): 
      if not self.isQuite:  print "Winer:", winPlayer,"Loser:", losePlayer
      self.recordWinStatics(  winPlayer  )
      self.recordLoseStatics( losePlayer )
     

  def gameLoop(self, playerNumber, diceNumber, trainingNumber, isLearning, playerToDiceStatusDict, allRealDiceStatus):
    playerOrder = firstPlayerOrder
    hostile_player_num = playerNumber - 1
    dice_amount_per_player = diceNumber
    flag_one = False
    risk_rate = 0
    yell_threshold = 0.5
    catch_threshold = 0.2
    playerOrder = roundNumber = 1
    oneAppear = False
    prevYell = None
    ARiskRate, ACatchThreshold, AYellOneProb = params.agentParamsOf('A')
    BRiskRate, BCatchThreshold, BYellOneProb = params.agentParamsOf('B')
    CRiskRate, CCatchThreshold, CYellOneProb = params.agentParamsOf('C')
    while True:
      A_Agent = ProbAgent( playerToDiceStatusDict[ 1 ], hostile_player_num, dice_amount_per_player, ARiskRate, ACatchThreshold, AYellOneProb, self.playerToCredibilityDict )
      B_Agent = ProbAgent( playerToDiceStatusDict[ 2 ], hostile_player_num, dice_amount_per_player, BRiskRate, BCatchThreshold, BYellOneProb, {1:0.1, 2:0.1, 3:0.1} )
      C_Agent = ProbAgent( playerToDiceStatusDict[ 3 ], hostile_player_num, dice_amount_per_player, CRiskRate, CCatchThreshold, CYellOneProb, {1:0.1, 2:0.1, 3:0.1} )
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
          print
          print "###################################"
          print "# Game Over, start showing result #"
          print "###################################"
          print
          print "catchPlayer:", self.catchPlayer
          print "lastPlayer:", self.lastPlayer
          print "playerYellHistory:", self.playerYellHistory
          print "prevYell", prevYell
        self.gameJudge( prevYell, allRealDiceStatus, oneAppear, self.catchPlayer, self.lastPlayer, trainingNumber )
        if isLearning:
          # learning = UpdateStatusTang( allRealDiceStatus, self.playerYellHistory, self.playerToCredibilityDict.values(), 0.8 )
          learning = UpdateStatusTang( allRealDiceStatus, self.playerYellHistory, self.playerToCredibilityDict.values(), params.learningRate( UpdateStatusTT ) ) if self.learningSwitch == UpdateStatusTT else UpdateStatusChuan( allRealDiceStatus, self.playerYellHistory, self.playerToCredibilityDict.values(), params.learningRate( UpdateStatusOO ) )
          # if self.learningSwitch == UpdateStatusTT:
          #   learning = UpdateStatusTang( allRealDiceStatus, self.playerYellHistory, self.playerToCredibilityDict.values(), 0.8 )
          # elif self.learningSwitch == UpdateStatusOO:
          #   learning = UpdateStatusChuan( allRealDiceStatus, self.playerYellHistory, self.playerToCredibilityDict.values(), 0.8 )
          newCredibilityList = learning.calcDistanceFromHistoryList()
          if self.updateAgent == 'all':
            self.playerToCredibilityDict = dict( enumerate( newCredibilityList, start = 1 ) )
          elif self.updateAgent == 'A':
            self.playerToCredibilityDict[1] = newCredibilityList[0]
          elif self.updateAgent == 'B':
            self.playerToCredibilityDict[2] = newCredibilityList[1]
          elif self.updateAgent == 'C':
            self.playerToCredibilityDict[3] = newCredibilityList[2]
          if not self.isQuite:  print "playerToCredibilityDict:", self.playerToCredibilityDict
        break
      else:
        if playerOrder < playerNumber:
          playerOrder += 1 # go to next playerOrder
        else:
          playerOrder = firstPlayerOrder
      roundNumber += 1

  def showStatisticsResult(self, playerStatistics, denominator, playerStatisticsType):
    print playerStatisticsType, playerStatistics   

  def run(self):  
    playerNumber, diceNumber, trainingNumber, isLearning = self.readCommand()
    for training in xrange( 1, trainingNumber + 1 ):
      if not self.isTraining( trainingNumber ):  
        print "playerNumber:", playerNumber, "diceNumber:", diceNumber
      else:
        if not self.isQuite:  print "training:", training
      self.playerToDiceStatusDict = dice.generate( self.playerToDiceStatusDict, playerNumber, diceNumber )
      self.allRealDiceStatus      = dice.allReallDiceStatusCount( self.playerToDiceStatusDict.values() )
      if not self.isTraining( trainingNumber ):  print "all dice status:", self.allRealDiceStatus
      self.gameLoop( playerNumber, diceNumber, trainingNumber, isLearning, self.playerToDiceStatusDict, self.allRealDiceStatus )
    if self.isTraining( trainingNumber ): 
      print "playerWinStatistics:", self.playerWinStatistics
      for player, winNumber in self.playerWinStatistics.items():
        print "player:", player,",",winNumber,"/",trainingNumber," = ", float( winNumber )/ trainingNumber * 100,"%"
      
      print "playerLoseStatistics:", self.playerLoseStatistics
      for player, loseNumber in self.playerLoseStatistics.items():
        print "player:", player,",",loseNumber,"/",trainingNumber," = ", float( loseNumber )/ trainingNumber * 100,"%"

      playerCatchStatistics = dictAdd( self.playerCatchLoseStatistics, self.playerCatchWinStatistics )
      print "playerCatchWinStatistics:", self.playerCatchWinStatistics
      for player, winNumber in self.playerCatchWinStatistics.items():
        print "player:", player,",",winNumber,"/",trainingNumber," = ", float( winNumber )/ trainingNumber * 100,"%"
        if playerCatchStatistics.has_key( player ) and playerCatchStatistics[ player ] != 0 :
          print "player:", player,",",winNumber,"/", playerCatchStatistics[ player ]," = ", float( winNumber )/ playerCatchStatistics[ player ] * 100,"%"
        else:
          print "player:", player, "catch 0 times."

      print "playerCatchLoseStatistics:", self.playerCatchLoseStatistics
      for player, loseNumber in self.playerCatchLoseStatistics.items():
        print "player:", player,",",loseNumber,"/",trainingNumber," = ", float( loseNumber )/ trainingNumber * 100,"%"
        if playerCatchStatistics.has_key( player ) and playerCatchStatistics[ player ] != 0:
          print "player:", player,",",loseNumber,"/",playerCatchStatistics[ player ]," = ", float( loseNumber )/ playerCatchStatistics[ player ] * 100,"%"
        else:
          print "player:", player, "catch 0 times."
      
      playerYellWinStatistics = dictSubstract( self.playerWinStatistics, self.playerCatchWinStatistics )
      playerYellLoseStatistics = dictSubstract( self.playerLoseStatistics, self.playerCatchLoseStatistics )
      playerYellStatistics = dictAdd( playerYellWinStatistics, playerYellLoseStatistics )
      print "playerYellWinStatistics:", playerYellWinStatistics
      for player, winNumber in playerYellWinStatistics.items():
        if playerYellStatistics.has_key( player ) and playerYellStatistics[ player ] != 0:
          print "player:", player,",",winNumber,"/",playerYellStatistics[ player ]," = ", float( winNumber )/ playerYellStatistics[ player ] * 100,"%"
        else:
          print "player:", player, "yell 0 times."
      
      print "playerYellLoseStatistics:", playerYellLoseStatistics
      for player, loseNumber in playerYellLoseStatistics.items():
        if playerYellStatistics.has_key( player ) and playerYellStatistics[ player ] != 0:
          print "player:", player,",",loseNumber,"/",playerYellStatistics[ player ]," = ", float( loseNumber )/ playerYellStatistics[ player ] * 100,"%"
        else:
           print "player:", player, "yell 0 times."

      if self.updateAgent == 'all':
        print "self.playerToCredibilityDict:", self.playerToCredibilityDict 
      elif self.updateAgent == 'A':
        print "agentA:", self.playerToCredibilityDict[1] 
      elif self.updateAgent == 'B':
        print "agentB:", self.playerToCredibilityDict[2]
      elif self.updateAgent == 'C':
        print "agentC:", self.playerToCredibilityDict[3]

if __name__ == '__main__':
  LiarDiceGame().run()
