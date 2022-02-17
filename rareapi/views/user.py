"""View module for handling requests about game"""
import base64
import uuid
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
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
        rare_users = RareUser.objects.order_by('-user__username')
        serializer = RareUserSerializer(rare_users, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized rare_user instance
        """
        rare_user = RareUser.objects.get(user=request.auth.user)
        try:
            serializer = CreateRareUserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Create a new instance of the game picture model you defined
            # Example: game_picture = GamePicture()
            rare_user = RareUser.objects.all()
            format, imgstr = request.data["profile_image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["id"]}-{uuid.uuid4()}.{ext}')
            rare_user.profile_image_url = data
            # Give the image property of your game picture instance a value
            # For example, if you named your property `action_pic`, then
            # you would specify the following code:
            #
            #       game_picture.action_pic = data

            # Save the data to the database with the save() method
            
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