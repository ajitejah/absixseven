from django.db import models
from django.db.models import Avg
from app_roadmap.models import Roadmap, Assignment, Submission
from app_auth.models import Student


# 🧾 EVALUATION (1 student = 1 roadmap)
class Evaluation(models.Model):
    roadmap     = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='evaluations')
    student     = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='evaluations')

    # 📊 ANALYTICS
    average     = models.FloatField(default=0)    
    progress    = models.FloatField(default=0)     
    rank        = models.PositiveIntegerField(null=True, blank=True)  
    predict     = models.FloatField(default=0)  
    confirmed = models.BooleanField(default=False) 

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('roadmap', 'student')

    def __str__(self):
         return f"{self.student.user.first_name} - {self.roadmap.name}"

    # 🔥 OPTIONAL: helper update average
    def update_average(self):
        avg = self.scores.aggregate(avg=Avg('score'))['avg']
        self.average = avg if avg else 0
        self.save()

# 📊 SCORE (detail nilai per submission)
class Score(models.Model):
    evaluation  = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name='scores')
    submission  = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='scores')
    assignment  = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='scores')
    score       = models.FloatField()
    feedback    = models.TextField(blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('evaluation', 'submission')

    def __str__(self):
        return f"{self.evaluation.student.user.first_name} - {self.assignment.title} - {self.score}"