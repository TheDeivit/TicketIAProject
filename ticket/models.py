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
        verbose_name_plural = "Ubicaciones"

class Urgency(Base):
    class Meta:
        verbose_name_plural = "Niveles de Urgencia"

class Status(Base):
    class Meta:
        verbose_name_plural = "Estados"

class Category(Base):
    class Meta:
        verbose_name_plural = "Categorias"

class Department(Base):
    class Meta:
        verbose_name_plural = "Departamentos"


# Create your models here.
class Ticket(Base):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    urgency = models.ForeignKey(Urgency, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    deadline = models.DateField()
    #evidence = models.FileField(upload_to='evidences/', blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "Tickets"