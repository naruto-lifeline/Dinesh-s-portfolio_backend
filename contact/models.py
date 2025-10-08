from django.db import models

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def _str_(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-submitted_at']