from django.shortcuts import render
from rest_framework.response import Response
from job.models import Job
from playfairauth.models import CustomUserModel, CustomUserProfile 
from playfairauth.serializers import BaseUserProfileSerializer
from candidate.models import AppliedJob
from rest_framework.decorators import api_view, permission_classes
from company.serializers import CompanySerializer, BaseCompanySerializer, ProfileCompanySerializer
from company.filters import CompanyFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework import status
from job.serializers import JobSerializer, BaseJobSerializer
from candidate.serializers import AppliedJobSerializer, BaseAppliedJobSerializer
from candidate.models import AppliedJob
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from datetime import date
from dateutil.relativedelta import relativedelta
from django.conf import settings
from company.models import Company, SavedCompanies
import bleach
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache


CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

bleached_tags = ['p', 'b', 'br', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'span', 'em', 'a', 'div', 'strong', 'li', 'ol', 'ul']
bleached_attr = ['class', 'href', 'style']

@api_view(['GET'])
def get_companies(request):
    try:
        order = "-name" if request.GET.get('orderBy') == 'desc' else "name"
        filterset = CompanyFilter(request.GET, queryset=Company.objects.all().order_by(order))   
        total = filterset.qs.count()
        per_page = 50
        paginator = PageNumberPagination()
        paginator.page_size = per_page
        queryset = paginator.paginate_queryset(filterset.qs, request)
        serializer = BaseCompanySerializer(queryset, many=True, context={'request': request})

        return Response({
            "total": total,
            "companies": serializer.data,
            "per_page": per_page,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #     if cache.get('companies'):
    #         filterset = cache.get('companies')
    #     else:
    #         filterset = Company.objects.all()
    #         cache.set('companies', filterset)
            
    #     order = "-name" if request.GET.get('orderBy') == 'desc' else "name"
    #     filterset = CompanyFilter(request.GET, queryset=filterset.order_by(order))
    #     total = filterset.qs.count()
    #     per_page = 50
    #     paginator = PageNumberPagination()
    #     paginator.page_size = per_page
    #     queryset = paginator.paginate_queryset(filterset.qs, request)
    #     serializer = BaseCompanySerializer(queryset, many=True, context={'request': request})

    #     return Response({
    #         "total": total,
    #         "companies": serializer.data,
    #         "per_page": per_page,
    #     }, status=status.HTTP_200_OK)
    # except Exception as e:
    #     return Response({ "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
def get_company(request, pk):
    try:
        company = get_object_or_404(Company, id=pk)
        companySerialized = CompanySerializer(company, many=False, context={'request': request})
        related_jobs = Job.objects.filter(company_id=company.id).select_related('company')[:2] 
        related_jobs = BaseJobSerializer(related_jobs, many=True)
        related_companies = Company.objects.filter(industry=company.industry).exclude(id=pk)[:3] 
        related_companies = CompanySerializer(related_companies, many=True, context={'request': request})
        return Response({
            "company": companySerialized.data,
            "relatedJobs": related_jobs.data,
            "relatedCompanies": related_companies.data
        }, status=status.HTTP_200_OK)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def read_my_company(request):
    try:
        user = request.user
        company = get_object_or_404(Company, user=user)
        company = BaseCompanySerializer(company)
        userProfile = CustomUserProfile.objects.filter(user=user).first()
        return Response({"company": company.data, "userProfile": BaseUserProfileSerializer(userProfile).data},status=status.HTTP_200_OK)
    except Exception:
        return Response({"message": "Company Not Found"},status=status.HTTP_404_NOT_FOUND)    

@api_view(['PUT'])
def update_my_company(request):
    print('ran file')
    data = request.data
    user = request.user
    company = get_object_or_404(Company, user=user)
    if company == None:
        return Response({
            'message': 'You can not update this company'
        }, status=status.HTTP_403_FORBIDDEN)

    company.name = bleach.clean(data['name']) if bleach.clean(data['name']) != None else None
    company.description = bleach.clean(data['description']) if data['description'] else None
    company.email = bleach.clean(data['email']) if data['email'] else None
    company.phone = bleach.clean(data['phone']) if data['phone'] else None
    company.address = bleach.clean(data['address']) if data['address'] else None
    company.country = bleach.clean(data['country']) if data['country'] else None
    company.city = bleach.clean(data['city']) if data['city'] else None
    company.industry = bleach.clean(data['industry']) if data['industry'] else None
    company.founded_in = int(data['founded_in']) if data['founded_in'] else None
    company.website = bleach.clean(data['website']) if data['website'] else None
    company.size = int(data['size']) if data['size'] else None
    company.country = bleach.clean(data['country']) if data['country'] else None
    company.state = bleach.clean(data['state']) if data['state'] else None
    company.lat = float(data['lat']) if data['lat'] else None
    company.long = float(data['long']) if data['long'] else None
    company.facebook = bleach.clean(data['facebook']) if data['facebook'] else None
    company.twitter = bleach.clean(data['twitter']) if data['twitter'] else None
    company.instagram = bleach.clean(data['instagram']) if data['instagram'] else None
    company.linkedIn = bleach.clean(data['linkedIn']) if data['linkedIn'] else None
    company.save()

    # if(company.name != None and company.description != None and company.country != None and company.state != None 
    #    and company.city != None, company.lat != None, company.long != None):
    #     user = CustomUserModel.objects.filter(id=user.id).first()
    #     user.is_complete = True
    #     user.save()
    #     company.is_complete = True
    #     company.save()

    company = CompanySerializer(company)
    return Response({"message": "Successfully Updated"},status=status.HTTP_200_OK)

@api_view(['DELETE'])
def deleteLogo(request):
    user = request.user
    if user == "AnonymousUser":
        return Response({})

    company = Company.objects.filter(company_user=user).first()
    company.company_logo.delete()
    company.save()
    return Response({
        "company": CompanySerializer(company).data
    }, status=status.HTTP_200_OK)

@api_view(['PUT'])
def upload_company_logo(request):
    user = CustomUserModel.objects.get(id=request.user.id)

    if user != None:
        if 'logo' not in request.FILES:
            return Response({"error": "Please upload your logo"})
        else:
            user.image.delete()
            user.image = request.FILES['logo']
            user.save()

        return Response({
            "image": user.image.url
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Could not find Company"
        })
    
@api_view(['PUT'])
def update_my_logo(request):
    user = request.user
    company = Company.objects.get(user=user)

    if company != None:
        if 'logo' not in request.FILES:
            return Response({"error": "Please upload your logo"})
        else:
            company.logo.delete()
            company.logo = request.FILES['logo']
            company.save()

        return Response({
            "logo": company.logo.url
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "message": "Could not find company"
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_company_jobs(request):
    try:
        user = request.user
        company = Company.objects.filter(user=user).first()
        jobs = Job.objects.filter(company=company.id)
        candidates = []
        
        for job in jobs:
            candidates.append(AppliedJob.objects.filter(job=job.id).values())

        return Response({ "jobs": BaseJobSerializer(jobs, many=True).data, "candidates": candidates }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
@api_view(['GET'])
def getMyCompanyJobCandidates(request):
    user = request.user
    company = Company.objects.filter(user=user).first()
    jobs = Job.objects.filter(company=company.id)
    jobArr = []
    time = 0

    if request.method == 'GET' and 'appliedAt' in request.GET:
        time = int(request.GET.get('appliedAt'))
        today = date.today()
        months = today - relativedelta(months=time)
        

    for x in jobs:
        dic = {
            "title": x.title,
            "id": x.id,
            "applications": BaseAppliedJobSerializer(AppliedJob.objects.filter(job_id=x.id, is_active=True), many=True,).data,
            "is_active": x.is_active,
            "featured": x.featured,
            "expired_at": x.expired_at,
            "type": x.type,
            "experience": x.experience,
            "positions": x.positions,
            "created_date": x.created_date,
            "start_date": x.start_date,
            "weekly_hours": x.weekly_hours,
            "logo": company.logo.url if company.logo == None  else None,
        }

        jobArr.append(dic)
    return Response({"jobs": jobArr })
    
@api_view(['GET'])
def getMyCompanyCandidates(request):
    user = request.user
    company = Company.objects.filter(user=user).first()

    if company == None:
        return Response({ "error": "Could not find company."}, status=status.HTTP_403_FORBIDDEN)
    
    candidates = AppliedJobSerializer(AppliedJob.objects.filter(company=company), many=True).data

    return Response({"candidates": candidates }, status=status.HTTP_200_OK)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_job(request, pk):
    job = get_object_or_404(Job, id=pk)

    if job.user != request.user:
        return Response({
            'message': 'You can not update this job'
        }, status=status.HTTP_403_FORBIDDEN)

    job.title = request.data['title']
    job.description = request.data['description']
    job.type = request.data['type']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.country = request.data['country']
    job.state =  request.data['state']
    job.city =  request.data['city']
    job.is_commission =  request.data['is_commission']
    job.min_salary = request.data['min_salary']
    job.max_salary = request.data['max_salary']
    job.positions = request.data['positions']
    job.responsibilities = request.data['responsibilities']
    job.skills = request.data['skills']
    job.weekly_hours = request.data['weekly_hours']
    job.save()

    serializer = JobSerializer(job, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_job(request, pk):
    job = Job.objects.get(id=pk)

    if job.user != request.user:
        return Response({
            'message': 'You can not delete this job'
        }, status=status.HTTP_403_FORBIDDEN)
    
    job.delete()

    return Response({ 'message': 'Job is Deleted.' }, status=status.HTTP_200_OK)

    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_candidate_application(request, pk):
    user = request.user
    company = Company.objects.filter(user=user).first()
    candidate = AppliedJob.objects.filter(id=pk).first()

    if company.id != candidate.id:
        Response({"error": "You are not able to access this candidate with this account."}, status=status.HTTP_403_FORBIDDEN)

    if candidate == None:
        Response({"error": "Could not find application."}, status=status.HTTP_404_NOT_FOUND)

    job = Job.objects.filter(id=candidate.job_id).first()
    if job == None:
        Response({"error": "Could not find job."}, status=status.HTTP_404_NOT_FOUND)

    return Response({"candidate": AppliedJobSerializer(candidate).data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def saveCompany(request, pk):
    user = request.user
    company = get_object_or_404(Company, id=pk)
    
    SavedCompanies.objects.create(
        user = user,
        company = company
    )
    return Response({ "message": "Successfully saved company." }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unsaveCompany(request, pk):
    try:
        company = get_object_or_404(Company, id=pk)
        user = request.user
        exists = SavedCompanies.objects.filter(company=company, user=user).first()

        if exists == None:
            return Response({ "error": "Could not find company." }, status=status.HTTP_200_OK)    
        
        exists.delete()
        return Response({ "message": "Successfully unsaved company." }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({ "error": str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# @transaction.atomic
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
# def delete_logo(request):
#     try:
#         user = request.user
#         company = Company.objects.filter(user=user).first()
#         company.logo = None
#         company.save()
#         # logo = Logo.objects.filter(user=user).get()
#         # logo.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_job(request):
    try:
        user = CustomUserModel.objects.get(id=request.user.id)
        company = Company.objects.filter(user_id=request.user.id).get()
        form = request.data
        job = Job.objects.create(
            title = bleach.clean(form['title']),
            description = bleach.clean(form['description'], attributes=bleached_attr, tags=bleached_tags),
            is_commission = form['is_commission'],
            type = form['type'],
            featured = False,
            candidates = [],
            education = bleach.clean(form['education']),
            country = bleach.clean(form['country']),
            address = bleach.clean(form['address']),
            state = bleach.clean(form['state']),
            city = bleach.clean(form['city']),
            industry = bleach.clean(form['industry']),
            experience = bleach.clean(form['experience']),
            min_salary = int(form['min_salary']),
            max_salary = int(form['max_salary']),
            positions = int(form['positions']),
            company = company,
            responsibilities = bleach.clean(form['responsibilities'], attributes=bleached_attr, tags=bleached_tags),
            skills = form['skills'],
            weekly_hours = int(form['weekly_hours']),
            user = user,
            is_active = True,
            lat = company.lat,
            long = company.long,
        )
        serializer = JobSerializer(job, many=False)
        return Response({
            "job": serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
