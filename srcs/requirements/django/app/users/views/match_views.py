from django.http import JsonResponse
from django.template.loader import render_to_string
from users.utils import generate_dummy_matches
from django.shortcuts import get_object_or_404
from users.models.User_model import CustomUser


def match_detail_view(request, match_id):
    username = request.GET.get('username')
    user_profile = get_object_or_404(CustomUser, username=username)
    
    dummy_matches = generate_dummy_matches(user_profile)

    # Find the match by ID
    match = next((m for m in dummy_matches if m.id == match_id), None)
    if not match:
        return JsonResponse({'error': 'Match not found'}, status=404)

    # Render the _fighting_card.html template with the match context
    rendered_html = render_to_string('users/partials/_fighting_card.html', {'match': match})
    return JsonResponse({'html': rendered_html})