from contract.serializers import *
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max, Count
from rest_framework.pagination import PageNumberPagination
from company.serializers import BaseCompanySerializer
from .serializers import BaseJobSerializer, JobSerializer
from contract.models import Contract
from .models import Job
from candidate.models import AppliedJob
from candidate.models import SavedJob
from candidate.serializers import AppliedJobSerializer
from django.shortcuts import get_object_or_404
from playfairauth.models import CustomUserModel
from .filters import JobsFilter
from company.models import Company
from rest_framework.permissions import IsAuthenticated
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.conf import settings
CACHE_TTL = getattr(settings ,'CACHE_TTL' , DEFAULT_TIMEOUT)

@api_view(['GET'])
def index(request):
    order =  '-created_date' if request.GET.get('orderBy') == 'asc' else 'created_date'
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by(order))
    total = filterset.qs.count()
    per_page = 50
    paginator = PageNumberPagination()
    paginator.page_size = per_page
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = BaseJobSerializer(queryset, many=True,  context={'request': request})
 
    return Response({
        "total": total,
        "per_page": per_page,
        'jobs': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def homeJobs(request):
    try:
        order = "-created_date"
        filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by(order))
        count = filterset.qs.count()
        resPerPage = 50
        paginator = PageNumberPagination()
        paginator.page_size = resPerPage
        queryset = paginator.paginate_queryset(filterset.qs, request)
        jobs = BaseJobSerializer(queryset, many=True,  context={'request': request}).data
        featured = BaseJobSerializer(Job.objects.filter(featured=True), many=True, context={'request': request}).data
        recent = BaseJobSerializer(Job.objects.filter(featured=False), many=True, context={'request': request}).data
        companies = BaseCompanySerializer(Company.objects.all(), many=True).data 
        contracts = BaseContractSerializer(Contract.objects.all(), many=True).data

        is_complete = None
        if CustomUserModel.objects.filter(id=request.user.id).exists():
            is_complete = CustomUserModel.objects.filter(id=request.user.id).first().is_complete
        return Response({
            "count": count,
            "resPerPage": resPerPage,
            'jobs': jobs,
            'contracts': contracts,
            'recent': recent,
            'featured': featured,
            'companies':companies,
            'is_complete': is_complete,
        }, status=status.HTTP_200_OK)
        # if cache.get('home_featured'):
        #     featured = cache.get('home_featured')
        # else:
        #     featured = BaseJobSerializer(Job.objects.filter(featured=True), many=True, context={'request': request}).data
        #     cache.set('home_featured', featured)
        # if cache.get('home_recent'):
        #     recent = cache.get('home_recent')
        # else:
        #     recent = BaseJobSerializer(Job.objects.filter(featured=False), many=True, context={'request': request}).data
        #     cache.set('home_recent', recent)
        # if cache.get('home_companies'):
        #     companies = cache.get('home_companies')
        # else:
        #     companies = BaseCompanySerializer(Company.objects.all(), many=True).data 
        #     cache.set('home_companies', companies)

        # is_complete = None
        # if CustomUserModel.objects.filter(id=request.user.id).exists():
        #     is_complete = CustomUserModel.objects.filter(id=request.user.id).first().is_complete
        # return Response({
        #     "featured": featured,
        #     "recent": recent,
        #     "companies": companies,
        #     'is_complete': is_complete
        # }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)         


@api_view(['GET'])
def get_job(request, pk):
    try:
        user = request.user
        job = get_object_or_404(Job, id=pk)
        candidates = job.appliedjob_set.all().count()
        serializer = JobSerializer(job, many=False, context={'request': request})
        relatedJobs = JobSerializer(Job.objects.filter(industry=serializer.data['industry']).exclude(id=pk), many=True)

        return Response({
            "job": serializer.data,
            "related_jobs": relatedJobs.data,
            "candidates": candidates,
        }, status=status.HTTP_200_OK)
    
    except Job.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def pauseJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    
    if job.user != request.user:
        return Response({
            'message': 'You do not have access to pause this job.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    job.is_active = False
    job.save()

    return Response({ 'message': 'Job is paused.' }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def startJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    
    if job.user != request.user:
        return Response({
            'message': 'You do not have access to start this job.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    job.is_active = True
    job.save()

    return Response({ 'message': 'Job has started.' }, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTopicStats(request, topic):

    args = { 'title__icontains': topic }
    jobs = Job.objects.filter(**args)

    if len(jobs) == 0:
        return Response({ 'message': 'Not stats found for {topic}'.format(topic=topic) })

    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_positions = Avg('positions'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary')
    )

    return Response(stats)


@api_view(['GET'])
def getCurrentUserAppliedJobs(request):
    args = { 'user_id': request.user.id }
    jobs = AppliedJob.objects.filter(**args)

    serializer = AppliedJobSerializer(jobs, many=True)

    return Response(serializer.data)

# @permission_classes([IsAuthenticated])
@api_view(['GET'])
def getCurrentUserJobs(request):

    args = { 'user': request.user.id }
    filterset = JobsFilter(request.GET, queryset=Job.objects.filter(**args).order_by('id'))

    count = filterset.qs.count()
    resPerPage = 50

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = JobSerializer(queryset, many=True)

    return Response({
        "jobs": serializer.data,
        "resPerPage": 50,
        "count": 10
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCandidatesApplied(request, pk):

    user = request.user
    job = get_object_or_404(Job, id=pk)

    if job.user != user:
        return Response({ 'error': 'You can not access this job' }, status=status.HTTP_403_FORBIDDEN)

    candidates = job.candidatesapplied_set.all()

    serializer = AppliedJobSerializer(candidates, many=True)

    return Response(serializer.data)

# Company perm 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approveCandidate(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    company = Company.objects.get(user=user)
    candidateApplication = AppliedJob.objects.filter(id=request.data['candidateId']).first()

    if job.company != company:
            return Response({"error": "You are not the poster of this job. You can not delete job."})
    
    if candidateApplication == None:
            return Response({"error": "Could not find application."})        
    
    candidateApplication.is_approved = request.data['approved']
    candidateApplication.save()


    return Response({"message": "Successfully updated application", "approved": request.data['approved']}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteCandidateApplication(request, pk, ck):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    company = Company.objects.get(user=user)
    candidateApplication = AppliedJob.objects.filter(id=ck).first()

    if job.company != company:
            return Response({"error": "You are not the poster of this job. You can not delete job."})
    
    if candidateApplication == None:
            return Response({"error": "Could not find application."})

    candidateApplication.delete()     
    return Response({"message": "Successfully deleted"}, status=status.HTTP_200_OK)