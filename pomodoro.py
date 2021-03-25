# Import logging
import logging
from time import monotonic
from threading import Timer

#states
IDLE = 0
WORK = 1
BREAK_ALARM = 2
SHORT_BREAK = 3
WORK_ALARM = 4
LONG_BREAK = 5

class Pomodoro:
  
  def __init__(self):
    logging.debug("Construct pomodoro object")
    self._pressStatus = False
    self.workDuration = 10
    self._timerDuration = 0
    self.timerStart = 0
    self.breakDuration = 5
    self.numberCycles = 3
    self.cycleCounter = 0
    self.setup()
    

  def setup(self):
    logging.debug("Setup")
    self.currentState = IDLE
  
  def checkState(self):
    logging.debug("Check state")
    # Create an object Timer which wait 1 second before calling the method checkState and keep track of it in the attribute _nextCheck
    self._nextCheck = Timer(1, self.checkState)
    # Start the timer
    self._nextCheck.start()
    if self.currentState == IDLE:
        if self.isPressed():
            self.startWork()
    elif self.currentState == WORK:
        if self.isTimeOver():
            self.ringBreakAlarm()
    elif self.currentState == BREAK_ALARM:
        if self.isPressed():
          if self.isTimeForLongBreak():
            self.startLongBreak()
          else:
            self.startShortBreak()
    elif self.currentState == SHORT_BREAK:
        if self.isTimeOver():
            self.ringWorkAlarm()
    elif self.currentState == WORK_ALARM:
        if self.isPressed():
            self.startWork()
    elif self.currentState == LONG_BREAK:
        if self.isPressed():
            self.pause()
    else:
        # Log a warning with the state
        logging.warn("Invalid state: " + self.currentState)
      
  			
  def start(self):
    logging.debug("Start Pomodoro")
    self.checkState()
  
  def stop(self):
    logging.debug("Stop Pomodoro")
    # If a timer has been constructed and waiting for the next second
    if self._nextCheck is not None:
      # Cancel the timer
      self._nextCheck.cancel()

  def changeState(self, state):
    """
    for changing states 
    state =  the new state
    """
    logging.debug("NEW STATE")
    self.currentState = state
    

  def startWork(self):
    logging.debug("Start work")
    self._timerDuration = self.workDuration
    self._timerStart = monotonic()
    self.changeState(WORK)

  def ringBreakAlarm(self):
    logging.debug("Ring break alarm")
    self.changeState(BREAK_ALARM)


  def startShortBreak(self):
    logging.debug("Start short break")
    self._timerDuration = self.breakDuration
    self.timerStart = monotonic()
    self.cycleCounter += 1
    self.changeState(SHORT_BREAK)

  def ringWorkAlarm(self):
    logging.debug("Ring work alarm")
    self.changeState(WORK_ALARM)

  def startLongBreak(self):
    logging.debug("Start long break")
    self.cycleCounter = 0
    self.changeState(LONG_BREAK)


  def pause(self):
    logging.debug("Pause")
    self.changeState(IDLE)

  def isPressed(self):
    logging.debug("Is Pressed?")
    if self._pressStatus:
      # Switch back button status to False, so that it is taken into account only once
      self._pressStatus = False
      return True
    return False


  def press(self):
    """
      Use _buttonStatus as a flag so that for the next check state the button is 'pressed'.
    """
    logging.debug("Pomodoro pressed")
    self._pressStatus = True

  def isTimeOver(self):
    logging.debug("Is time over?")
    return monotonic() - self._timerStart > self._timerDuration


  def isTimeForLongBreak(self):
    logging.debug("Is time for long break?")
    return self._cycleCounter >= self.numberCycles