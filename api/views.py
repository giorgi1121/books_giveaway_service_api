from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, viewsets, serializers
from .models import Author, Genre, Condition, Image, Book, BookInterest
from django.contrib.auth.models import User
from .serializers import AuthorSerializer, GenreSerializer, ConditionSerializer, ImageSerializer, BookSerializer, UserSerializer, BookInterestSerializer, BookExpressInterestSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .filters import BookFilter
from rest_framework.response import Response
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.db.models import CharField


class AuthorList(generics.ListCreateAPIView):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  permission_classes = [IsAuthenticated]


class GenreList(generics.ListCreateAPIView):
  queryset = Genre.objects.all()
  serializer_class = GenreSerializer
  permission_classes = [IsAuthenticated]


class ConditionList(generics.ListCreateAPIView):
  queryset = Condition.objects.all()
  serializer_class = ConditionSerializer
  permission_classes = [IsAuthenticated]


class ImageUploadView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    
    
class BookList(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Book.objects.all()
    filterset_class = BookFilter
    
    def perform_create(self, serializer):
        # Set the owner of the book to the currently authenticated user
        serializer.save(owner=self.request.user)
    

class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the book instance
        book = super().get_object()

        # Check if the current user is the owner of the book
        if self.request.user != book.owner:
            raise PermissionDenied('You do not have permission to access this book.')

        return book
    


# views for expressing interest


class ExpressInterestView(generics.ListCreateAPIView):
    serializer_class = BookExpressInterestSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookInterest.objects.all()

    def create(self, request, *args, **kwargs):
        # Get the book ID from the request data
        book_id = request.data.get('book')

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'message': f'Book with ID {book_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the book is available for expressing interest
        if book.status == 'borrowed':
            return Response({'message': 'This book is not available for expressing interest.'}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically set the interested_user to the currently authenticated user
        serializer = self.get_serializer(data={'book': book_id})
        serializer.is_valid(raise_exception=True)

        interest_exists = BookInterest.objects.filter(
            interested_user=self.request.user, book_id=book_id
        ).exists()

        if interest_exists:
            return Response({'message': 'User is already interested in this book.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(interested_user=self.request.user)

        # Update the book status to "Requested"
        book.status = 'requested'
        book.save()

        return Response({'message': 'Expressed interest in the book successfully.'}, status=status.HTTP_201_CREATED)



class BookInterestsView(generics.ListAPIView):
    serializer_class = BookInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        book_id = self.kwargs['pk']
        return BookInterest.objects.filter(book_id=book_id)
    

class AllBooksInterestsView(generics.ListAPIView):
    serializer_class = BookInterestSerializer
    permission_classes = [IsAuthenticated]
    queryset = BookInterest.objects.all()
    

class ChooseInterestedUserView(generics.ListCreateAPIView):
    serializer_class = BookInterestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the current user
        user = self.request.user

        # Annotate the BookInterest queryset with related Book data
        queryset = BookInterest.objects.annotate(
            book_title=Concat(
                F("book__title"), Value(" - "), F("book__author__name"), output_field=CharField()
            )
        )

        # Filter the queryset to include only BookInterests related to books where the user is the owner
        queryset = queryset.filter(book__owner=user)

        return queryset

    def perform_create(self, serializer):
        # Get the current user
        user = self.request.user

        # Get the book ID from the POST data
        book_id = self.request.data.get("book")

        # Get the interested user ID from the POST data
        interested_user_id = self.request.data.get("interested_user")

        # Check if the user is interested in the specified book
        is_interested = BookInterest.objects.filter(
            interested_user=interested_user_id, book_id=book_id
        ).exists()

        if not is_interested:
            # If the user is not already interested, raise a validation error
            raise serializers.ValidationError({'message': 'User is not interested in this book.'})

        # Check if the specified book belongs to the current user
        is_owner = Book.objects.filter(owner=user, id=book_id).exists()

        if not is_owner:
            # If the user does not own the book, raise a validation error
            raise serializers.ValidationError({'message': 'You do not own this book.'})

        # Update the book's status to "Borrowed" and set the borrowed_to field
        book = Book.objects.get(id=book_id)
        book.status = 'unavailable'
        book.owner_id = interested_user_id
        book.previous_owner_id = user
        book.save()

        # Create a new BookInterest record
        serializer.save(interested_user_id=interested_user_id, book_id=book_id)

        return Response({'message': 'Book has been borrowed by the selected user'}, status=status.HTTP_201_CREATED)



# Current User


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return the current user.
        return User.objects.filter(pk=self.request.user.pk)



# REGISTRATION/AUTHORIZATION


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Book
from .serializers import BookSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']  # Get email from serializer
        password = serializer.validated_data['password']

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)

        token, created = Token.objects.get_or_create(user=user)
        #'token': token.key,

        return Response({'token': token.key,'message': 'Registration successful'}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.authtoken.models import Token

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        #'token': token.key,
        return Response({'token': token.key,'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logged out'}, status=status.HTTP_200_OK)
