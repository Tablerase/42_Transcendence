
class Coords:
  def __init__(self, height, width, x, y, pprint=False):
    self._height = height
    self._width = width
    self._x = x
    self._y = y
    self._update_edges()
    if pprint:
        print(f"Coords: {self}")

  def _update_edges(self):
    self._top = self._y - self._height / 2
    self._bottom = self._y + self._height / 2
    self._left = self._x - self._width / 2
    self._right = self._x + self._width / 2

  def update(self, x, y):
    self._x = x
    self._y = y
    self._update_edges()

  def get_top(self):
    return self._top

  def get_bottom(self):
    return self._bottom

  def get_left(self):
    return self._left

  def get_right(self):
    return self._right
  
  def get_x(self):
    return self._x

  def get_y(self):
    return self._y
  
  def set_y(self, y):
    self._y = y

  def set_x(self, x):
    self._x = x
  
  def __str__(self):
    return (f"Coords(x={self._x}, y={self._y}, "
            f"top={self._top}, bottom={self._bottom}, "
            f"left={self._left}, right={self._right})")
  
  def contains_point(self, x, y):
    return self._left <= x <= self._right and self._top <= y <= self._bottom
  
  def collides_with(self, other):
    return not (self._right < other.get_left() or
                self._left > other.get_right() or
                self._bottom < other.get_top() or
                self._top > other.get_bottom())
  
  def contains_object(self, other):
    return (self._left <= other.get_left() and
            self._right >= other.get_right() and
            self._top <= other.get_top() and
            self._bottom >= other.get_bottom())
