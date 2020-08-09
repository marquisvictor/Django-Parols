from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from snippets.models import snippet
from snippets.serializers import SnippetSerializer

# Create your views here.

class SnippetList(APIView):
    """
        still same functionality but in a class setting

        list all snippets or create a new one
    """

    def get(self, request, format=None):
        snippets = snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    
    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            seriailizer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
class SnippetDetail(APIView):

    def get_object(self, pk):
        try:
            return snippet.objects.get(pk=pk)
        except snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk, format=None):
        Snippet = self.get_object(pk)
        serializer = SnippetSerializer(Snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Snippet = self.get_object(pk)
        serializer = SnippetSerializer(Snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Snippet = self.get_object(pk)
        Snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
