from djongo import models
from django.utils import timezone
from bson.objectid import ObjectId
from django.contrib.auth.models import User

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

class SpecialCase(Base):
    class Meta:
        verbose_name_plural = "Casos"

class CategoryType(Base):
    class Meta:
        verbose_name_plural = "Tipo de Categoria"

class Category(Base):
    categorytype = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Categorias"

class Department(Base):
    class Meta:
        verbose_name_plural = "Departamentos"

class Specialty(Base):
    class Meta:
        verbose_name_plural = "Especialidad"

# Create your models here.
class Ticket(Base):
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    urgency = models.ForeignKey(Urgency, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    specialCase = models.ForeignKey(SpecialCase, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    deadline = models.DateField()
    technician = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="technician")
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    #evidence = models.FileField(upload_to='evidences/', blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "Tickets"

class Profile(Base):
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    
    class Meta:
        verbose_name_plural = "Perfil de Usuario"

