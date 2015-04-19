#encoding:utf-8
# -*- coding: utf-8 -*- 
import sys

class LiarDiceGame:

  def readCommand():
    # Sprint "arg:", sys.argv
    argList = sys.argv
    if len( argList ) >= 1:
      playerNumber = argList[ argList.index('-p') + 1 ] if '-p' in argList else 3 #-p: player
      diceNumber   = argList[ argList.index('-d') + 1 ] if '-d' in argList else 5 #-d: dice 

    return [ int(playerNumber), int(diceNumber) ] 

  def main():  
    playerNumber, diceNumber = readCommand()
    print "playerNumber:", playerNumber, "diceNumber:", diceNumber
    playerTurnCount = 1
    while True:
      print "Turn for player", playerTurnCount
      diceTuple, Catch = input("how many dice? & 有沒有1？ ")
      print diceTuple, Catch
      
      if Catch:
        print "Game Over, start showing result"
        break
      else:
        if playerTurnCount < playerNumber:
          # prisnt "playerTurnCount:", playerTurnCount, "playerNumber", playerNumber
          playerTurnCount += 1
        else:
          playerTurnCount = 1

def readCommand():
  # Sprint "arg:", sys.argv
  argList = sys.argv
  if len( argList ) >= 1:
    playerNumber = argList[ argList.index('-p') + 1 ] if '-p' in argList else 3 #-p: player
    diceNumber   = argList[ argList.index('-d') + 1 ] if '-d' in argList else 5 #-d: dice 

  return [ int(playerNumber), int(diceNumber) ]

if __name__ == '__main__':
  main()
