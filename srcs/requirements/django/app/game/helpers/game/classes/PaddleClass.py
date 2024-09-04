from game.helpers.game.classes.CoordsClass import Coords
import asyncio

class Paddle:
  def __init__(self, name, height, width, x, y, speed=0.1, pprint=False):
    self._height = height
    self._width = width
    self._name = name
    self._speed = speed
    self._coords = Coords(height, width, x, y, pprint=pprint)
    self._target_y = self._coords.get_y()
    if pprint:
      print(f"Paddle initialized with coords: {self._coords}")

  def set_speed(self, speed):
    self._speed = speed

  def get_coords(self):
    return self._coords
  
  def get_coords_pretty(self):
    return {
      'height': self._height,
      'width': self._width,
      'x': self._coords.get_left(),
      'y': self._coords.get_top()
    }
  
  def get_height(self):
    return self._height
  
  def get_name(self):
    return self._name

  async def _move_smoothly(self):
    current_y = self._coords.get_y()
    distance = self._target_y - current_y
    step = distance * 0.1

    if abs(step) > 0.5:
      new_y = current_y + step
      self._coords.update(self._coords.get_x(), new_y)
      await asyncio.sleep(0.016)  # 16ms delay to simulate 60 FPS (1000ms / 60)
      await self._move_smoothly()
    else:
        self._coords.update(self._coords.get_x(), self._target_y)

  
  async def move(self, board, direction):
    if direction == 'up':
      self._target_y = max(board.get_coords().get_top() + (self._height / 2), 
        self._coords.get_y() - self._speed * board.get_height())
    elif direction == 'down':
      self._target_y = min(board.get_coords().get_bottom() - (self._height / 2), 
        self._coords.get_y() + self._speed * board.get_height())
    await self._move_smoothly()

  def is_touching(self, other_coords):
    return self._coords.collides_with(other_coords)
  
  def reset_position(self):
    self._coords.update(self._coords.get_x(), 350)
  
  def __str__(self):
    return (f"Paddle '{self._name}':\n"
            f"  Dimensions: {self._width}x{self._height}\n"
            f"  Speed: {self._speed}\n"
            f"  Coordinates: (x: {self._coords.get_x()}, y: {self._coords.get_y()})")