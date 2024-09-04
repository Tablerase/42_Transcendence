import asyncio

from game.helpers.game.classes.BoardClass import Board
from game.helpers.game.classes.PaddleClass import Paddle
from game.helpers.game.classes.BallClass import Ball
from game.helpers.game.classes.MatchInfoClass import Match
import game.helpers.game.utils.websocket_utils as ws_utils


class Game:
  def __init__(self, match_info):
    self._match_info = match_info
    self._board = Board()
    middle_x, middle_y = self._board.get_middle()
    self._paddles = [
      Paddle(name='left_paddle', height=100, width=10, x=10, y=middle_y),
      Paddle(name='right_paddle', height=100, width=10, x=945, y=middle_y)
    ]
    self._ball = Ball(self._board)
    self.prev_ball_top = 0
    self.is_game_running = True
  
  async def game_loop(self):
    while self.is_game_running:
      await self.ball_board_intersection()
      self.ball_paddle_intersection()
      self._ball.move()
      await asyncio.sleep(0.016)  # Simulate ~60fps
      await self.send_game_state()
  
  async def send_game_state(self):
    game_state = {
      'message': 'game_state',
      'board': self._board.get_coords_pretty(),
      'left_paddle': self._paddles[0].get_coords_pretty(),
      'right_paddle': self._paddles[1].get_coords_pretty(),
      'ball': self._ball.get_coords_pretty(),
      'scores':  self._match_info.get_scores(),
      'name': self._match_info.get_name()
    }
    await ws_utils.send_message_to_group(self._match_info, 'game_state', game_state=game_state)
  
  async def move_paddle(self, paddle_name, direction):
    for paddle in self._paddles:
      if paddle.get_name() == paddle_name:
        await paddle.move(self._board, direction)
  
  async def score(self, scorer):
    players = self._match_info.get_player_names()
    scorer_name = players[scorer]
    self._match_info.set_message(f'{scorer_name} scored!')
    await self._match_info.increment_score(scorer)
    if self._match_info.get_scores()[scorer] == 10:
      self.finish_and_restore(scorer)
  
  async def someone_scored(self):
    if self._ball.get_coords().get_left() <= self._board.get_coords().get_left():
      await self.score(1)
      return True
    elif self._ball.get_coords().get_right() >= self._board.get_coords().get_right():
      await self.score(0)
      return True
    return False
  
  async def ball_board_intersection(self):
    if self._board.is_out_of_bounds(self._ball.get_coords()):
      if await self.someone_scored():
        self._ball.reset_position() 
      else:
        self._ball.invert_direction('y')
  
  def ball_paddle_intersection(self):
    for paddle in self._paddles:
      if paddle.is_touching(self._ball.get_coords()):
        if self._ball.get_coords().get_top() == self.prev_ball_top:
          self._ball.reset_slope()
        self.prev_ball_top = self._ball.get_coords().get_top()
        self._ball.augment_pace()
        self._ball.invert_direction('x')
  
  def finish_and_restore(self, winner):
    players = self._match_info.get_player_names()
    self._match_info.set_message(f'{players[winner]} won!')
    self._match_info.reset_scores()
    self._ball.reset_position()
    self._paddles[0].reset_position()
    self._paddles[1].reset_position()
    self.is_game_running = False
  


