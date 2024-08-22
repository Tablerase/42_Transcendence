import { Board } from './board.js';
import { Ball } from './ball.js';
import { Paddle } from './paddle.js';
import { Panel } from './panel.js';

export class Game {
  #panel
  #board;
  #paddles;
  #ball;
  #isGameRunning;
  #keysPressed;
  #prevBallTop;

  constructor ()
  {
    this.#panel = new Panel();
    this.#board = new Board(document.querySelector('.board'));
    this.#paddles = [
      new Paddle(document.querySelector('.paddle_1'), 'w', 's'),
      new Paddle(document.querySelector('.paddle_2'), 'ArrowUp', 'ArrowDown')
    ];
    this.#ball = new Ball(document.querySelector('.ball'));
    this.#isGameRunning = false;
    this.#keysPressed = {};
    this.#prevBallTop = 0;
    this.#monitorGame();
  }

  /* Game control functions */
  #monitorGame() {
    document.addEventListener('keydown', (event) => {
      if (event.key === ' ') 
      {
        if (this.#isGameRunning)
        {
          this.#pauseGame();
        } else {
          this.#startGame();
        }
      }
    });
  }

  #startGame()
  {
    if (this.#isGameRunning) return;

    this.#isGameRunning = true;
    this.#panel.changeMessage('PLAYING');
    this.#animateBall();
    this.#animatePaddles();
  }

  #pauseGame()
  {
    if (this.#isGameRunning)
    {
      this.#isGameRunning = false;
      this.#panel.changeMessage('GAME PAUSED');
    }
  }

  /* Objects animation */

  #animateBall() 
  {
    if (!this.#isGameRunning) 
      return;

    this.#ballBoardIntersection(this.#ball, this.#board)
    this.#ballPaddleIntersection(this.#ball, this.#paddles);
    this.#ball.move();
    requestAnimationFrame(() => this.#animateBall(this.#ball, this.#board, this.#paddles, this.#panel));
  }

  #animatePaddles()
  {
    if (!this.#isGameRunning)
      return;

    for (let paddle of this.#paddles)
    {
      if (this.#keysPressed[paddle.getKeyUp()])
      {
        paddle.move(this.#board, 'up');
        continue;
      }
      else if (this.#keysPressed[paddle.getKeyDown()])
      {
        paddle.move(this.#board, 'down');
      }
    }
    this.#listenPaddleKeys('keydown');
    this.#listenPaddleKeys('keyup', false);

    requestAnimationFrame(() => this.#animatePaddles());
  }

  #listenPaddleKeys(eventName, yes=true)
  {
    const keysOfInterest = ['ArrowUp', 'ArrowDown', 'w', 's', 'W', 'S'];

    document.addEventListener(eventName, (event) => {
      if (keysOfInterest.includes(event.key))
      {
        if (event.key == 'W' || event.key == 'S')
          this.#keysPressed[event.key.toLowerCase()] = yes;
        else
          this.#keysPressed[event.key] = yes;
      }
    });
  }

  #score(player)
  {
    this.#panel.boostScore(player);
    this.#panel.changeMessage('PLAYER ' + (player + 1) + ' SCORED!');
    if (this.#panel.getScore(player) == 10)
    {
      this.#isGameRunning = false;
      this.#panel.changeMessage('PLAYER ' + (player + 1) + ' WINS!');
      this.#resetGame();
    }
  }

  #someoneScored()
  {
    if (this.#ball.getCoords().left <= this.#board.getLeft())
    {
      this.#score(1);
      return 1;
    }
    else if (this.#ball.getCoords().right >= this.#board.getRight())
    {
      this.#score(0);
      return 1;
    }
    return 0;
  }

  #ballBoardIntersection() 
  {
    if (this.#board.isTouchingBorder(this.#ball.getCoords())) 
    {
      if (this.#someoneScored(this.#ball, this.#board, this.#panel)) 
        this.#ball.resetPosition();
      else 
        this.#ball.opposedDirection('y');
    }
  }

  #ballPaddleIntersection() 
  {
    for (let paddle of this.#paddles)
    {
      let htmlElems = [ this.#ball.getHtmlElem(), this.#board.getBoard(), paddle.getHtmlElem()];
      if (paddle.isTouching(this.#ball.getCoords())) 
      {
        if (this.#ball.getCoords().top == this.#prevBallTop)
          this.#ball.resetSlope();
        this.#prevBallTop = this.#ball.getCoords().top;
        this.#ball.augmentPace();
        this.#ball.opposedDirection('x');
        for (let elem of htmlElems)
          elem.classList.add('hit');
        setTimeout(() => {
          for (let elem of htmlElems)
            elem.classList.remove('hit');
        }, 150);
      }
    }
  }

  #resetGame() 
  {
    this.#panel.resetPosition();
    this.#ball.resetPosition();
    this.#paddles[0].resetPosition();
    this.#paddles[1].resetPosition();
  }
};

