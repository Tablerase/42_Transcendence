from channels.db import database_sync_to_async

from game.models import Tournament


async def get_results_context(tournament_id):
  results = await get_tournament_results(tournament_id)
  context = {
    'message': 'results',
    'results' : results
  }
  return context


@database_sync_to_async
def get_tournament_results(tournament_id):
  tournament = Tournament.objects.get(id=tournament_id)
  return tournament.get_leaderboard()
