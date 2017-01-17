# play.py
# Nicolas Barone(njb227) Jineet Patel(jjp257)
# 12/08/2016
# used Walker White's code from arrows.py as a reference 
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """   
    def getBricks(self):
        """Returns: the list of bricks initiaized in Play. """
        return self._bricks
    def __init__(self):
        """**Constructor**: intitilaizes play by assigning values to specific attributes.
        Method makes sure all the invariants are satisfied for the attributes. """
        i = 0
        acc = []
        for i in range(0,10):
            for j in range(0,10):
                new = Brick(i,j)
                acc.append(new)
        self._bricks = acc
        paddle = Paddle()
        self._paddle = paddle   
        self._ball = None
        self._tries = NUMBER_TURNS
        self._image1 = Beach(x= 230)
        self._image2 = Beach(x = 100)
        self._image3 = Beach(x = 350)
        self._text = GLabel( text='poof!', x = 200, y = 350,
                            font_name = "Zapfino.ttf")
        # self._image = None)
      
    def draw(self, view):
        """Draws the game objects to the application screen.
        Draws the bricks, paddle, and ball as necessary.
        
        Parameter: The view window
        Precondition: view is a GView."""
        for i in self._bricks:
            i.draw(view)
        self._paddle.draw(view)
        self._image1.draw(view)
        self._image2.draw(view)
        self._image3.draw(view)
        if self._ball is not None:
            self._ball.draw(view)
        
    def updatePaddle(self,input):
        """Animates the paddle.
        
        Parameter input: the input of the user
        Precondition: input is a GObject."""
        # used Walker White's code from arrows.py as a reference 
        x = 6
        da = 0
        dy = 0
        if input.is_key_down('left'):
            da -= x
        if input.is_key_down('right'):
            da += x
        posx = self._paddle.getX() + da
        self._paddle.setX(posx) 
        self._paddle.setX(max(self._paddle.getX(), PADDLE_WIDTH/2))
        self._paddle.setX(min(self._paddle.getX(), GAME_WIDTH-PADDLE_WIDTH/2))
        #EXTENISON allows user to move the paddle up and down up until GAME_HEIGHT/4
        # and bellow until PADDLE_OFFSET+PADDLE_HEIGHT/2
        if input.is_key_down('down'):
            dy -= x
        if input.is_key_down('up'):
            dy += x
        posy = self._paddle.getY() + dy
        self._paddle.setY(posy)
        self._paddle.setY(min(self._paddle.getY(), GAME_HEIGHT/4))
        self._paddle.setY(max(self._paddle.getY(),
        PADDLE_OFFSET + PADDLE_HEIGHT/2))
    
    def makeBall(self):
        """makes a ball only when it is called upon in breakout."""
        self._ball = Ball()
    
    def updateBall(self):
        """ updates ball's position to make it move across the screen.
            Checks if ball and paddle collides with either paddle or brick.
            If it collides with bricks removes brick from screen and negates
            the y velocity of the ball. If it collides with the paddle it
            negates the y velocity of the ball and if it hits edges of the
            paddle it also reverse x velocity"""
            #Extension here check
        self._ball.moveBall()
        if self._paddle.collides(self._ball):
            self._ball.setColor()
            self._ball.setVy(-self._ball.getVy())
            if ((self._ball.getX() + BALL_DIAMETER/2) >=
                (self._paddle.getX() + PADDLE_WIDTH/4)):
                self._ball.setVx(-self._ball.getVx())
            elif ((self._ball.getX() - BALL_DIAMETER/2) <=
                (self._paddle.getX() - PADDLE_WIDTH/4)):
                self._ball.setVx(-self._ball.getVx())
        if self._image1.collides(self._ball):
            self._ball.setVy(-self._ball.getVy())
        if self._image2.collides(self._ball):
            self._ball.setVy(-self._ball.getVy())
        if self._image3.collides(self._ball):
            self._ball.setVy(-self._ball.getVy())
        x = -1
        for i in range(len(self._bricks)):
            if self._bricks[i].collides(self._ball):
              
                self._ball.setVy(-self._ball.getVy())
                self._ball.setColor()
                self._ball.setVx(random.uniform(1.0,5.0))
                x = i 
                self._bricks.remove(self._bricks[x])
                return
                
    def MoveBall(self):
        """calls upon method for the class ball in Models.py to change the
        x and y position by adding the x and y velocities."""
        self._ball.BounceBall()
        
    def SoundUp(self):
        """Load an audio file by creating a sound object then calling
        it for use in Breakout.py"""
        bounceSound = Sound('bounce.wav')
        bounceSound.play()
    
    def gameFail(self):
        """Returns: True or False depending on whether
        the ball passes the bottom of the screen. If ball is below the screen
        calls upon ball method found in Models.py."""
        #entension removes ball from view
        if (self._ball.getY() - BALL_DIAMETER/2) <= 0:
            self._ball.removeBall()
            return True
        return False
    
