
export class Ball {

  #htmlElement;
  #speed;
  #slope_x;
  #slope_y;
  #direction_x;
  #direction_y;
  #coords;

  constructor (ball, speed=9, pprint=false)
  {
    this.#speed = speed;
    this.#direction_x =  Math.floor(Math.random() * 2);
    this.#direction_y = Math.floor(Math.random() * 2); 
    this.#coords = ball.getBoundingClientRect();
    this.#htmlElement = ball;
    this.#setSlopes();
    if (pprint) {
      console.log(this.#coords);
    }
  }

  #setSlopes() {

    // generate random angle between 0 and 90 degrees
    let angle = Math.floor(Math.random() * 90) - 45;
    // transform angle to radians
    angle = angle * Math.PI / 180;

    this.#slope_x = this.#speed * Math.sin(angle);
    this.#slope_y = this.#speed * Math.cos(angle);

    console.log(this.#slope_x, this.#slope_y);

  }

  getCoords() {
    return this.#coords;
  }

  resetDirection (direction) {

    if (direction == 'y')
    {
      this.#direction_y = (this.#direction_y == 0) ? 1 : 0;
    }
    else if (direction == 'x')
    {
      this.#direction_x = (this.#direction_x == 0) ? 1 : 0;
    }
  }

  resetBallPosition() {
    this.#setSlopes();
    this.move(1);
  }

  move(middle=false) {

    if (middle) {
      this.#htmlElement.style.top = 'calc(50% - 20px)';
      this.#htmlElement.style.left = 'calc(50% - 20px)';
    }
    else {
      this.#htmlElement.style.top = this.#coords.top + this.#slope_x * (this.#direction_y == 0 ? -1 : 1) + 'px';
      this.#htmlElement.style.left = this.#coords.left + this.#slope_y * (this.#direction_x == 0 ? -1 : 1) + 'px';
    }
    this.#coords = this.#htmlElement.getBoundingClientRect();
  }

}


