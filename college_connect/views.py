from django.shortcuts import render
from students.models import Student, Skill, Interest, FollowRequest
from django.db import models

from datetime import datetime

def home(request):
    if request.user.is_authenticated :
        students = Student.objects.exclude(user=request.user)
    else:
        students = Student.objects.all()
    return render(request, 'home.html', {
        "year": datetime.now().year,
        'students':students[:6]
    })


def generate_reports(request):
    context = {}

    # Student statistics
    context["total_students"] = Student.objects.count()
    context["by_course"] = Student.objects.values("course").annotate(count=models.Count("uid"))
    context["by_year"] = Student.objects.values("year").annotate(count=models.Count("uid"))
    context["with_skills"] = Student.objects.filter(skills__isnull=False).distinct().count()
    context["with_interests"] = Student.objects.filter(interests__isnull=False).distinct().count()

    # Follower statistics
    context["most_followed"] = (
        Student.objects.annotate(follow_count=models.Count("followers"))
        .order_by("-follow_count")[:10]
    )

    # Follow request statistics
    context["pending_requests"] = FollowRequest.objects.filter(status="pending").count()
    context["accepted_requests"] = FollowRequest.objects.filter(status="accepted").count()
    context["rejected_requests"] = FollowRequest.objects.filter(status="rejected").count()

    return render(request, "adminpanel/reports.html", context)

from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_report_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="report.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)

    p.drawString(100, 800, "Admin Report")

    by_course = Student.objects.values("course").annotate(count=models.Count("uid"))

    y = 760
    stats = [
        f"Student Overview :-",
        f"Total Students: {Student.objects.count()}",
        f"Students with Skills: {Student.objects.filter(skills__isnull=False).distinct().count()}",
        f"Students with Interests: {Student.objects.filter(interests__isnull=False).distinct().count()}",
        f"Pending Requests: {FollowRequest.objects.filter(status='pending').count()}",
        f"Accepted Requests: {FollowRequest.objects.filter(status='accepted').count()}",
        f" ",
        f"Students By Course :-",
    ]

    for item in by_course:
        stats.append(f"{item['course']}: {item['count']}")

    stats.extend([" ", "Top 10 Most Followed Students :-"])

    most_followed = (
        Student.objects.annotate(follow_count=models.Count("followers"))
        .order_by("-follow_count")[:10]
    )

    for s in most_followed:
        stats.append(f"{s.get_full_name()}: {s.followers.count()} followers")

    p.setFont("Times-Roman", 16)

    for line in stats:
        p.drawString(80, y, line)
        y -= 25

    p.showPage()
    p.save()
    return response

