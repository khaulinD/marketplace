from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from .filters.resume_filter import ResumeFilter
from .models import Resume
from .serializers.resume_serializers import ResumeSerializer


class ResumeViewSet(viewsets.ViewSet):
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResumeFilter

    def perform_create(self, serializer):
        serializer.save(creatorID=self.request.user)  # Assuming request.user is the creator

    def list(self, request):
        resumes = self.queryset.prefetch_related('extra_info')  # Corrected related name
        queryset = self.filterset_class(request.GET, resumes).qs
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        resumes = self.queryset.prefetch_related('extra_info')
        resume = get_object_or_404(resumes, pk=pk)
        serializer = self.serializer_class(resume)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        resume = get_object_or_404(self.queryset, id=pk)
        serializer = self.serializer_class(resume, data=request.data, partial=True)
        if serializer.is_valid():
            # Check if extra_info exists in the request data
            # extra_info_data = request.data.get('extra_info')
            serializer.save()  # Save the Resume object
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, pk=None):
        comment = get_object_or_404(self.queryset, pk=pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

