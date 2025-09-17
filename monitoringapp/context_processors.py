from .models import User

# context_processors.py
def logged_in_user(request):
    user = None
    is_team_lead = False
    if request.session.get("user_id"):
        try:
            user = User.objects.get(id=request.session["user_id"])
            if user.job_Position.lower() == "team lead":
                is_team_lead = True
        except User.DoesNotExist:
            pass
    return {"logged_in_user": user, "is_team_lead": is_team_lead}

