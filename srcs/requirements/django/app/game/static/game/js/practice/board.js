export class Board {
  #htmlElement;
  #top;
  #bottom;
  #right;
  #left;

  constructor (board) {
    
    let coords;
    
    coords = board.getBoundingClientRect();
    this.#top = coords.top;
    this.#bottom = coords.bottom;
    this.#right = coords.right;
    this.#left = coords.left;
    this.#htmlElement = board; 
  }

  // Getters
  getTop() { return this.#top; }
  getBottom() { return this.#bottom; }
  getRight() { return this.#right; }
  getLeft() { return this.#left; }
  getBoard() { return this.#htmlElement;}

  isTouchingBorder(coords) {
    if (coords.top <= this.#top || coords.bottom >= this.#bottom 
      || coords.left <= this.#left || coords.right >= this.#right) 
    {
      return true;
    }
    return false;
  }
  
};