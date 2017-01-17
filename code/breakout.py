# breakout.py
# Nicolas Barone(njb227) Jineet Patel(jjp257)
# 12/08/2016
#used Walker White's code for determineState(self) from state.py
#used Walker White's code for updatePaddle() from arrows.py
#used code from state.py as a reference for chaning states in update(self)
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
         view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
        _time   [int >= 0, 0 if state changed]:
            frames since state last changed (pressed, released) 
        _pause  [GLabel, or None if there is no message to display]
                the message when user loses a life 
        _lose   [GLabel, or None if game isn't complete]
        _3      [GLabel, or None if game isn't a countdown before the game is started or restarted if a life was lost]
        _lives	[int <= NUMBER_TURNS, 3 if no lives have been lost]
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
        Attribute _pause is only not None if _state is STATE_PAUSED 
        
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """

    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""

        self._state =  STATE_INACTIVE
        self._game = None
        self._mssg = GLabel( text='press any key to play', x = 200, y = 350,
                            font_name = "Zapfino.ttf")
        # self._image = None
        self._time = 0
        self._pause = None
        self._lose = None
        self._3 = None
        self._lives = NUMBER_TURNS
              
    def update(self,dt):
        #used code from state.py as a reference for chaning states
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
       
        x = NUMBER_TURNS
        self._determineState()
        if self._state == STATE_NEWGAME:
            self._mssg = None
            self._game = Play()
            self._game.updatePaddle(self.input)
        elif self._state == STATE_COUNTDOWN:
            self._Countdown()
        elif self._state == STATE_ACTIVE:
            # self._image = GImage(x = 230, y = 20, width = 40, height = 20, source='beach-ball.png')
            self._3 = None
            self._game.updatePaddle(self.input)
            self._game.updateBall()
            self._game.MoveBall()
            self.messages()
        elif self._state == STATE_COMPLETE:
            self._3 = None 
            if len(self._game.getBricks()) == 0:
                self._lose = GLabel(
                    text='Congrats, 70,000$ later, and you won a game of breakout.'
                , x = 200, y = 350, font_name = "ArialBold.ttf", font_size = 15)
            else:
                self._lose =GLabel(
                    text='You lost, Congradulations!',
                    x = 250, y = 350, font_name = "ArialBold.ttf", font_size = 20)
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""


        if self._mssg is not None:
            self._mssg.draw(self.view)

        elif self._pause is not None:
            self._pause.draw(self.view)

        elif self._game is not None:
            self._game.draw(self.view)

        if self._lose is not None:
            self._lose.draw(self.view)

        if self._3 is not None:
            self._3.draw(self.view)
        
        # if self._image is not None:
        #     self._image.draw(self.view)
    
    def _determineState(self):
        #used code from State.py file given by Walker White
        """Determines the current state and assigns it to self.state
        
        This method checks for a key press, and if there is one, changes the state 
        to the next value.  A key press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as we hold down the key.  The
        user must release the key and press it again to change the state."""


        curr_keys = self.input.key_count

        change = curr_keys > 0
        
        if change and self._state == STATE_INACTIVE:
            self._state = STATE_NEWGAME

        elif self._state == STATE_NEWGAME:
            self._state = STATE_COUNTDOWN
        elif change and self._state == STATE_PAUSED:
            self._state = STATE_COUNTDOWN
            
    def _Countdown(self):

        """Establishes a countdown for the game.
        
        It incrememts the timer and prints it. When the timer, and thus
        the # of frames,hits 180, the game ball is created and the state
        is changed to STATE_ACTIVE. If a player loses a life, the timer starts
        again at the previous count. When it hits 360, the game ball is created
        and the state is changed to STATE_ACTIVE. The same is done if the timer hits
        540. If the timer goes above 540, the state is changed to STATE_COMPLETE
        and the game has concluded.
        
        Extension within this allows for the countdown to appear in the game
        for 3 seconds, 2 seconds, and 1 seconds. """
        #(Extension here allows for countdown to display 3,2,1 everythime
        #the frame the game starts or the user loses a life and is ready
        #to play again.)
        x = NUMBER_TURNS
        self._time = self._time + 1
        self._pause = None
        self._game.updatePaddle(self.input)
        if self._time % 180 == 1:
            self._3 = GLabel( text='3', x = 200, y = 350,
                             font_name = "ArialBold.ttf", font_size = 50)
        elif self._time % 180 == 60:
            self._3 = GLabel( text='2', x = 200, y = 350,
                             font_name = "ArialBold.ttf", font_size = 50)
        elif self._time % 180 == 120:
            self._3 = GLabel( text='1', x = 200, y = 350,
                             font_name = "ArialBold.ttf", font_size = 50)
        elif self._time == 180:
            self._3 = None
            self._game.makeBall()
            self._state = STATE_ACTIVE
        elif self._time == 360:
            x = x - 1 
            self._game.makeBall()
            self._state = STATE_ACTIVE
        elif self._time == 540:
            x = x - 2
            self._game.makeBall()
            self._state = STATE_ACTIVE
        elif self._time > 540:
            self._state = STATE_COMPLETE
        
    def messages(self):
        """calls upon helper method that checks checks if the brick count gets
        into a certain range to display a message to the user. Also changed
        state depending on if specific method is evaluated to True or False.
        checks number of lives and if it reaches a certain point will display
        message. Checks brick count that if it is equal to zero changes state
        to STATE_COMPLETE to end the game."""
        # extension
        print len(self._game.getBricks())
        self.textDisplayed()
        if len(self._game.getBricks()) == 0:
                self._state = STATE_COMPLETE 
        if self._game.gameFail() == True:
                self._state = STATE_PAUSED
                print self._state
                print self._time 
        if self._state == STATE_PAUSED:
            print 'aaaaaaaaaaaa'
            self._lives = self._lives - 1
            if self._time >= 540:
                
                self._state = STATE_COMPLETE
            else:
                self._3 = None
                if self._time == 180:
                    self._3 = GLabel( text='Might wanto ask for help..',
                    x = 200,y = 350, font_name = "ArialBold.ttf", font_size = 20)
                    
                if self._time == 360:
                    self._3 = GLabel( text='You call yourself a consultant?',
                    x = 200,y = 350, font_name = "ArialBold.ttf", font_size = 20)
                
    def textDisplayed(self):
        """method checks if the brick length is between a certain range and if it is
        sets atrribute _3 to a message that temporarily displays during that range.
        If the brick length is in between a certain range will also call on sound
        method found in Play.py file and play the sound."""
        #extension that displays messages and plays sound 
        if 86 < len(self._game.getBricks()) < 95:
                self._3 = GLabel( text='Hey good for you', x = 200, y = 350,
                                 font_name = "ArialBold.ttf",font_size = 20)
        elif 80 < len(self._game.getBricks()) < 85:
                self._3 = GLabel( text='alright I see you',
                    x = 200, y = 350, font_name = "ArialBold.ttf",font_size = 20)
        elif 60 <len(self._game.getBricks()) < 65:
                self._3 = GLabel( text='Pretty lucky', x = 200, y = 350,
                                 font_name = "ArialBold.ttf", font_size = 20)
        elif 30 <len(self._game.getBricks()) < 35:
                self._3 = GLabel( text='Thats it! You will not Win!', x = 200,
                                 y = 350, font_name = "ArialBold.ttf",
                                 font_size = 20)
                self._game.SoundUp()
        elif 25 <len(self._game.getBricks()) < 30:
                self._3 = GLabel( text='Annoying Huh? I\'ll stop', x = 200, y = 350,
                                 font_name = "ArialBold.ttf", font_size = 20)
                
        elif 20 < len(self._game.getBricks()) < 25:
                self._3 = GLabel( text='JK..', x = 200, y = 350,
                                 font_name = "ArialBold.ttf", font_size = 20)
                self._game.SoundUp()
                
        
        
        