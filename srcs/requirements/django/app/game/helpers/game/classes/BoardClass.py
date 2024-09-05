from game.helpers.game.classes.CoordsClass import Coords

class Board:
  def __init__(self, pprint=True):
    self._height = 700
    self._width = 960
    self._coords = Coords(self._height, self._width, self._width / 2, self._height / 2)
    if pprint:
      print(f"Board: {self}")

  def is_out_of_bounds(self, coords):
    return not self._coords.contains_object(coords)
  
  def get_middle(self):
    return self._coords.get_x(), self._coords.get_y()
  
  def get_height(self):
    return self._height
 
  def get_width(self):
    return self._width
  
  def get_coords(self):
    return self._coords
  
  def get_coords_pretty(self):
    return {
      'height': self._height,
      'width': self._width,
      'x': self._coords.get_left(),
      'y': self._coords.get_top()
    }
  
  def __str__(self):
    return (f"Board(height={self._height}, width={self._width}, "
      f"coords={self._coords})")
