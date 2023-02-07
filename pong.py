from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            ball.velocity_x *= -1.1


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    # Latest Position = Current Velocity + Current Position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# Update - moving the ball by calling the move() and other stuff
class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

        # Reset position
        self.ball.center = self.center

    def update(self, dt):
        self.ball.move()

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height - 50):
            self.ball.velocity_y *= -1

        # bounce off left and increase the score
        if self.ball.x < 0:
            self.ball.velocity_x *= -1
            self.player1.score +=1
            self.serve_ball()
        # bounce off right
        if self.ball.x > self.width - 50:
            self.ball.velocity_x *= -1
            self.player2.score += 1
            self.serve_ball()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1 / 4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3 / 4:
            self.player2.center_y = touch.y

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1, spacing=10)
        layout.add_widget(Label(text='Pong Game'))
        btn1 = Button(text='Single Player')
        btn1.bind(on_press=self.goto_game)
        btn2 = Button(text='Multiplayer')
        btn2.bind(on_press=self.goto_game)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        self.add_widget(layout)

    def goto_game(self, instance):
        # Switch to the game screen
        self.manager.current = 'game'

class PongScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = PongGame()
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        self.add_widget(self.game)


class PongApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.menu = MenuScreen(name='menu')
        self.game = PongScreen(name='game')
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.game)
        self.sm.current = 'menu'
        return self.sm



PongApp().run()
