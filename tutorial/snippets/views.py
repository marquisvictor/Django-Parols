from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import snippet
from snippets.serializers import SnippetSerializer
from django.http import HttpResponse, JsonResponse
# Create your views here.

@csrf_exempt
def snippet_list(request):
    """list all the snippets or create a new one"""

    if request.method == 'GET':
        snippets = snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """endpoint to view, update or delete a code snippet"""

    try:
        Snippet = snippet.objects.get(pk=pk)
    except snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(Snippet)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(Snippet, data=data)
        if serializer.is_valid():
            return JsonResponse(serializer.data)  # come back here to see what happens with a staus http there like above. 
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Snippet.delete()
        return HttpResponse(status=204)

