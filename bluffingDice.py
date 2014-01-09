#!/usr/bin/python 
import sys
import game

############################################################################
#                     THE HIDDEN SECRETS OF PACMAN                         #
#                                                                          #
# You shouldn't need to look through the code in this section of the file. #
############################################################################

class ClassicGameRules:
  """
  These game rules manage the control flow of a game, deciding when
  and how the game starts and ends.
  """
  def __init__(self, timeout=30):
    self.timeout = timeout

  def newGame( self, layout, pacmanAgent, ghostAgents, display, quiet = False, catchExceptions=False):
    agents = [pacmanAgent] + ghostAgents[:layout.getNumGhosts()]
    initState = GameState()
    initState.initialize( layout, len(ghostAgents) )
    game = Game(agents, display, self, catchExceptions=catchExceptions)
    game.state = initState
    self.initialState = initState.deepCopy()
    self.quiet = quiet
    return game

  def process(self, state, game):
    """
    Checks to see whether it is time to end the game.
    """
    if state.isWin(): self.win(state, game)
    if state.isLose(): self.lose(state, game)

  def win( self, state, game ):
    if not self.quiet: print "Pacman emerges victorious! Score: %d" % state.data.score
    game.gameOver = True

  def lose( self, state, game ):
    if not self.quiet: print "Pacman died! Score: %d" % state.data.score
    game.gameOver = True

  

def readCommand(argv):
  print "argv", argv

def runGame(args):
  print args
  # import __main__
  
  rules = ClassicGameRules(timeout)
  games = []

  for i in range( numGames ):
    beQuiet = i < numTraining
    if beQuiet:
        # Suppress output and graphics
        import textDisplay
        gameDisplay = textDisplay.NullGraphics()
        rules.quiet = True
    else:
        gameDisplay = display
        rules.quiet = False
    game = rules.newGame( layout, pacman, ghosts, gameDisplay, beQuiet, catchExceptions)
    game.run()
    if not beQuiet: games.append(game)

    if record:
      import time, cPickle
      fname = ('recorded-game-%d' % (i + 1)) +  '-'.join([str(t) for t in time.localtime()[1:6]])
      f = file(fname, 'w')
      components = {'layout': layout, 'actions': game.moveHistory}
      cPickle.dump(components, f)
      f.close()

  if numGames > 1:
    scores = [game.state.getScore() for game in games]
    wins = [game.state.isWin() for game in games]
    winRate = wins.count(True)/ float(len(wins))
    print 'Average Score:', sum(scores) / float(len(scores))
    print 'Scores:       ', ', '.join([str(score) for score in scores])
    print 'Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), winRate)
    print 'Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins])

  return games

if __name__ == '__main__':
    args = readCommand(sys.argv[1:])
    runGame(**args)