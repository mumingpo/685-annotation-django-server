from django.db import models

# Create your models here.

class Tweet(models.Model):
    text = models.CharField(max_length=1000)

class Annotator(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=128)
    password = models.CharField(max_length=16)

class Annotation(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    annotator = models.ForeignKey(Annotator, on_delete=models.CASCADE)
    choices = [
        (0, "Not annotated"),
        (1, "Positive sentiment"),
        (2, "Negative sentiment"),
        (3, "Unintelligible tweet"),
    ]
    choice = models.PositiveSmallIntegerField(
        choices=choices,
        default=0,
    )
    order = models.PositiveSmallIntegerField(null=True)
    time_filled = models.DateTimeField(auto_now=True)

    def get_display_id(self):
        raise NotImplementedError("Should not be used again")
        #return (self.id - 32) % 250 + 1

    def get_choice_text(self):
        return dict(self.choices).get(self.choice)
