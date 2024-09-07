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
      this.#showModal(message.title, message.error_message);
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
      this.#redirectHome();
    }
  }

  #showModal(title, message) {
    // Dynamically create the modal element
    const modalContainer = document.createElement('div');
    modalContainer.innerHTML = `
        <div class="modal fade" id="dynamicModal" tabindex="-1" aria-labelledby="modalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="modalLabel">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        ${message}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modalContainer);
    const dynamicModal = new bootstrap.Modal(document.getElementById('dynamicModal'));
    dynamicModal.show();
    document.getElementById('dynamicModal').addEventListener('hidden.bs.modal', () => {
       modalContainer.remove();
    });
  }
    
  #redirectHome() { window.location.href = "/game/home/"; }
  #initializeSocket() {
    this.#tournament.socket.onopen    = (event) => {                                  };
    this.#tournament.socket.onclose   = (event) => {                                  };  
    this.#tournament.socket.onmessage = (event) => { this.#parseMessage(event.data);  };
    this.#tournament.socket.onerror   = (error) => { this.#redirectHome();            };
  }
}