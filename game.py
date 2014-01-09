class Game:
	def __init__(self):
		self.catchThreshold = None
		self.yellThreshold = None
		self.agentYell = {}
		self.probTable = {}

	def characterSetting(self):
		print "characterSetting"

	def run( self ):
    """
    Main control loop for game play.
    """
    self.display.initialize(self.state.data)
    self.numMoves = 0

    ###self.display.initialize(self.state.makeObservation(1).data)
    # inform learning agents of the game start
    for i in range(len(self.agents)):
      agent = self.agents[i]
      if not agent:
        self.mute(i)
        # this is a null agent, meaning it failed to load
        # the other team wins
        print "Agent %d failed to load" % i
        self.unmute()
        self._agentCrash(i, quiet=True)
        return
      if ("registerInitialState" in dir(agent)):
        self.mute(i)
        if self.catchExceptions:
          try:
            timed_func = TimeoutFunction(agent.registerInitialState, int(self.rules.getMaxStartupTime(i)))
            try:
              start_time = time.time()
              timed_func(self.state.deepCopy())
              time_taken = time.time() - start_time
              self.totalAgentTimes[i] += time_taken
            except TimeoutFunctionException:
              print "Agent %d ran out of time on startup!" % i
              self.unmute()
              self.agentTimeout = True
              self._agentCrash(i, quiet=True)
              return
          except Exception,data:
            self._agentCrash(i, quiet=False)
            self.unmute()
            return
        else:
          agent.registerInitialState(self.state.deepCopy())
        ## TODO: could this exceed the total time
        self.unmute()

    agentIndex = self.startingIndex
    numAgents = len( self.agents )

    while not self.gameOver:
      # Fetch the next agent
      agent = self.agents[agentIndex]
      move_time = 0
      skip_action = False
      # Generate an observation of the state
      if 'observationFunction' in dir( agent ):
        self.mute(agentIndex)
        if self.catchExceptions:
          try:
            timed_func = TimeoutFunction(agent.observationFunction, int(self.rules.getMoveTimeout(agentIndex)))
            try:
              start_time = time.time()
              observation = timed_func(self.state.deepCopy())
            except TimeoutFunctionException:
              skip_action = True
            move_time += time.time() - start_time
            self.unmute()
          except Exception,data:
            self._agentCrash(agentIndex, quiet=False)
            self.unmute()
            return
        else:
          observation = agent.observationFunction(self.state.deepCopy())
        self.unmute()
      else:
        observation = self.state.deepCopy()

      # Solicit an action
      action = None
      self.mute(agentIndex)
      if self.catchExceptions:
        try:
          timed_func = TimeoutFunction(agent.getAction, int(self.rules.getMoveTimeout(agentIndex)) - int(move_time))
          try:
            start_time = time.time()
            if skip_action:
              raise TimeoutFunctionException()
            action = timed_func( observation )
          except TimeoutFunctionException:
            print "Agent %d timed out on a single move!" % agentIndex
            self.agentTimeout = True
            self._agentCrash(agentIndex, quiet=True)
            self.unmute()
            return

          move_time += time.time() - start_time

          if move_time > self.rules.getMoveWarningTime(agentIndex):
            self.totalAgentTimeWarnings[agentIndex] += 1
            print "Agent %d took too long to make a move! This is warning %d" % (agentIndex, self.totalAgentTimeWarnings[agentIndex])
            if self.totalAgentTimeWarnings[agentIndex] > self.rules.getMaxTimeWarnings(agentIndex):
              print "Agent %d exceeded the maximum number of warnings: %d" % (agentIndex, self.totalAgentTimeWarnings[agentIndex])
              self.agentTimeout = True
              self._agentCrash(agentIndex, quiet=True)
              self.unmute()

          self.totalAgentTimes[agentIndex] += move_time
          #print "Agent: %d, time: %f, total: %f" % (agentIndex, move_time, self.totalAgentTimes[agentIndex])
          if self.totalAgentTimes[agentIndex] > self.rules.getMaxTotalTime(agentIndex):
            print "Agent %d ran out of time! (time: %1.2f)" % (agentIndex, self.totalAgentTimes[agentIndex])
            self.agentTimeout = True
            self._agentCrash(agentIndex, quiet=True)
            self.unmute()
            return
          self.unmute()
        except Exception,data:
          self._agentCrash(agentIndex)
          self.unmute()
          return
      else:
        action = agent.getAction(observation)
      self.unmute()

      # Execute the action
      self.moveHistory.append( (agentIndex, action) )
      if self.catchExceptions:
        try:
          self.state = self.state.generateSuccessor( agentIndex, action )
        except Exception,data:
          self.mute(agentIndex)
          self._agentCrash(agentIndex)
          self.unmute()
          return
      else:
        self.state = self.state.generateSuccessor( agentIndex, action )

      # Change the display
      self.display.update( self.state.data )
      ###idx = agentIndex - agentIndex % 2 + 1
      ###self.display.update( self.state.makeObservation(idx).data )

      # Allow for game specific conditions (winning, losing, etc.)
      self.rules.process(self.state, self)
      # Track progress
      if agentIndex == numAgents + 1: self.numMoves += 1
      # Next agent
      agentIndex = ( agentIndex + 1 ) % numAgents

      if _BOINC_ENABLED:
        boinc.set_fraction_done(self.getProgress())

    # inform a learning agent of the game result
    for agent in self.agents:
      if "final" in dir( agent ) :
        try:
          self.mute(agent.index)
          agent.final( self.state )
          self.unmute()
        except Exception,data:
          if not self.catchExceptions: raise
          self._agentCrash(agent.index)
          self.unmute()
          return
    self.display.finish()
