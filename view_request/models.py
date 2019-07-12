from django.db import models

class Blog(models.Model):
    title=models.CharField(max_length=100)
    pub_date=models.DateTimeField('date published')
    body=models.TextField()

    def __str__(self):
        return self.title
        
    def summary(self):
        return self.body[:100] #100글자까지만 출력해라
# Create your models here.
