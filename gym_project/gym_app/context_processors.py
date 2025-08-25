from .models import Enrollment

def enrollment_status(request):
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user).exists()
    return {'is_enrolled': is_enrolled}
