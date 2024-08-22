document.addEventListener('DOMContentLoaded', function() {
    // Send Friend Request
    var sendFriendForm = document.getElementById('send-friend-form');
    if (sendFriendForm) {
        sendFriendForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var actionUrl = this.action;
            var userId = actionUrl.split('/').filter(Boolean).pop();
            console.log('Sending friend request for user ID:', userId);

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                var actionElement = document.getElementById('friend-action-' + userId);
                if (actionElement) {
                    actionElement.innerHTML = '<i class="' + data.icon + '"></i>';
                } else {
                    console.error('Element not found for ID: friend-action-' + userId);
                }
            });
        });
    }

    // Accept Friend Request
    var acceptFriendForm = document.getElementById('accept-friend-form');
    if (acceptFriendForm) {
        acceptFriendForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var userId = this.getAttribute('data-user-id');
            console.log('Accepting friend request for user ID:', userId);

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data.status === 'friend') {
                    var actionElement = document.getElementById('friend-action-' + userId);
                    if (actionElement) {
                        actionElement.innerHTML = '<i class="' + data.icon + '"></i>';
                    } else {
                        console.error('Element not found for ID: friend-action-' + userId);
                    }
                } else {
                    console.error('Unexpected status:', data.status);
                }
            })
            .catch(error => console.error('Error processing the fetch response:', error));
        });
    }

    // Remove Friend
    var removeFriendForm = document.getElementById('remove-friend-form');
    if (removeFriendForm) {
        removeFriendForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var actionUrl = this.action;
            var userId = actionUrl.split('/').filter(Boolean).pop();
            console.log('Removing friend with user ID:', userId);

            fetch(this.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => response.json())
            .then(data => {
                var actionElement = document.getElementById('friend-action-' + userId);
                if (actionElement) {
                    actionElement.innerHTML = '<i class="' + data.icon + '"></i>';
                } else {
                    console.error('Element not found for ID: friend-action-' + userId);
                }
            });
            
        });
    }
});

// Utility function to get the CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}