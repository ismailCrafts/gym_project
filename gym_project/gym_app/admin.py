from django.contrib import admin

# Register your models here.
from gym_app.models import ContactMessage,MembershipPlan,Enrollment,Trainer,Attendance,Member


# Register your models here.
admin.site.register(ContactMessage)
admin.site.register(MembershipPlan)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(Attendance)
admin.site.register(Member)