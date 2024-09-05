import { Lobby } from "./lobby.js";
import { Match } from "./match.js";
import { LeaderBoard } from "./leaderboard.js";

export class Tournament {
  #tournament;
  #lobby;
  #match;
  #leaderboard;

  constructor(tournament) {
    this.#tournament = tournament;
    tournament.socket = new WebSocket(
      'ws://' + window.location.host + '/ws/tournament/' + this.#tournament.id + '/'
    );
    this.#lobby = new Lobby(this.#tournament);
    this.#match = new Match(this.#tournament);
    this.#leaderboard = new LeaderBoard(this.#tournament);
    this.#displayPage();
    this.#initializeSocket();
  }

  #displayPage() {
    if (this.#tournament.status === 'open') {
      this.#lobby.showPage();
      this.#match.hidePage();
      this.#leaderboard.hidePage();
    }
    else if (this.#tournament.status === 'locked') {
      this.#lobby.hidePage();
      this.#match.showPage();
      this.#leaderboard.hidePage();
    }
    else if (this.#tournament.status === 'closed') {
      this.#lobby.hidePage();
      this.#match.hidePage();
      this.#leaderboard.showPage();
    }
  }

  #togglePage(hide, show) {
    hide.hidePage();
    show.showPage();
  }
  
  #parseMessage(data, pprint=true) {
    const message = JSON.parse(data);
    if (pprint) 
    if (message.message === 'start_tournament') 
    {
      this.#togglePage(this.#lobby, this.#match);
      this.#match.setMatchEventListeners(message);
    }
    else if (message.message === 'modal')
    {
      var modalElement = document.getElementById('modal');
      if (modalElement) {
        var myModal = new bootstrap.Modal(modalElement);
        myModal.show();
      }
      window.location.reload();
    }
    else if (message.message === 'lobby_update') {
      this.#lobby.updatePage(message.players, message.host_id);
    }
    else if (message.message === 'countdown') {
      this.#match.showCountdown(message.count)
    }
    else if (message.message === 'game_state') {
     this.#match.updateState(message);
    }
    else if (message.message === 'results') {
      this.#togglePage(this.#match, this.#leaderboard);
      this.#leaderboard.loadLeaderboard(message.results);
    }
  }
    
  #redirectHome() { window.location.href = "/game/home/"; }
  #initializeSocket() {
    this.#tournament.socket.onopen    = (event) => {                                  };
    this.#tournament.socket.onclose   = (event) => { this.#redirectHome();            };
    this.#tournament.socket.onmessage = (event) => { this.#parseMessage(event.data);  };
    this.#tournament.socket.onerror   = (error) => { this.#redirectHome();            };
  }
}