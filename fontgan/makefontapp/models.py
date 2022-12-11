from django.db import models


def user_directory_path(instance, filename):
    # postdate = instance.postdate.strftime('%y-%m-%d_%a_%H:%M')
    postdate = instance.postdate.strftime('%y-%m-%d-%H-%M')
    return f'uploads/userwords/{instance.owner_id}/{postdate}/{filename}'

class Images(models.Model):
    owner_id = models.EmailField()    
    postdate = models.DateTimeField(auto_now_add=True)
    attached = models.FileField('image', upload_to=user_directory_path)


    def __str__(self):
        return f"{self.id} . {self.postdate} ."