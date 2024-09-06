document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("match-modal");
    const modalContent = document.getElementById("match-details");
    const loadingText = document.getElementById("loading-text");
    const span = document.getElementsByClassName("close")[0];

    modal.style.display = "none";
    document.querySelectorAll(".match-item").forEach(item => {
      item.addEventListener("click", function() {
        const matchId = this.getAttribute("data-match-id");
        const username = this.getAttribute("data-username");

        const url = `/match-detail/${matchId}/?username=${username}`;

        loadingText.style.display = 'block';
        fetch(url)
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            loadingText.style.display = 'none';
            if (data.html) {
              modalContent.innerHTML = data.html;
              modal.style.display = "block";
            } else {
              alert('Failed to load match details.');
            }
          })
          .catch(error => {
            loadingText.style.display = 'none';
            console.error('Error fetching match details:', error);
            alert('Failed to load match details. Please try again.');
          });
      });
    });

    function closeModal() {
      modal.style.display = "none";
      const backdrops = document.getElementsByClassName('modal-backdrop');
      Array.from(backdrops).forEach(backdrop => backdrop.remove());
    }
    
    span.onclick = closeModal;
    window.onclick = function(event) {
      if (event.target == modal) {
        closeModal();
      }
    }
});