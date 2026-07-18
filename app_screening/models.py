from django.db import models


class PlacementQuestion(models.Model):
    question    = models.TextField()
    image       = models.ImageField(upload_to='screening/questions/', null=True, blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question[:60]


class PlacementOption(models.Model): 
    answer      = models.CharField(max_length=255) 
    score       = models.IntegerField(default=0) 
    order       = models.PositiveIntegerField(default=0)
 
    question    = models.ForeignKey(PlacementQuestion, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.answer


class PlacementResult(models.Model):  
    score = models.IntegerField(default=0) 
    
    # simpan jawaban mentah (untuk audit / debug / recalculation)
    raw_data = models.JSONField(null=True, blank=True)

    student = models.OneToOneField('app_auth.Student', on_delete=models.CASCADE, related_name='placement_result')
    level = models.ForeignKey('app_auth.Level', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.email} - {self.level.name}"