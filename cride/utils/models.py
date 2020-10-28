""" Django models utilities. """

#Django
from django.db import models

class CRideModel(models.Model):
    """ Comparte Ride base model

    CRideModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes.
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """
    created = models.DateTimeField(
        'created at',
        auto_now_add= True,
        help_text='Date time on which the object was created.'
    )

    modified = models. DateTimeField(
        'modified at',
        auto_now=True,
        help_text='Date time on which the object was last modified'
    )

    class Meta:
        """Meta option"""
        abstract = True
        #Abstract evita que se cree una tabla en la base
        get_latest_by = 'created'
        #los signos negativos significan en orden descendiente
        ordering = ['-created', '-modified']
"""
#Ejemplo multitabla
class Student(CRideModel):
    name = models.CharField()
    # Hereda de CRmodel

    class Meta(CRideModel.META):
        #Al heredar .META, se suma al meta de la clase superior.
        db_table = 'student_role'



# Ejemplo de proxy
class Person(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()

class MyPerson(Person):
    class Meta:
        proxy = True

    def say_hi(name):
        pass

#Con esto se implementa la funcion sin necesidad de afectar el modelo.
MyPerson.objects.all()
ricardo = MyPerson.objects.get(pk=1)
ricardo.say_hi('Gabospa')

rulo = Person.objects.get(pk=2)
rulo.say_hi('Gabospa') # Esto fallaría ya que no existe

"""
