from djongo import models

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

#class Urgency(Base):
#    class Meta:
#        verbose_name_plural = "UrgencyLevels"

# Create your models here.
class Ticket(Base):
    content = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    #urgency = models.ForeignKey(Urgency, on_delete=models.PROTECT)