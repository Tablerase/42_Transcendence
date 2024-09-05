import math
import random

from game.helpers.game.classes.CoordsClass import Coords

class Ball:
  def __init__(self, board, speed=7):
    self._diameter = 50
    self._pace = 1
    self._speed = speed
    self._board_coords = board.get_coords()
    self._coords = Coords(
      self._diameter,
      self._diameter,
      self._board_coords.get_x(),
      self._board_coords.get_y()
    )
    self._set_direction()
    self._set_slope()
  
  def info_dict(self):
    return {
      'height': self._diameter,
      'width': self._diameter,
      'x': self._coords.get_left(),
      'y': self._coords.get_top()
    }
  
  def augment_pace(self):
    self._pace += 0.1
  
  def _set_slope(self):
    angle = math.floor(random.random() * 90) - 45
    angle = angle * math.pi / 180
    self._slope_x = self._speed * math.cos(angle)
    self._slope_y = self._speed * math.sin(angle)
  
  def _set_direction(self):
    self._direction_x = random.randint(0, 1)
    self._direction_y = random.randint(0, 1)

  def invert_direction(self, direction):
    if direction == 'y':
      self._direction_y = 1 if self._direction_y == 0 else 0
    elif direction == 'x':
      self._direction_x = 1 if self._direction_x == 0 else 0
      if self._direction_x == 1:
        self._coords.set_x(self._coords.get_x() + 5)
      else:
        self._coords.set_x(self._coords.get_x() - 5)

  def reset_position(self):
    self._set_slope()
    self._set_direction()
    self.move(middle=True)
  
  def reset_slope(self):
    self._set_slope()

  def move(self, middle=False):
    if middle:
      self._pace = 1
      target_x = self._board_coords.get_x()
      target_y = self._board_coords.get_y()
    else:
      x = self._coords.get_x()
      y = self._coords.get_y()
      target_x = x + self._slope_x * (-self.get_pace() if self._direction_x == 0 else self.get_pace())
      target_y = y + self._slope_y * (-self.get_pace() if self._direction_y == 0 else self.get_pace())
    self._coords.update(target_x, target_y)

  def get_pace(self):
    return self._pace
  
  def get_coords(self):
    return self._coords