"""View module for handling requests about game"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import RareUser


class RareUserView(ViewSet):
    """Level up game view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game 
        
        Returns:
            Response -- JSON serialized game 
        """
        try:
            rare_user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(rare_user)
            return Response(serializer.data)
        except RareUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND) 

    def list(self, request):
        """Handle GET requests to get all rare_user 

        Returns:
            Response -- JSON serialized list of rare_user
        """
        rare_users = RareUser.objects.all()
        rare_users = RareUser.objects.order_by('user__username')
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rare_user instance
        """
        try:
            serializer = CreateRareUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            rare_user = serializer.save()
            return Response(rare_user.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Handle PUT requests for a rare_user

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            rare_user = RareUser.objects.get(pk=pk)
            serializer = CreateRareUserSerializer(rare_user, data=request.data)
            serializer.is_valid(raise_exception=True)
            rare_user = serializer.save()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except ValidationError as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, pk):
        rare_user = RareUser.objects.get(pk=pk)
        rare_user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    
class RareUserSerializer(serializers.ModelSerializer):
    """JSON serializer for rare_user
    """
    class Meta:
        model = RareUser
        fields = ('id', 'user', 'bio', 'profile_image_url', 'created_on', 'active')
        depth = 1
        
class CreateRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ['id', 'bio', 'profile_image_url', 'created_on', 'active']