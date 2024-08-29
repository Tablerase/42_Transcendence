// Assuming tournamentId is defined in the template
if (typeof tournamentId !== 'undefined') {
  const tournamentSocket = new WebSocket(
      'ws://' + window.location.host + '/ws/tournament/' + tournamentId + '/'
  );

  tournamentSocket.onopen = function(e) {
      console.log('WebSocket connection established for tournament:', tournamentId);
  };

  tournamentSocket.onclose = function(e) {
      console.error('WebSocket connection closed for tournament:', tournamentId);
  };
} else {
  console.error('tournamentId is not defined');
}
