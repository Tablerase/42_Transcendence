export class Lobby {
  #tournament;
  #page;
  #startButton;
  #leaveTournamentButton;
  #noFriendsDiv;
  #playersContainer;

  constructor (tournament, pprint=false) {
    this.#tournament = tournament;
    this.#page = document.getElementById('lobbyPage');
    this.#startButton = document.getElementById('startTournamentButton');
    this.#setTournamentHost(this.#tournament.host_id);
    this.#initializeleaveTournamentButton();
    this.#noFriendsDiv = document.getElementById('noFriendsDiv');
    this.#playersContainer = document.getElementById('playersContainer');
    if (pprint) {
      console.log(this.#tournament);
      console.log(this.#page);
      console.log(this.#startButton);
      console.log(this.#leaveTournamentButton);
      console.log(this.#noFriendsDiv);
    }
  }

  updatePage(players, host_id) {
    if (this.#tournament.host_id !== host_id) {
      this.#setTournamentHost(host_id); 
    }
    
    const playersContainer = this.#playersContainer;
    Array.from(playersContainer.children).forEach(child => {
      if (child !== noFriendsDiv) {
        playersContainer.removeChild(child);
      }
    });
    if (players.length === 1) {
      this.#noFriendsDiv.removeAttribute('hidden');
    }
    else {
      this.#noFriendsDiv.setAttribute('hidden', true);
      players.forEach(player => { 
        let playerDiv;
        if (player.id === this.#tournament.host_id) 
          playerDiv = this.#createPlayerDiv(player, true);
        else
          playerDiv = this.#createPlayerDiv(player, false);
        playersContainer.appendChild(playerDiv);
      });
    }
  }

  #setTournamentHost(host_id) {
    this.#tournament.host_id = host_id;
    if (this.#tournament.user_id === this.#tournament.host_id){
      this.#startButton.removeAttribute('hidden');
      const context = {
        'message': 'start_tournament'
      }
      this.#startButton.addEventListener('click', () => {
        this.#sendToServer( context );
      });
    }
  }

  #initializeleaveTournamentButton() {
    this.#leaveTournamentButton = document.getElementById('leaveTournamentButton');
    const context = {
      'message': 'leave_tournament'
    }
    this.#leaveTournamentButton.addEventListener('click', () => {
      this.#sendToServer(context);
      this.#tournament.socket.close(1000);
      window.location.href = "/game/home/";
    });
  }

  #createPlayerDiv(player, isHost) {
    const playerDiv = document.createElement('div');
    playerDiv.className = 'player';
    if (isHost) {
      playerDiv.classList.add('host');
    }
  
    playerDiv.innerHTML = `
      <a class="left-part player-part" href="/profile/${player.username}">
        <div class="image">
          <img class="photo" src="${player.image_url}" alt="${isHost ? 'host' : 'player'} pic">
          ${isHost ? '<img src="/static/users/svg/crown.svg" alt="winner" class="crown">' : ''}
        </div>
        <h3>${player.username}</h3>
      </a>
      <div class="right-part player-part">
        <p>🏆: <span class="text-success">${player.wins}</span></p>
        <p>💔: <span class="text-danger">${player.losses}</span></p>
      </div>
    `;
  
    return playerDiv;
  }

  #sendToServer(context) { this.#tournament.socket.send(JSON.stringify( context ));}
  showPage() { this.#page.removeAttribute('hidden'); }
  hidePage() { this.#page.setAttribute('hidden', true);}
}