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

    const http_scheme = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const ws_url = http_scheme + window.location.host + '/ws/tournament/' + this.#tournament.id + '/';

    console.log('Connecting to ' + ws_url);

    tournament.socket = new WebSocket(
      ws_url
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
  
  #parseMessage(data) {
    const message = JSON.parse(data);
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
    else if (message.message === 'redirect_home') {
      this.redirectHome();
    }
  }
    
  redirectHome() { window.location.href = "/game/home/"; }
  #initializeSocket() {
    this.#tournament.socket.onopen    = (event) => {                                  };
    this.#tournament.socket.onclose   = (event) => {                                  };  
    this.#tournament.socket.onmessage = (event) => { this.#parseMessage(event.data);  };
    this.#tournament.socket.onerror   = (error) => { this.redirectHome();            };
  }
}