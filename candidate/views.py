import bleach
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import SavedJob, AppliedJob, SavedCompany
from django.shortcuts import get_object_or_404
from rest_framework import status
from job.models import Job
from rest_framework.response import Response
from company.models import Company
from playfairauth.serializers import BaseUserProfileSerializer, FullUserProfileSerializer
from candidate.models import AppliedJob, SavedJob
from playfairauth.models import CustomUserProfile, CustomUserModel
from playfairauth.serializers import CustomUserSerializer, FullCustomUserSerializer
from django.db import transaction
from .serializers import AppliedJobSerializer, CandidateSavedJobSerializer
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password
from message.models import Message
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .filters import CandidateFilter
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group

bleached_tags = ['p', 'b', 'br', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'em', 'a', 'div', 'strong']
bleached_attr = ['class', 'href', 'style']

def is_candidate(user):
    if(user.groups.filter(name='candidate').exists()):
        return True
    else:
        return Response({"message": "Only candidates can access this route."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 

@api_view(['POST'])
@user_passes_test(is_candidate)
@permission_classes([IsAuthenticated])
def save_job(request, pk):
    try:
        user = request.user
        job = get_object_or_404(Job, id=pk)
        
        SavedJob.objects.create(
            user = user,
            job = job
        )
        return Response({ "message": "Successfully saved job." }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsave_job(request, pk):
    try:

        user = request.user
        job = Job.objects.filter(id=pk).get()
        exists = SavedJob.objects.filter(job=job, user=user).first()

        if exists == None:
            return Response({ "error": "Could not find job." }, status=status.HTTP_200_OK)    
        
        exists.delete()
        return Response({ "message": "Successfully unsaved job." }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_company(request, pk):
    try:
        user = request.user
        company = get_object_or_404(Company, id=pk)
        savedCompany = SavedCompany.objects.create(
            saved = True,
            user = user,
            company = company
        )
        savedCompany.save()
        return Response({ "message": "Successfully saved company." }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_candidate)
def upgrade_to_company(request):
    try:
        data = request.data
        user = request.user
        
        if Company.objects.filter(email=bleach.clean(data['email'])).exists():
            return Response({ "error": "Email in already in use."}, status=status.HTTP_200_OK)
        
        if CustomUserModel.objects.filter(email=bleach.clean(data['email'])).exists():
            return Response({ "error": "Email in already in use."}, status=status.HTTP_200_OK)
        
        candidateGroup = Group.objects.get(name='candidate') 
        companyGroup = Group.objects.get(name='company') 
        user.groups.remove(candidateGroup)
        companyGroup.user_set.add(user)
        user = CustomUserModel.objects.filter(email=user.email).first()
        company = Company.objects.create(
            name = bleach.clean(data['name']),
            description = bleach.clean(data['description'], attributes=bleached_attr, tags=bleached_tags),
            email = bleach.clean(data['email']),
            phone = bleach.clean(data['phone']),
            industry = bleach.clean(data['industry']),
            address = bleach.clean(data['address']),
            country = bleach.clean(data['country']),
            founded_in = bleach.clean(data['founded_in']) if data['founded_in'] else datetime.today().year,
            website = data['website'],
            size = int(data['size']),
            state = bleach.clean(data['state']),
            city = bleach.clean(data['city']),
            lat = float(data['lat']),
            long = float(data['long']),
            facebook = bleach.clean(data['facebook']),
            twitter = bleach.clean(data['twitter']),
            instagram = bleach.clean(data['instagram']),
            linkedIn = bleach.clean(data['linkedIn']),
        )

        company.save()
        user.company = company.id
        user.email = bleach.clean(data['email'])
        user.save()
        
        return Response({ "message": "Successfully saved company.", "company": company.id }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @user_passes_test(is_candidate)
def upgrade_to_company_logo(request):
    try:
        user = CustomUserModel.objects.filter(email=request.user.email).first()
        user.image = request.FILES['logo']
        user.save()
        return Response({ "message": "Successfully added logo" }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsave_company(request, pk):
    try:

        user = request.user
        company = Company.objects.filter(id=pk).get()
        exists = SavedCompany.objects.filter(company=company, user=user).first()

        if exists == None:
            return Response({ "error": "Could not find company." }, status=status.HTTP_200_OK)    
        
        exists.delete()
        return Response({ "message": "Successfully unsaved company." }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_to_job(request, pk):
    try:
        user = request.user
        user_profile = CustomUserProfile.objects.get(user=user)
        job = get_object_or_404(Job, id=pk)
        company = Company.objects.filter(id=job.company_id).first()
        
        if user_profile.resume == '':
            return Response({ 'error': 'Please upload your resume first.' }, status=status.HTTP_400_BAD_REQUEST)
        
        already_applied = AppliedJob.objects.filter(job=job, user=user).exists()

        if already_applied:
            return Response({ "error": "You have already applied for this job"}, status=status.HTTP_400_BAD_REQUEST)

        jobApplied = AppliedJob.objects.create(
            job = job,
            user = user,
            resume = user_profile.resume.url,
            coverLetter = request.data['coverLetter'],
            company = company,
            is_active = True
        )

        return Response({
            "applied": True,
            "job_id": jobApplied.id,
            "message": "Successfully Applied"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def upload_candidate_logo(request):
    data = request.data
    user = request.user
    userProfile = CustomUserProfile.objects.filter(user=user).first()

    if userProfile is not None:
        if 'logo' not in request.FILES:
            return Response({"error": "Please upload your logo"})
        else:
            userProfile.logo = request.FILES['logo']
            userProfile.save()
            
            return Response({
                "logo": userProfile.logo.url
            }, status=status.HTTP_200_OK)
    else:
        return Response({ "message" : "User not found, could not upload image"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def candidate_message_company(request):
    try:
        user = request.user
        user = CustomUserModel.objects.filter(id=user.id).first()
        company = Company.objects.filter(id=request.data['company']).first()
        c = {
            "company_email": company.email,
            'company_name': company.name,
            'user_email': user.email,
            'message': request.data['message'],
            'subject': request.data['subject']
        }
        msg_html = render_to_string('user_company_message.html', c)
        send_mail(f"Playfair Message - {request.data['subject']}", None, 'noreply@playfairwork.com', [company.email], html_message=msg_html)
        return Response({ "message": "Successfully sent message."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": "Erorr With" + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_candidate_resume(request):
    user = request.user
    profile = CustomUserProfile.objects.get(user=user)
    resume = request.FILES['resume']
    
    if resume == '' or resume == None:
        return Response({"error": "Please upload your resume"})

    profile.resume = resume
    profile.save()

    return Response({ "message": "Successfully Uploaded resume", "resume": profile.resume.url }, status=status.HTTP_200_OK)

@api_view(['GET'])
@transaction.atomic
def getAppliedJobs(request):
    try:
        jobs =  AppliedJobSerializer(AppliedJob.objects.filter(user=request.user.id), many=True).data
        return Response({ "jobs": jobs})
    except Exception as e:
        return Response({ "error": "Erorr With" + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@transaction.atomic
def get_applied_job(request, pk):
    try:
        application =  AppliedJobSerializer(AppliedJob.objects.filter(user=request.user.id, id=pk).first()).data
        return Response({ "candidate": application})
    except Exception as e:
        return Response({ "error": "Erorr With" + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@transaction.atomic
def get_saved_jobs(request):
    try:
        time = int(request.GET.get('createdAt'))
        today = date.today()
        months = today - relativedelta(months=time)
        savedJobs = CandidateSavedJobSerializer(SavedJob.objects.filter(user=request.user.id, createdAt__gte = months), many=True).data
        return Response({ "savedJobs": savedJobs })
    except Exception as e:
        return Response({ "error": "Erorr With" + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def delete_saved_job(request, pk):
    user = request.user
    if request.method == 'DELETE':
        job = SavedJob.objects.filter(id=pk, user=user).first()

        if job!= None:
            job.delete()
            return Response({ "message": "Successfully Deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Could not find job"}, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])        
def delete_resume(request):
    try:
        user = request.user
        userprofile = CustomUserProfile.objects.filter(user=user).first()
        userprofile.resume.delete()
        userprofile.save()
        return Response({ "message": "Successfully Deleted Resume."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def update_me(request):
    user = request.user
    data = request.data

    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != '':
        user.password = make_password(data['password'])

    user.save()

    serializer = CustomUserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_applied(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    applied = AppliedJob.objects.filter(job=job, user=user).exists()

    return Response(applied, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_candidate_me(request):
    try:
        data = request.data
        user = request.user
        user = CustomUserModel.objects.get(username=user)
        # user.email = data['email']
        user.save()
        userprofile = CustomUserProfile.objects.filter(user=user).first()

        if CustomUserProfile.objects.filter(user=user).exists() == False:
           return Response({ "error": "Could not find profile"}, status=status.HTTP_400_BAD_REQUEST)
        
        userprofile.address = data['address']
        userprofile.title = data['title']
        userprofile.city = data['city']
        userprofile.experience = data['experience']
        userprofile.country = data['country']
        userprofile.bio = data['bio']
        userprofile.linkedIn = data['linkedIn']
        userprofile.instagram = data['instagram']
        userprofile.state = data['state']
        userprofile.website = data['website']
        userprofile.postal_code = data['postal_code']
        userprofile.industry = data['industry']
        userprofile.interests = data['interests']
        userprofile.languages = data['languages']
        userprofile.allow_in_listings = data['allow_in_listings']
        userprofile.experience = data['experience']
        userprofile.expected_salary = data['expected_salary']
        userprofile.phone = data['phone']
        userprofile.is_expected_salary_visible = data['is_expected_salary_visible']
        userprofile.education_level = data['education_level']
        userprofile.save()

        if userprofile.country != None and userprofile.state != None and userprofile.title != None and userprofile.industry != None:
            user = CustomUserModel.objects.get(id=userprofile.user.id)
            user.is_complete = True
            user.save()
            userprofile.is_complete = True
            userprofile.save()

        return Response({ "userprofile": FullUserProfileSerializer(userprofile).data, 'is_complete': user.is_complete}, status=status.HTTP_200_OK)
    except Exception as e: 
        return Response({ "error": "Erorr With" + str(e)})
    

    
@api_view(['POST'])
def message_to_candidate(request):
    try:
        user = request.user
        user = CustomUserModel.objects.filter(id=user.id).first()
        company = Company.objects.filter(id=request.data['company']).first()
        c = {
            'name': request.data['name'],
            "message": request.data['message'],
            'email': request.data['email'],
        }
        msg_html = render_to_string('message_to_company.html', c)
        send_mail(f"Playfair - You've received a messasge", None, 'noreply@playfairwork.com', [user.email], html_message=msg_html)
        return Response({ "message": "Successfully sent message."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": "Erorr With" + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['GET'])
def get_candidates(request):
    order = "-first_name" if request.GET.get('orderBy') == 'desc' else "first_name"
    filterset = CandidateFilter(request.GET, CustomUserProfile.objects.all().order_by(order))
    count = filterset.qs.count()
    resPerPage = 50

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = BaseUserProfileSerializer(queryset, many=True)

    return Response({"candidates": serializer.data, "count": count, "resPerPage": 50}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_candidate(request, pk):
    try:
        profile = CustomUserProfile.objects.filter(id=pk).first()
        if profile == None:
            return Response(status.HTTP_404_NOT_FOUND)
        return Response({ "candidate": FullUserProfileSerializer(profile).data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e)}, status=status.HTTP_200_OK)
    
@api_view(['DELETE'])
def delete_logo(request):
    user = request.user
    if user == "AnonymousUser":
        return Response({})

    userProfile = CustomUserProfile.objects.filter(user=user).first()

    if userProfile != None:
        userProfile.logo.delete()
        userProfile.save()

        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_200_OK)