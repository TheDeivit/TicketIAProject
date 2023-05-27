from djongo import models
from django.utils import timezone
from bson.objectid import ObjectId

class Base(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=255)

    @property
    def pk(self):
        return self._id
    
    def __str__(self):
        return self.name
    
    class Meta:
        abstract = True

class Location(Base):
    class Meta:
        verbose_name_plural = "Locations"

class Urgency(Base):
    class Meta:
        verbose_name_plural = "UrgencyLevels"

class Status(Base):
    class Meta:
        verbose_name_plural = "Status"



# Create your models here.
class Ticket(Base):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    urgency = models.ForeignKey(Urgency, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=ObjectId("6472217d988c9a90e9aadfea"))