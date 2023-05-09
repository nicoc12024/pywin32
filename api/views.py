from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from .models import Blog
from .models import Like
from .models import Comment
from .serializers import BlogSerializer
from .serializers import UserSerializer
from .serializers import LikeSerializer
from .serializers import CommentSerializer
from rest_framework import status
from django.db.models import Prefetch   
from rest_framework.pagination import PageNumberPagination


@api_view(['GET'])
def get_blogs(request):
    paginator = PageNumberPagination()
    paginator.page_size = 3  
    blogs = Blog.objects.all().order_by('-created_at')
    page = paginator.paginate_queryset(blogs, request)
    serializer = BlogSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def get_user_blog_likes(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
        blogs = Blog.objects.filter(user=user)
        data = []
        for blog in blogs:
            likes_count = Like.objects.filter(blog=blog).count()
            comments_count = Comment.objects.filter(blog=blog).count()
            data.append({'blog_id': blog.id, 'likes_count': likes_count, 'comments_count': comments_count})
        return Response(data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': f'User with id {user_id} does not exist'})

@api_view(['GET'])
def get_blog_comments(request, blog_id):
    try:
        comments = Comment.objects.filter(blog__id=blog_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    except Comment.DoesNotExist:
        return Response(status=404, data={'error': f'Comments for blog with id {blog_id} do not exist'})
    
@api_view(['POST'])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_comment(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
        user_id = request.query_params.get('user_id', None)

        if user_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Missing user_id parameter'})

        if str(comment.user.user_id) != user_id:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error': 'You are not authorized to delete this comment'})

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get user liked posts object
@api_view(['GET'])
def get_user_liked_posts(request):
    user_id = request.query_params.get('user', None)

    if user_id is None:
        return Response(status=400, data={'error': 'Missing user parameter'})

    try:
        user = User.objects.prefetch_related(Prefetch('likes', queryset=Like.objects.select_related('blog'))).get(user_id=user_id)
        liked_blogs = [like.blog for like in user.likes.all()]
        serializer = BlogSerializer(liked_blogs, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=404, data={'error': f'User with user_id {user_id} does not exist'})

# user like a post object
@api_view(['POST'])
def create_like(request):
    serializer = LikeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete users like post from liked object
@api_view(['DELETE'])
def delete_like(request, pk):
    try:
        like = Like.objects.get(id=pk)
        print(f"Deleting like {pk} for user {like.user.user_id} and blog {like.blog.id}")
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Like.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
# get like object
@api_view(['GET'])
def get_like(request):
    user_id = request.query_params.get('user', None)
    blog_id = request.query_params.get('blog', None)

    if user_id is None or blog_id is None:
        return Response(status=400, data={'error': 'Missing user or blog parameter'})

    try:
        like = Like.objects.get(user__user_id=user_id, blog__id=blog_id)
        serializer = LikeSerializer(like, many=False)
        return Response(serializer.data)
    except Like.DoesNotExist:
        return Response(status=404, data={'error': f'Like object with user {user_id} and blog {blog_id} does not exist'})


@api_view(['GET'])
def get_user(request):
    user_id = request.query_params.get('user_id', None)
    if user_id is None:
        return Response(status=400, data={'error': 'Missing user_id parameter'})

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=404, data={'error': f'User with id {user_id} does not exist'})

    serializer = UserSerializer(user, many=False)
    data = serializer.data
    return Response(data)

@api_view(['PUT', 'PATCH'])
def update_user(request):
    data = request.data
    print("Data received in the backend:", data)

    user_id = data.get('user_id', None)
    email = data.get('email', None)
    username = data.get('username', None)
   

    if user_id is None or email is None or username is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Missing required parameters'})

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist as error:
        print(str(error)) 
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': f'User with user_id {user_id} does not exist'})

    user.email = email
    user.username = username
    user.profilePicture = data.get('profilePicture', user.profilePicture)
    user.profession = data.get('profession', user.profession)
    user.bio = data.get('bio', user.bio)
    user.location = data.get('location', user.location)
    user.save()

    serializer = UserSerializer(user, many=False)
    print(data)

    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    data = request.data
    user_id = data.get('user_id', None)
    email = data.get('email', None)
    username = data.get('username', None)
    location = data.get('location', None)
    profession = data.get('profession', None)
    bio = data.get('bio', None)
    profilePicture = data.get('profilePicture', None)

    if user_id is None or email is None or username is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Missing required parameters'})

    user, created = User.objects.get_or_create(
        user_id=user_id,
        defaults={
            'email': email,
            'username': username,
            'profilePicture': data.get('profilePicture', None),
            'profession': data.get('profession', None),
            'bio': data.get('bio', None),
            'location': data.get('location', None)
        }
    )
    if not created:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'User already exists'})

    serializer = UserSerializer(user, many=False)
    print(data)

    return Response(serializer.data)


@api_view(['GET'])
def get_user_posts(request, user_id):
    if user_id is None:
        return Response(status=400, data={'error': 'Missing user_id parameter'})

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=404, data={'error': f'User with id {user_id} does not exist'})

    try:
        user_posts = Blog.objects.filter(user_id=user_id)
        serializer = BlogSerializer(user_posts, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response(status=500, data={'error': f'Error occurred while fetching posts: {str(e)}'})


@api_view(['POST'])
def create_blog(request):
    data = request.data
    user_id = data.get('user_id', None)
    body = data.get('body', None)

    if user_id is None or body is None:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Missing required parameters'})

    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': f'User with user_id {user_id} does not exist'})

    blog = Blog.objects.create(body=body, user=user)
    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def update_blog(request, pk):
    data = request.data

    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': f'Blog with id {pk} does not exist'})

    serializer = BlogSerializer(instance=blog, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_blog(request, pk):
    try:
        blog = Blog.objects.get(id=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND, data={'error': f'Blog with id {pk} does not exist'})

    blog.delete()
    return Response('Blog deleted successfully')