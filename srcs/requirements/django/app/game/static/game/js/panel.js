export class Panel 
{
  #message;
  #scores;

  constructor()
  {
    this.#message = document.querySelector('.message');
    this.#scores = [document.querySelector('.player_1_score'), document.querySelector('.player_2_score')];
  }

  getScore(player_index)
  {
    return parseInt(this.#scores[player_index].innerHTML);
  }

  resetPosition()
  {
    this.#scores[0].innerHTML = 0;
    this.#scores[1].innerHTML = 0;
  }

  boostScore(player_index)
  {
    this.#scores[player_index].innerHTML = parseInt(this.#scores[player_index].innerHTML) + 1;
  }

  changeMessage(message)
  {
    this.#message.innerHTML = message;
  }
}