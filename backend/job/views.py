from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Job
from .serializers import JobSerializer
from rest_framework import status
from django.db.models import Sum, Avg, Max, Min, Count
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .filters import JobFilter
# Create your views here.
@api_view(['GET'])
def getAllJobs(request):
    filterset = JobFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    count = filterset.qs.count()
    resPerPage = 4
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request)

    
    print("Filtered queryset:", filterset.qs)
    searlizer = JobSerializer(filterset.qs, many=True)
    return Response({  
                     'count': count,
                     'resPerPage':resPerPage,
                     'jobs':searlizer.data})


 
@api_view(['GET'])
def getJob(request, id):
    job = get_object_or_404(Job, id=id)
    searlizer = JobSerializer(job, many=False)
    return Response(searlizer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createJob(request):
    data = request.data
    job = Job.objects.create(**data)
    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateJob(request, id):
    job = get_object_or_404(Job, id=id)
    if job.user != request.user:
        return Response({'message': 'You are not authorized to update this job!'}, status=status.HTTP_403_FORBIDDEN)    
    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience_level = request.data['experience_level']
    job.job_type = request.data['job_type']
    job.salary = request.data['salary']
    job.position = request.data['position']
    job.company = request.data['company']
    job.points = request.data['points']
    
    job.save()

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteJob(request, id):
    
    job = get_object_or_404(Job, id=id)
    if job.user != request.user:
        return Response({'message': 'You are not authorized to delete this job!'}, status=status.HTTP_403_FORBIDDEN)
    job.delete()

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getTopics(request, topics):

    args = {'title__icontains': topics }
    jobs = Job.objects.filter(**args)
    
    if len(jobs) == 0:
        return Response({'message': 'No Jobs Found!'},status=404)
    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        average_salary = Avg('salary'),
        average_position = Avg('position'),
        min_salary = Min('salary'),
        max_salary = Max('salary'),

    )
    return Response(stats)