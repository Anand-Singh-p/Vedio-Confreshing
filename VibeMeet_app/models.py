# import uuid
# from django.db import models
# from django.contrib.auth.models import User

# class Meeting(models.Model):
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     start_time = models.DateTimeField()
#     meeting_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4)

#     def __str__(self):
#         return self.title
from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    id=models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


