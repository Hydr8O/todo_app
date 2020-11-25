from django.db import models
from django.db.models import Min, Max, Count
from django.contrib.auth.models import User

class TodoManager(models.Manager):
    def get_average_per_day(self, user):
        aggregate = self.filter(completed_at__isnull=False, user=user).aggregate(min_date=Min('completed_at'), max_date=Max('completed_at'), overall_number=Count('pk'))
        if aggregate.get('min_date'):
            number_of_days = (aggregate.get('max_date').date() - aggregate.get('min_date').date()).days + 1
            average = aggregate.get('overall_number') / number_of_days
            return average
        else:    
            return 0

    def get_n_completed_by_date(self, user, date):
        n_completed_today = len(self.get_completed_by_date(user, date))
        return n_completed_today

    def get_completed_by_date(self, user, date):
        completed = Todo.objects.filter(
            user=user, 
            completed_at__date=date
        )
        return completed

    def get_n_completed(self, user):
        n_completed = len(
            Todo.objects.filter(
                user=user, 
                completed_at__isnull=False
            )
        )
        return n_completed

class Todo(models.Model):
    title = models.CharField(max_length=70)
    memo = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = TodoManager()

    def __str__(self):
        return self.title