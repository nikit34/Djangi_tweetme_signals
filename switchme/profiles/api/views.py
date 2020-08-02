from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Profile
from ..serializers import PublicProfileSerializer

User = get_user_model()


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def user_profile_detail_view(request, username, *args, **kwargs):
#     current_user = request.user
#     to_follow_user = ??
#     return Response({}, status=200)


@api_view(['GET'])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({'detail': 'User not found'}, status=404)
    profile_obj = qs.first()
    data = PublicProfileSerializer(instance=profile_obj, context={'request': request})
    return Response(data.data, status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username=username)
    if me.username == username:
        my_followers_qs = me.profile.followers.all()
        return Response({'count': my_followers_qs.count()}, status=200)
    if not other_user_qs.exists():
        return Response({}, status=404)
    other = other_user_qs.first()
    profile = other.profile
    data = request.data or {}
    action = data.get('action')
    if action == 'follow':
        profile.followers.add(me)
    elif action == 'unfollow':
        profile.followers.remove(me)
    else:
        pass
    data = PublicProfileSerializer(instance=profile, context={'request': request})
    return Response(data.data, status=200)
