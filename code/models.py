# models.py
# Nicolas Barone(njb227) Jineet Patel(jjp257)
# 12/08/2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.
You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""   
import random 
from constants import *
from game2d import *


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    def getX(self):
        "Returns: x position of paddle"
        return self.x
    
    def getY(self):
        "Returns y position of paddle"
        return self.y
    
    def setX(self, value):
        "sets x position of paddle"
        self.x = value
    
    def setY(self, value):
        "sets y position of paddle"
        self.y = value 
    
    def __init__(self):
        """**Constructor**: Creates a new solid paddle.
        overides the GRectangle __init__ method to create a paddle.
        
        Parameter i: int used to multiply and loop through x positions of each brick.
        Precondition: i is an int > 0
        
        Parameter j: int used to multiply and loop through y positions of each brick.
        Precondition: j is an int > 0"""
        GRectangle.__init__(self,x = GAME_WIDTH/2, y = PADDLE_OFFSET,
        width = PADDLE_WIDTH, fillcolor = colormodel.BLACK, height = PADDLE_HEIGHT)
    
    def collides(self,ball):
        """Returns: True if the ball collides with this paddle by calling
        contains method in game2d.py to check if if the paddle contains
        the balls (x,y) position.
        
        Parameter ball: The ball to check.
        Precondition: ball is of class Ball."""
        
        if (self.contains(ball.x - BALL_DIAMETER/2.0, ball.y - BALL_DIAMETER/2.0)
            and ball._vx < 0):
            return True
        
        if (self.contains(ball.x + BALL_DIAMETER/2.0, ball.y - BALL_DIAMETER/2.0)
            and ball._vy < 0):
            return True

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    def __init__(self, i, j):
        """**Constructor**: Creates a new solid brick.
        overides the GRectangle __init__ method to create a brick.
        
        Parameter i: int used to multiply and loop through x positions of each brick.
        Precondition: i is an int > 0
        
        Parameter j: int used to multiply and loop through y positions of each brick.
        Precondition: j is an int > 0"""
        GRectangle.__init__(self, left = BRICK_SEP_H/2 + i*(BRICK_WIDTH + BRICK_SEP_H),
        y = (GAME_HEIGHT - BRICK_Y_OFFSET)  - j* (BRICK_HEIGHT + BRICK_SEP_V),
        fillcolor = BRICK_COLOR[j%10], width = BRICK_WIDTH, height = BRICK_HEIGHT,
        linecolor = BRICK_COLOR[j%10])
    
    def collides(self,ball):
        """Returns: True if the ball collides with this brick by calling
        contains method in game2d.py to check if if the paddle contains
        the balls (x,y) position.
        
        Parameter ball: The ball to check.
        Precondition: ball is of class Ball."""
        if self.contains(ball.x - BALL_DIAMETER/2.0, ball.y + BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x - BALL_DIAMETER/2.0, ball.y - BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x + BALL_DIAMETER/2.0, ball.y + BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x + BALL_DIAMETER/2.0, ball.y - BALL_DIAMETER/2.0):
            return True
            

class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY"""
    
    def getVx(self):
        "Returns: the x velocity of the ball"
        return self._vx
    
    def getVy(self):
        "Returns: the y velocity of the ball"
        return self._vy
    
    def setVx(self, value):
        "sets the x velocity of the ball"
        self._vx = value
    
    def setVy(self, value):
        "sets the y velocity of the ball"
        self._vy = value
    
    def getY(self):
        "Returns: the y position of the ball"
        return self.y
    
    def getX(self):
        "Returns: the x position of the ball"
        return self.x

    def __init__(self, vx=0, vy=0):
        """**Constructor**: Creates a new solid ball
        overides the GEllipse __init__ method to create a ball.
        
        Parameter vx: int used set the x veclocity of the ball.
        Precondition: vx is an int > 0
        
        Parameter vy: used set the x veclocity of the ball.
        Precondition: vy is an int > 0"""
        # self._vx = 0.0
        self._vx = random.uniform(1.0,5.0)
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
        GEllipse.__init__(self, x = GAME_WIDTH/2, y = GAME_HEIGHT/2,
        fillcolor = colormodel.BLUE, width = BALL_DIAMETER, height = BALL_DIAMETER)
        
    def moveBall(self):
        """Changes the x and y position by adding the x and y velocities."""
        self.x = self.x + self._vx
        self.y = self.y + self._vy
        
    def BounceBall(self):
        """Checks that if the ball is at the boundary of the game window
        it negates its direction to bounce back. If it is hitting the top
        or bottom of the game window it reverses the y velocity of the ball.
        If it hits the side of the game window it reverses the x velocity of
        the ball. """
        if self.y+BALL_DIAMETER/2 >= GAME_HEIGHT:
            self._vy = -self._vy
        if self.y - BALL_DIAMETER/2 <= 0:
            self._vy = -self._vy
        if self.x + BALL_DIAMETER/2 >= GAME_WIDTH:
            self._vx= -self._vx
        if self.x - BALL_DIAMETER/2 <= 0:
            self._vx = -self._vx
            
    def removeBall(self):
        """when called moves ball position to negative values
        to take the ball out of the user's view"""
        self.y = -10
        self.x = -10
    def setColor(self):
       
        x = random.uniform(1.0, 4.0)
        if 1.0 <= x < 2.0:
            if self.fillcolor == colormodel.RED:
                self.filcolor == colormodel.BLACK
            self.fillcolor = colormodel.RED
        elif 2.0 <= x < 3.0:
            if self.fillcolor == colormodel.BLACK:
                self.fillcolor = colormodel.BLUE
            self.fillcolor = colormodel.BLACK
        elif 3.0 <= x <= 4.0:
            if self.fillcolor == colormodel.BLUE:
                self.fillcolor = colormodel.RED
            self.fillcolor = colormodel.BLUE
        # elif 4.0 <= x < 5.0:
        #     if self.fillcolor == colormodel.YELLOW:
        #         self.fillcolor = colormodel.BLUE
        #     self.fillcolor == colormodel.YELLOW
        # elif x == 5.0:
        #     self.fillcolor == colormodel.GREEN
        #     
            
        #  if self.fillcolor == colormodel.RED:
        #     self.filcolor == colormodel.BLACK
        # if self.fillcolor == colormodel.BLACK:
        #     self.fillcolor = colormodel.BLUE
        # if self.fillcolor == colormodel.BLUE:
        #     self.fillcolor = colormodel.RED   
class Beach(GImage):
    """**Constructor**: Creates a new rectangle image
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide it with a list of 
        keyword arguments that initialize various attributes. For example, to load the 
        image `beach-ball.png`, use the constructor
        
            GImage(x=0,y=0,width=10,height=10,source='beach-ball.png')
        
        This class supports the all same keywords as `GRectangle`; the only new keyword
        is `source`.  See the documentation of `GRectangle` and `GObject` for the other
        supported keywords."""
    def __init__(self,x):
        GImage.__init__(self,x = x, y = 20, width = 70, height = 20, source='beach-ball.png')
        
    def collides(self, ball):
        """Returns: True if the ball collides with this brick by calling
        contains method in game2d.py to check if if the paddle contains
        the balls (x,y) position.
        
        Parameter ball: The ball to check.
        Precondition: ball is of class Ball."""
        if self.contains(ball.x - BALL_DIAMETER/2.0, ball.y + BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x - BALL_DIAMETER/2.0, ball.y - BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x + BALL_DIAMETER/2.0, ball.y + BALL_DIAMETER/2.0):
            return True
        if self.contains(ball.x + BALL_DIAMETER/2.0, ball.y - BALL_DIAMETER/2.0):
            return True
    def removeBeach(self):
        """removes the beach from the screen after a certain period of time"""
        self.x = -10
        self.y = -10
class Text(GLabel):
    
    
    def __init__(self,x,y, font ):
        """Instances represent an (uneditable) text label
    
    This object is exactly like a GRectangle, except that it has the possibility of
    containing some text.
    
    The attribute `text` defines the text content of this label.  Uses of the escape 
    character '\\n' will result in a label that spans multiple lines.  As with any
    `GRectangle`, the background color of this rectangle is `fillcolor`, while 
    `linecolor` is the color of the text.
    
    The text itself is aligned within this rectangle according to the attributes `halign` 
    and `valign`.  See the documentation of these attributes for how alignment works.  
    There are also attributes to change the point size, font style, and font name of the 
    text. The `width` and `height` of this label will grow to ensure that the text will 
    fit in the rectangle, no matter the font or point size.
    
    To change the font, you need a .ttf (TrueType Font) file in the Fonts folder; refer 
    to the font by filename, including the .ttf. If you give no name, it will use the 
    default Kivy font.  The `bold` attribute only works for the default Kivy font; for 
    other fonts you will need the .ttf file for the bold version of that font.  See the
    provided `ComicSans.ttf` and `ComicSansBold.ttf` for an example."""
        GLabel.__init__(text = text, x = x, y = y, font = font)


  