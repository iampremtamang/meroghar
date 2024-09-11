from django.db import models

class BaseModel(models.Model):
    """
    An abstract base model that provides timestamp fields for tracking 
    when an object is created and last updated.
    
    Attributes:
        created_at (DateTimeField): Automatically set to the current date and time when the object is first created.
        updated_at (DateTimeField): Automatically updated to the current date and time whenever the object is saved.
    
    This model can be inherited by other models to include automatic timestamp functionality.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True