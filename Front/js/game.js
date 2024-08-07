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
  }

  setupEventListeners() {
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') 
      {
        if (this.#isGameRunning)
        {
          this.pauseGame();
        } else {
          this.startGame();
        }
      }
    });
  }


  startGame()
  {
    if (this.#isGameRunning) return;
    this.#panel.changeMessage('Game is running...');
    this.#isGameRunning = true;
    this.#animateBall();
    for (let paddle of this.#paddles)
    {
      paddle.setSpeed(0.01);
    }
    this.#animatePaddles();
  }

  pauseGame()
  {
    if (this.#isGameRunning)
    {
      this.#isGameRunning = false;
      this.#panel.changeMessage('Game is paused...');
      for (let paddle of this.#paddles)
      {
        paddle.setSpeed(0);
      }
    }
  }

  /* Intersection functions and game logic */

  #someoneScored()
  {
    if (this.#ball.getCoords().left <= this.#board.getLeft())
    {
      this.#panel.boostScore(1);
      this.#panel.changeMessage('Player 2 scored!');
      return 1;
    }
    else if (this.#ball.getCoords().right >= this.#board.getRight())
    {
      this.#panel.boostScore(0);
      this.#panel.changeMessage('Player 1 scored!');
      return 1;
    }
    return 0;
  }

  #ballBoardIntersection() 
  {
    if (this.#board.isTouchingBorder(this.#ball.getCoords())) 
    {
      if (this.#someoneScored(this.#ball, this.#board, this.#panel)) 
      {
        this.#ball.resetBallPosition();
        return 1;
      }
      else 
      {
        this.#ball.resetDirection('y');
      }
    }
    return 0;
  }

  #ballPaddleIntersection() 
  {
    for (let paddle of this.#paddles)
    {
      if (paddle.isTouching(this.#ball.getCoords())) 
      {
        this.#ball.resetDirection('x');
      }
    }
  }

  /* Object Animation functions */

  #animateBall() 
  {
    if (!this.#isGameRunning) 
    {
      return;
    }
    if (this.#ballBoardIntersection(this.#ball, this.#board) === 1)
    {
      this.#isGameRunning = false;
      return;
    }
    this.#ballPaddleIntersection(this.#ball, this.#paddles);
    this.#ball.move();
    requestAnimationFrame(() => this.#animateBall(this.#ball, this.#board, this.#paddles, this.#panel));
  }

  #animatePaddles()
  {
    const keysOfInterest = ['ArrowUp', 'ArrowDown', 'w', 's', 'W', 'S'];
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

    document.addEventListener('keydown', (event) => {
      if (keysOfInterest.includes(event.key))
      {
        if (event.key == 'W' || event.key == 'S')
          this.#keysPressed[event.key.toLowerCase()] = true;
        else
          this.#keysPressed[event.key] = true;
      }

    });

    document.addEventListener('keyup', (event) => {
      {
        if (keysOfInterest.includes(event.key))
        {
          if (event.key == 'W' || event.key == 'S')
            this.#keysPressed[event.key.toLowerCase()] = false;
          else
            this.#keysPressed[event.key] = false;
        }
      }
    });
    requestAnimationFrame(() => this.#animatePaddles());
  }
};
