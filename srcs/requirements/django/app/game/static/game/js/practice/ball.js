
export class Ball {

  #htmlElement;
  #speed;
  #pace;
  #slope_x;
  #slope_y;
  #direction_x;
  #direction_y;
  #coords;

  constructor (ball, speed=7)
  {
    this.#pace = 1;
    this.#speed = speed;
    this.#setDirection(); 
    this.#coords = ball.getBoundingClientRect();
    this.#htmlElement = ball;
    this.#setSlope();
  }

  getPace() { return this.#pace; }
  augmentPace() { this.#pace += 0.1;}

  #setSlope() {
    let angle = Math.floor(Math.random() * 90) - 45;
    angle = angle * Math.PI / 180;
    this.#slope_x = this.#speed * Math.sin(angle);
    this.#slope_y = this.#speed * Math.cos(angle);
  }

  #setDirection() {
    this.#direction_x = Math.floor(Math.random() * 2);
    this.#direction_y = Math.floor(Math.random() * 2);
  }

  getHtmlElem() { return this.#htmlElement; }
  getCoords() {
    return this.#coords;
  }

  opposedDirection(direction) {

    if (direction == 'y')
    {
      this.#direction_y = (this.#direction_y == 0) ? 1 : 0;
    }
    else if (direction == 'x')
    {
      this.#direction_x = (this.#direction_x == 0) ? 1 : 0;
    }
  }

  resetPosition() {
    this.#setSlope();
    this.#setDirection();
    this.move(1);
  }

  resetSlope() {
    this.#setSlope();
  }

  move(middle=false) {

    if (middle) {
      this.#pace = 1;
      this.#htmlElement.style.top = 'calc(50% + 20px)';
      this.#htmlElement.style.left = 'calc(50% - 20px)';
    }
    else {
      this.#htmlElement.style.top = this.#coords.top + this.#slope_x * (this.#direction_y == 0 ? -this.getPace() : this.getPace()) + 'px';
      this.#htmlElement.style.left = this.#coords.left + this.#slope_y * (this.#direction_x == 0 ? -this.getPace() : this.getPace()) + 'px';
    }
    this.#coords = this.#htmlElement.getBoundingClientRect();
  }

}


// Someone wins
// Tournament: 
// Bootstrap: Modal for game winner, Popover for customization