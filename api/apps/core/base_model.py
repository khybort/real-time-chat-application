from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
    
    
    def soft_delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
    
    @classmethod
    def active_objects(cls):
        return cls.objects.filter(is_deleted=True)