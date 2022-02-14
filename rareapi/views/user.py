"""View module for handling requests about rare_user"""
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rareapi.models.user import RareUser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status



class RareUserView(ViewSet):
    """Level up rare_user view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single rare_user 
        
        Returns:
            Response -- JSON serialized rare_user 
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
        rare_user_type = request.query_params.get('type', None)
        if rare_user_type is not None:
            rare_users = rare_users.filter(rare_user_type_id=rare_user_type)
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
            serializer.save(rare_user=rare_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            serializer.save()
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
        fields = ('id', '', 'title', 'maker', '', 'number_of_players', 'skill_level')
        depth = 1
        
class CreateRareUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUser
        fields = ['id', 'rare_user_type', 'title', 'maker', 'number_of_players', 'skill_level']