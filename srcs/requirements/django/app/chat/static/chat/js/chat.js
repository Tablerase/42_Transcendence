document.getElementById('commentForm').addEventListener('submit', function(e) {
  if (e.target.dataset.authenticated !== 'true') {
    alert('You must be logged in to post a comment.');
    e.preventDefault();
    return;
  }
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  fetch(form.action, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      const chatContainer = document.getElementById('chatContainer');
      chatContainer.insertAdjacentHTML('beforeend', data.comment_html);
      chatContainer.lastElementChild.scrollIntoView();
      form.reset();
      }
  })
  .catch(error => console.error('Error:', error));
});