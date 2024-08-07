export class Panel 
{
  #message;
  #scores;

  constructor()
  {
    this.#message = document.querySelector('.message');
    this.#scores = [document.querySelector('.player_1_score'), document.querySelector('.player_2_score')];
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