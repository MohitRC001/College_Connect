from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True



class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="experiences")
    title = models.CharField(max_length=100)  
    description = models.TextField(blank=True)
    years = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.student.user.username})"



class Student(BaseModel):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student"
    )

    bio = models.TextField(
        max_length=300,
        default=" "
    )

    college = models.TextField(
        max_length=300,
    )
    
    course = models.CharField(
        max_length=20,
        choices=[('MCA','MCA'),('MBA','MBA'),('BCA','BCA'),('BSC','BSC'),]
    )
    
    year = models.CharField(
        max_length=2,
        choices=[('FY','First Year'),('SY','Second Year'),('TY','Third Year'),]
    )
    
    mobile = models.IntegerField(
        unique=True,
    )
    
    profile_image = models.ImageField(
        upload_to='profile',
        blank=True,
        null=True
    )
    
    followers = models.ManyToManyField(
        'self',
        related_name="following",
        symmetrical=False,
        blank=True
    )

    skills = models.ManyToManyField(Skill, blank=True, related_name='student')
    interests = models.ManyToManyField(Interest, blank=True, related_name='student')

    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return self.user.username





class FollowRequest(BaseModel):
    STATUS_CHOICES = (
        (("pending","Pending")),
        (("accepted","Accepted")),
        (("rejected","Rejected")),
    )

    sender = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='sent_follow_request',
    )
    receiver = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='received_follow_request',
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        unique_together = ('sender','receiver')
    
    def __str__(self):
        return f"{self.sender} -> {self.receiver}. ({self.status})"
    