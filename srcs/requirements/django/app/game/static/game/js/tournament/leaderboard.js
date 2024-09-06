export class LeaderBoard {
  #tournament;
  #page;
  #leaveButton;

  constructor (tournament, pprint=false) {
    this.#tournament = tournament;
    this.#page = document.getElementById('leaderboardPage');
    this.#leaveButtonListener();
  }
  
  showPage() { this.#page.removeAttribute('hidden'); }
  hidePage() { this.#page.setAttribute('hidden', true);}
  
  #leaveButtonListener() {
    this.#leaveButton = document.getElementById('leaveButton');
    const context = {
      'message': 'leave_tournament'
    }
    console.log("Event set");
    this.#leaveButton.addEventListener('click', () => {
      console.log("Button Presed");
      this.#sendToServer(context);
      this.#tournament.socket.close(1000);
      window.location.href = "/game/home/";
    });
  }

  loadLeaderboard(results) {
    const tableBody = document.getElementById('leaderboardTableBody');

    // Clear existing rows
    tableBody.innerHTML = '';

    let index = 1;
    results.forEach(result => {
      const row = document.createElement('tr');

      const rankCell = document.createElement('td');
      rankCell.textContent = index++;
      rankCell.classList.add('rank');
      row.appendChild(rankCell);

      const avatarCell = document.createElement('td');
      const img = document.createElement('img');
      img.src = result.image_url;
      img.alt = result.username;
      avatarCell.appendChild(img);
      avatarCell.classList.add('avatar');
      row.appendChild(avatarCell);

      const usernameCell = document.createElement('td');
      usernameCell.textContent = result.username;
      usernameCell.classList.add('username');
      row.appendChild(usernameCell);

      const pointsCell = document.createElement('td');
      pointsCell.textContent = result.points;
      pointsCell.classList.add('points');
      row.appendChild(pointsCell);

      tableBody.appendChild(row);
    });
  }

  #sendToServer(context) { this.#tournament.socket.send(JSON.stringify( context ));}
}
