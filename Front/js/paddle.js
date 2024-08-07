
export class Paddle {
  #htmlElem;
  #speed;
  #coords;
  #keys;
  #targetTop;

  constructor (paddle, keyup, keydown, speed=0.07, pprint=false)
  {
    this.#htmlElem = paddle;
    this.#speed = speed;
    this.#keys = [keyup, keydown];
    this.#coords = this.#htmlElem.getBoundingClientRect();
    this.#targetTop = this.#coords.top;
    if (pprint){
      console.log(this.#coords);
    }
  }

  #animateMove()
  {
    const currentTop = this.#coords.top;
    const distance = this.#targetTop - currentTop;
    const step = distance * 0.1;

    if (Math.abs(step) > 0.5)
    {
      this.#htmlElem.style.top = (currentTop + step) + 'px';
      this.#coords = this.#htmlElem.getBoundingClientRect();
      requestAnimationFrame(() => this.#animateMove());
    }
    else
    {
      this.#htmlElem.style.top = this.#targetTop + 'px';
      this.#coords = this.#htmlElem.getBoundingClientRect();
    }
  }
  #move(board, direction)
  {
    if (direction === 'up')
    {
      this.#targetTop = Math.max(board.getTop(), this.#coords.top - 
        this.#speed * window.innerHeight);
    }
    else if (direction === 'down')
    {
      this.#targetTop = Math.min(board.getBottom() - this.#coords.height, 
        this.#coords.top + this.#speed * window.innerHeight);
    }

    this.#animateMove();
  };

  isTouching(coords) {
    if (this.#coords.top <= coords.bottom && this.#coords.bottom >= coords.top) {
      if ((this.#coords.left <= coords.right && this.#coords.right >= coords.left) ||
          (this.#coords.right >= coords.left && this.#coords.left <= coords.right)) {
        return true;
      }
    }
    return false;
  }

  setEventListener(board)
  {
    document.addEventListener('keydown', (event) => {
      if (event.key === this.#keys[0]) 
      {
        requestAnimationFrame(() => this.#move(board, 'up'));
      }
      else if(event.key === this.#keys[1])
      {
        requestAnimationFrame(() => this.#move(board, 'down')); 
      }
    });
  };
}




// TODO: Make movement smoother
// TODO: Make sure both paddles can move at the same time