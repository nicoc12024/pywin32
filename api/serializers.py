from rest_framework import serializers
from .models import Blog, User, Like, Comment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'username', 'profilePicture', 'profession', 'bio', 'location']

class BlogSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    profession = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    profilePicture = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    likes_user_ids = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            'id', 'body', 'username', 'user_id', 'created_at', 'profession', 'location', 'profilePicture',
            'likes_user_ids', 'likes_count']

    def get_username(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.user_id

    def get_created_at(self, obj):
        # Format the date as a string (e.g., "2023-04-14")
        return obj.created_at.strftime("%d-%m-%Y")

    def get_profession(self, obj):
        return obj.user.profession

    def get_location(self, obj):
        return obj.user.location

    def get_profilePicture(self, obj):
        return obj.user.profilePicture

    def get_likes_count(self, obj):
        return Like.objects.filter(blog=obj).count()

    def get_likes_user_ids(self, obj):
        return [like.user.user_id for like in obj.like_set.all()]
    
class CommentSerializer(serializers.ModelSerializer):
    profilePicture = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'blog', 'content', 'created_at', 'profilePicture', 'username']

    def get_profilePicture(self, obj):
        return obj.user.profilePicture    
    
    def get_username(self, obj):
        return obj.user.username



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
