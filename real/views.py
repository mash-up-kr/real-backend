from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from knox.auth import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from real.permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import DreamSerializer, ResultSerializer
from .models import Dream
from rest_framework import permissions, status


class DreamListCreateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        dreams = Dream.objects.filter(user=request.user).filter(result=None)
        serializer = DreamSerializer(dreams, many=True)
        return Response({"dreams": serializer.data})

    def post(self, request):
        serializer = DreamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class DreamHistoryListAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        dreams = Dream.objects.filter(user=request.user).exclude(result=None)
        serializer = DreamSerializer(dreams, many=True)
        return Response({"dreams": serializer.data})


class DreamRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,
                         IsOwner, )
    authentication_classes = (TokenAuthentication,)

    def get_object(self, pk):
        return get_object_or_404(Dream, pk=pk)

    def get(self, request, pk):
        dream = self.get_object(pk)
        self.check_object_permissions(request, dream)
        dream_serializer = DreamSerializer(dream)
        if dream_serializer.data['is_completed']:
            result_serializer = ResultSerializer(dream.result)
            return_data = dict()
            for k, v in chain(dream_serializer.data.items(), result_serializer.data.items()):
                return_data[k] = v

            return Response(return_data)

        return Response(dream_serializer.data)

    def patch(self, request, pk):
        dream = self.get_object(pk)
        self.check_object_permissions(request, dream)
        serializer = DreamSerializer(dream, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        dream = self.get_object(pk)
        self.check_object_permissions(request, dream)
        dream.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ResultCreateUpdateAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,
                         IsOwner, )
    authentication_classes = (TokenAuthentication,)

    def get_dream(self, pk):
        return get_object_or_404(Dream, pk=pk)

    def post(self, request, pk):
        dream = self.get_dream(pk)
        self.check_object_permissions(request, dream)

        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dream=dream)
            dream_serializer = DreamSerializer(dream)

            return_data = dict()
            for k, v in chain(dream_serializer.data.items(), serializer.data.items()):
                return_data[k] = v

            return Response(return_data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        dream = self.get_dream(pk)
        self.check_object_permissions(request, dream)

        try:
            result = dream.result
            serializer = ResultSerializer(result, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()

                dream_serializer = DreamSerializer(dream)

                return_data = dict()
                for k, v in chain(dream_serializer.data.items(), serializer.data.items()):
                    return_data[k] = v

                return Response(return_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            raise NotFound('Result Not Found')