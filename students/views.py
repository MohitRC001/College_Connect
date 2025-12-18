from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from .models import *


# Create your views here.




@login_required
def all_students(request):
    students = User.objects.all()
    return render(request, 'students/all_students.html', {'students':students})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        student_form = StudentRegisterForm(request.POST, request.FILES)

        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()

            # Create student record
            student = student_form.save(commit=False)
            student.user = user

            if not student.profile_image:
                student.profile_image = "default/profile.png"
            
            student.save()

            messages.success(request, "Your account has been created!")

            # auto login after register
            login(request, user)

            return redirect('home')

    else:
        user_form = UserRegisterForm()
        student_form = StudentRegisterForm()

    return render(request, 'registration/register.html', {
        'user_form': user_form,
        'student_form': student_form,
    })




@login_required
def edit_profile(request):
    student = request.user.student

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        student_form = StudentEditForm(request.POST, request.FILES, instance=student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        student_form = StudentEditForm(instance=student)

    return render(request, 'students/edit_profile.html', {
        'user_form': user_form,
        'student_form': student_form,
    })





@login_required
def  view_profile(request,student_id):
    try:
        student = get_object_or_404(Student, pk=student_id)

        followers = len(student.followers.all())
        following = len(student.following.all())

        # follow_request_status = 

        if not(request.user.is_staff) and student.received_follow_request.filter(sender=request.user.student).exists():
            follow_request = get_object_or_404(FollowRequest, sender=request.user.student, receiver = student)
            follow_request_status = follow_request.status
        else:
            follow_request_status = ""
    except Exception as e:
        student = dict()
        print(f"\nAn unexpected error at students > views > view_profile : {e}\n")
        return redirect('home')
    return render(request,'students/view_profile.html', {'student':student, 'follow_request_status':follow_request_status, 'followers':followers, 'following':following})






@login_required
def profile(request):
    try:
        student = get_object_or_404(Student, pk=request.user.student.uid)

        followers = len(student.followers.all())
        following = len(student.following.all())

    except Exception as e:
        student = dict()
        print(f"\nAn unexpected error at students > views > profile : {e}\n")
        return redirect('home')
    return render(request,'students/profile.html', {'student':student, 'followers':followers, 'following':following})




@login_required
def send_follow_requests(request, student_id):
    try:
        receiver = get_object_or_404(Student, pk=student_id)

        if receiver == request.user.student:
            return redirect("home")
        
        # if not(receiver.followers.contains(request.user.student)):
        follow_request = FollowRequest.objects.get_or_create(
            sender = request.user.student,
            receiver = receiver,
        )

        
        if follow_request[0].status == 'rejected':
            follow_request[0].status = 'pending'
            follow_request[0].save()


    except Exception as e:
        print(f"\nAn unexpected error at students > views > send_follow_requests : {e}\n")
        return redirect('home')
    
    return redirect('view_profile',student_id)



@login_required
def delete_follow_requests(request, student_id):
    try:
        receiver = get_object_or_404(Student, pk=student_id)
        follow_request = FollowRequest.objects.filter(sender=request.user.student, receiver = receiver)
        if follow_request:
            follow_request.delete()

    except Exception as e:
        print(f"\nAn unexpected error at students > views > send_follow_requests : {e}\n")
        return redirect('home')
    
    next_url = request.GET.get("next")
    if next_url : 
        return redirect(next_url)
    else:
        return redirect('view_profile', student_id)



@login_required
def accept_follow_requests(request, request_id):
    try:
        follow_request = get_object_or_404(FollowRequest, pk=request_id)
        
        follow_request.status = 'accepted'
        follow_request.save()

        follow_request.receiver.followers.add(follow_request.sender)
        follow_request.receiver.save()

    except Exception as e:
        print(f"\nAn unexpected error at students > views > accept_follow_requests : {e}\n")
        return redirect('home')
    
    return redirect('received_follow_requests')



@login_required
def reject_follow_requests(request, request_id):
    try:
        follow_request = get_object_or_404(FollowRequest, pk=request_id)
        
        follow_request.status = 'rejected'
        follow_request.save()


    except Exception as e:
        print(f"\nAn unexpected error at students > views > accept_follow_requests : {e}\n")
        return redirect('home')
    
    return redirect('received_follow_requests')



@login_required
def unfollow(request, student_id):
    try:
        receiver = get_object_or_404(Student, pk=student_id)

        if receiver == request.user.student:
            return redirect("home")
        
        receiver.followers.remove(request.user.student)

        follow_request = FollowRequest.objects.get_or_create(
            sender = request.user.student,
            receiver = receiver,
        )

        follow_request[0].delete()

    except Exception as e:
        print(f"\nAn unexpected error at students > views > unfollow : {e}\n")
        return redirect('home')
    
    next_url = request.GET.get("next")
    if next_url : 
        return redirect(next_url, request.user.student.uid)
    else:
        return redirect('view_profile', student_id)
    



@login_required
def remove_follower(request, student_id):
    try:
        follower = get_object_or_404(Student, pk=student_id)

        if follower == request.user.student:
            return redirect("home")
        
        follower.following.remove(request.user.student)

        follow_request = FollowRequest.objects.get_or_create(
            sender = follower,
            receiver = request.user.student,
        )

        follow_request[0].delete()

    except Exception as e:
        print(f"\nAn unexpected error at students > views > remove_follower : {e}\n")
        return redirect('home')
    
    return followers(request, request.user.student.uid)



@login_required
def sent_follow_requests(request):
    sent_requests = FollowRequest.objects.filter(sender = request.user.student).order_by('updated_at').reverse()
    return render(request, 'students/sent_follow_requests.html', {'sent_requests':sent_requests})




@login_required
def received_follow_requests(request):
    recevied_requests = FollowRequest.objects.filter(receiver = request.user.student).order_by('updated_at').reverse()
    return render(request, 'students/received_follow_requests.html', {'recevied_requests':recevied_requests})



def followers(request):
    try:
        followers = request.user.student.followers.all()
    except Exception as e:
        student = dict()
        print(f"\nAn unexpected error at students > views > followers : {e}\n")
        return redirect('home')
    return render(request,'students/followers.html',{'followers':followers})


def followings(request):
    try:
        followings = request.user.student.following.all()
    except Exception as e:
        student = dict()
        print(f"\nAn unexpected error at students > views > followings : {e}\n")
        return redirect('home')
    return render(request,'students/followings.html',{'followings':followings})





@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill, created = Skill.objects.get_or_create(name=form.cleaned_data['name'])
            request.user.student.skills.add(skill)
            return redirect('profile')
    else:
        form = SkillForm()

    return render(request, 'students/add_edit_skill.html', {'form': form})



@login_required
def edit_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return redirect('all_skills')
    else:
        form = SkillForm(instance=skill)

    return render(request, 'students/add_edit_skill.html', {'form': form})


@login_required
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    request.user.student.skills.remove(skill)
    return redirect('all_skills')





@login_required
def add_interest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest, created = Interest.objects.get_or_create(name=form.cleaned_data['name'])
            request.user.student.interests.add(interest)
            return redirect('profile')
    else:
        form = InterestForm()

    return render(request, 'students/add_edit_interest.html', {'form': form})


@login_required
def edit_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            return redirect('all_interests')
    else:
        form = InterestForm(instance=interest)

    return render(request, 'students/add_edit_interest.html', {'form': form})


@login_required
def delete_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)
    request.user.student.interests.remove(interest)
    return redirect('all_interests')





@login_required
def add_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.student = request.user.student
            exp.save()
            return redirect('profile')
    else:
        form = ExperienceForm()

    return render(request, 'students/add_edit_experience.html', {'form': form})



@login_required
def edit_experience(request, exp_id):
    exp = get_object_or_404(Experience, id=exp_id)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=exp)
        if form.is_valid():
            form.save()
            return redirect('all_experiences')
    else:
        form = ExperienceForm(instance=exp)

    return render(request, 'students/add_edit_experience.html', {'form': form})


@login_required
def delete_experience(request, exp_id):
    exp = get_object_or_404(Experience, id=exp_id)
    exp.delete()
    return redirect('all_experiences')


@login_required
def all_skills(request):
    return render(request, 'students/all_skills.html')


@login_required
def all_interests(request):
    return render(request, 'students/all_interests.html')


@login_required
def all_experiences(request):
    return render(request, 'students/all_experiences.html')

@login_required
def explore_students(request):

    if request.user.is_staff:
        students = Student.objects.all()
    else:
        current_student = request.user.student  

        students = Student.objects.exclude(uid=current_student.uid)

    # Get filter parameters
    skill = request.GET.get('skill')
    interest = request.GET.get('interest')
    course = request.GET.get('course')
    year = request.GET.get('year')
    college = request.GET.get('college')

    # Apply filters dynamically
    if skill:
        students = students.filter(skills__id=skill)

    if interest:
        students = students.filter(interests__id=interest)

    if course:
        students = students.filter(course=course)

    if year:
        students = students.filter(year=year)

    if college:
        students = students.filter(college=college)

    # Remove duplicates
    students = students.distinct()

    context = {
        "students": students,
        "skills": Skill.objects.all(),
        "interests": Interest.objects.all(),
        "years": [{"value":"FY", "label":"First Year"}, {"value":"SY", "label":"Second Year"}, {"value":"TY", "label":"Third Year"}]
    }

    return render(request, "students/explore.html", context)

