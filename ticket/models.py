from djongo import models

class Location(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)

    @property
    def pk(self):
        return self._id
    
    def __str__(self):
        return self.name
# Create your models here.
class Ticket(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)
    content = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    @property
    def pk(self):
        return self._id
    
    def __str__(self):
        return self.name