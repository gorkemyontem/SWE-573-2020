from django.http import JsonResponse
from django.core import serializers
from scraper.models import Submission

def indexView(request):
    # form = FriendForm()
    friends = Submission.objects.all()
    return render(request, "index.html", {"friends": friends})

def postFriend(request):
    print(33)
    return JsonResponse({"error": ""}, status=400)
