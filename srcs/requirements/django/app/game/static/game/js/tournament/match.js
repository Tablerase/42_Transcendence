import { Item } from "./item.js";

export class Match {
  #tournament;
  #page;
  #board;
  #leftPaddle;
  #rightPaddle;
  #ball;
  #message;
  #scores;

  constructor (tournament) 
  {
    this.#tournament = tournament;
    this.#page = document.getElementById('matchPage');
    this.#board = new Item('board');
    this.#leftPaddle = new Item('leftPaddle');
    this.#rightPaddle = new Item('rightPaddle');
    this.#ball = new Item('ball');
    this.#message = new Item('matchMessage');
    this.#scores = [new Item('score_0'), new Item('score_1')];
    this.#saveStateListener();
    this.#restoreStateListener();
  }

  setMatchEventListeners(message) 
  {
    this.#message.setInnerHtml(message.match);
    console.log(message.role);
    if (message.role === 'left_paddle' || message.role === 'right_paddle') {
      document.addEventListener('keydown', (event) => {
        let message;
        if (event.key == 'ArrowUp')
          message = 'up';
        else if (event.key == 'ArrowDown')
          message = 'down';
        if (message) {
          const context = { 'message': message };
          this.#sendToServer(context);
        }
      });
    }
  }

  showCountdown(count)
  {
    let countdown = document.getElementById('countdown');
    this.#ball.hideItem();
    countdown.innerHTML = count;
    countdown.style.display = 'block';
    if (count === 0)
    {
      this.#ball.showItem();
      this.#leftPaddle.showItem();
      this.#rightPaddle.showItem();
      countdown.style.display = 'none';
    }
  }

  #sendToServer(context) { this.#tournament.socket.send(JSON.stringify( context ));}
  
  updateState(message) {

    // Check if this is the first time the function is being called
    if (!this._initialized) {
      this.initializeElements(message);
      // Set initialized flag to true
      this._initialized = true;
    } else {
      // Update positions with the calculated offsets
      this.#board.updatePosition(message.board.x + this._offsetX, message.board.y + this._offsetY);
      this.#ball.updatePosition(message.ball.x + this._offsetX, message.ball.y + this._offsetY);
      this.#leftPaddle.updatePosition(message.left_paddle.x + this._offsetX, message.left_paddle.y + this._offsetY);
      this.#rightPaddle.updatePosition(message.right_paddle.x + this._offsetX, message.right_paddle.y + this._offsetY);
    }
    // Update text elements
    this.#message.updateText(message.name);
    this.#scores[0].updateText(message.scores[0]);
    this.#scores[1].updateText(message.scores[1]);
  }


  initializeElements(message) {
    const boardWidth = message.board.width;
    const boardHeight = message.board.height;
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;

    // Calculate the offset to center the board
    this._offsetX = (screenWidth - boardWidth) / 2;
    this._offsetY = (screenHeight - boardHeight) / 2;

    // Initialize element dimensions
    this.#board.setDimensions(boardWidth, boardHeight);
    this.#ball.setDimensions(message.ball.width, message.ball.height);
    this.#leftPaddle.setDimensions(message.left_paddle.width, message.left_paddle.height);
    this.#rightPaddle.setDimensions(message.right_paddle.width, message.right_paddle.height);

    // Update positions with the correct offsets
    this.#board.updatePosition(message.board.x + this._offsetX, message.board.y + this._offsetY);
    this.#ball.updatePosition(message.ball.x, message.ball.y);
    this.#leftPaddle.updatePosition(message.left_paddle.x , message.left_paddle.y);
    this.#rightPaddle.updatePosition(message.right_paddle.x, message.right_paddle.y );

    // Show paddles and ball
    this.#ball.showItem();
    this.#leftPaddle.showItem();
    this.#rightPaddle.showItem();
  }

  #restoreStateListener()
  {
    const matchData = JSON.parse(localStorage.getItem('matchData'));
    if (matchData) {
      this.#message.setInnerHtml( matchData.message );
      this.#leftPaddle.setCoords( matchData.leftPaddleCoords );
      this.#rightPaddle.setCoords( matchData.rightPaddleCoords );
      this.#ball.setCoords( matchData.ballCoords );
      this.#scores[0].setInnerHtml( matchData.scores[0] );
      this.#scores[1].setInnerHtml( matchData.scores[1] );
    }
  }

  #saveStateListener() {
    window.addEventListener('beforeunload', (event) => {
      const matchData = {
        message: this.#message.getInnerHtml(),
        leftPaddleCoords: this.#leftPaddle.getCoords(),
        rightPaddleCoords: this.#rightPaddle.getCoords(),
        ballCoords: this.#ball.getCoords(),
        scores : [this.#scores[0].getInnerHtml(), this.#scores[1].getInnerHtml()]
      };
      localStorage.setItem('matchData', JSON.stringify(matchData));
    });
  }
  showPage() {this.#page.removeAttribute('hidden');}
  hidePage() {this.#page.setAttribute('hidden', true);}
}
