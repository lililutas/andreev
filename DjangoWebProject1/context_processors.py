
from app.models import UserProfile

def UserProfiles(request):
    if request.user.is_authenticated:
        currentUser, status = UserProfile.objects.get_or_create(user = request.user)
        if status: 
            currentUser.role = 'client'
            currentUser.choosedSide = 'none'
    else:
        currentUser = None    
    return {
            'currentUser': currentUser
            }