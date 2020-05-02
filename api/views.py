from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import PictureSerializer
from .serializers import AlbumSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny

from django.views.decorators.csrf import csrf_exempt

import json
from django.core.exceptions import ObjectDoesNotExist

from .models import Album
from .models import Picture
from django.contrib.auth.models import User
from .serializers import UserSerializer


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_album(request):
    payload = json.dumps(request.data)
    payload = json.loads(payload)
    user = request.user
    try:
        album = Album.objects.create(
            album_name=payload["album_name"],
            album_description=payload["album_description"],
            creator=user,

        )
        serializer = AlbumSerializer(album)
        return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileUploadView(APIView):
    parser_class = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        albums = Album.objects.get(album_name=request.data['album_name'])
        file_serializer = PictureSerializer(data=request.data)

        if file_serializer.is_valid():
            file_serializer.save(albums=albums)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def welcome(request):
    content = {"message": "Welcome to the Solito"}
    return JsonResponse(content)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_pictures(request):
    user = request.user.id
    pictures = Picture.objects.filter(albums__creator=user)
    serializer = PictureSerializer(pictures, many=True)
    return JsonResponse({'pictures': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_albums(request):
    user = request.user.id
    album = Album.objects.filter(creator=user)
    serializer = AlbumSerializer(album, many=True)
    return JsonResponse({'album': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def get_public_albums(request):

    album = Album.objects.filter(is_private=False)
    serializer = AlbumSerializer(album, many=True)
    return JsonResponse({'album': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([AllowAny])
def get_public_album(request, pk):

    album = Album.objects.filter(is_private=False, id=pk)
    serializer = AlbumSerializer(album, many=True)
    return JsonResponse({'album': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_auth(request):
    payload = json.dumps(request.data)
    payload = json.loads(payload)

    user = User.objects.create_user(
        email=payload["email"], username=payload["username"], password=payload["password"])
    serializer = UserSerializer(user)
    return JsonResponse({'user': serializer.data}, safe=False, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def album_detail(request, pk):

    try:
        album = Album.objects.get(pk=pk)
    except Album.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AlbumSerializer(album)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AlbumSerializer(album, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        album.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# Create your views here.

