from django.utils import timezone
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Min, Max, Count
from rest_framework.pagination import PageNumberPagination
from company.serializers import BaseCompanySerializer
from .serializers import BaseJobSerializer, JobSerializer
from .models import Job
from candidate.models import AppliedJob
from candidate.models import SavedJob
from candidate.serializers import AppliedJobSerializer
from django.shortcuts import get_object_or_404
from playfairauth.models import CustomUserModel
from .filters import JobsFilter
from company.models import Company
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from datetime import date

@api_view(['GET'])
def jobs(request):
    order = "-created_date"
    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by(order))
    count = filterset.qs.count()
    resPerPage = 50
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = BaseJobSerializer(queryset, many=True,  context={'request': request})
    

    return Response({
        "count": count,
        "resPerPage": resPerPage,
        'jobs': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def homeJobs(request):
    featured = Job.objects.filter(featured=True)
    featured = BaseJobSerializer(featured, many=True, context={'request': request})
    recent = Job.objects.filter(featured=False)
    recent = BaseJobSerializer(recent, many=True, context={'request': request})
    companies = BaseCompanySerializer(Company.objects.all(), many=True)
    is_complete = None
    if CustomUserModel.objects.filter(id=request.user.id).exists():
         is_complete = CustomUserModel.objects.filter(id=request.user.id).first().is_complete

    if request.user:
         print('RAN')
    return Response({
        "featured": featured.data,
        "recent": recent.data,
        "companies": companies.data,
        'is_complete': is_complete
    }, status=status.HTTP_200_OK)


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
            "relatedJobs": relatedJobs.data,
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