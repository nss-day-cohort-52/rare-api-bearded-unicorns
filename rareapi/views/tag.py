from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Tag
from django.core.exceptions import ValidationError
from rest_framework.decorators import action

class TagView(ViewSet):
    def retrieve(self, request, pk):
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data)
        except Tag.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        tag = Tag.objects.all()
        serializer = TagSerializer(tag, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        tag = Tag.objects.create(
            label=request.data["label"]
        )    
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, pk):
        tag = Tag.objects.get(pk=pk)
        tag.label = request.data["label"]
        tag.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class TagSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Tag
        fields = ('id', 'label')
        
class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model: Tag
        fields = ['id', 'label']