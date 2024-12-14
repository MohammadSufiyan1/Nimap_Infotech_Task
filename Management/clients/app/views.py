from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def retrieve(self, request, pk=None):
        client = self.get_object()
        projects = client.projects.all()
        serializer = self.get_serializer(client)
        project_data = ProjectSerializer(projects, many=True).data
        response_data = {**serializer.data, 'projects': project_data}
        return Response(response_data)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def create(self, request, client_id=None):
        client = Client.objects.get(id=client_id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(client=client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_204_NO_CONTENT)
    