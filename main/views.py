from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.db.models import Q
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .serializers import TicketSerializer, ShowsSerializer, NewsSerializer, UserProfileSerializer, GenreSerializer, ActorSerializer, SessionSerializer, RegisterSerializer, LoginSerializer
from .models import Show, News, Ticket, UserProfile, Session, Genre, Actor
from django.contrib.auth.models import User
from .permissions import Read_only_permission

from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # пропускаем проверк


class ShowShowsViewSet(viewsets.ModelViewSet):
    serializer_class = ShowsSerializer
    queryset = Show.objects.filter(available=True)
    #parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Show.objects.filter(available=True)
        
        genre_id = self.request.query_params.get('genre')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        return queryset.distinct()
    
    
    @action(detail=True, methods=['get'])
    def sessions(self, request, pk=None):
        show = self.get_object()
        sessions = Session.objects.filter(show=show)
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)

class ShowNewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all().order_by('-published_at')
    permission_classes = [Read_only_permission]
    
    def get_queryset(self):
        return News.objects.all().order_by('-published_at')

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.filter(status=True)
    permission_classes=[AllowAny]
    
    def create(self, request):
        """Покупка билета - POST /api/tickets/"""
        print(f"DEBUG: Получены данные: {request.data}") 
        try:
            session_id = request.data.get('session')
            row = request.data.get('row')
            seat = request.data.get('seat')
            price = request.data.get('price')
            user_id = request.data.get('user')

            try:
               session = Session.objects.get(id=session_id)
            except Session.DoesNotExist:
                return Response(
                    {'error': 'Спектакль не найден или недоступен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                user = UserProfile.objects.get(id=user_id)
            except UserProfile.DoesNotExist:
                return Response(
                    {'error': 'Пользователь не найден'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            existing_ticket = Ticket.objects.filter(
                session=session,
                row=row,
                seat=seat,
                status=True
            ).first()
            
            if existing_ticket:
                return Response({
                    'error': f'Место уже занято!',
                    'details': f'Ряд {row}, место {seat}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            ticket_data = {
                'session': session_id,
                'row': row,
                'seat': seat,
                'price': price,
                'status': True,
                'user': user_id,
            }
            
            serializer = self.get_serializer(data=ticket_data)
            serializer.is_valid(raise_exception=True)
            ticket = serializer.save()
            
            return Response({
                'success': True,
                'message': 'Билет успешно куплен!',
                'ticket': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Проверить доступность места: /api/tickets/available/?show=1&row=5&seat=10"""
        session_id = request.query_params.get('session')
        row = request.query_params.get('row')
        seat = request.query_params.get('seat')
        
        if not all([session_id, row, seat]):
            return Response(
                {'error': 'Укажите show, row и seat'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        is_occupied = Ticket.objects.filter(
            session_id=session_id,
            row=row,
            seat=seat,
            status=True
        ).exists()
        
        return Response({
            'available': not is_occupied,
            'session_id': session_id,
            'row': row,
            'seat': seat,
            'is_occupied': is_occupied
        })

class ShowSessionsViewSet(viewsets.ModelViewSet):
    serializer_class = SessionSerializer
    queryset = Session.objects.all()
    
    def get_queryset(self):
        """Фильтрация сеансов"""
        queryset = Session.objects.all()
        
        date = self.request.query_params.get('date')  # ← Исправлено!
        if date:
            queryset = queryset.filter(date=date)
        
        show_id = self.request.query_params.get('show')
        if show_id:
            queryset = queryset.filter(show_id=show_id)
        
        return queryset.order_by('date')
    
    @action(detail=True, methods=['get'])
    def seats(self, request, pk=None):
        """Схема мест: /api/sessions/1/seats/"""
        session = self.get_object()
        occupied_seats = Ticket.objects.filter(session=session, status=True)
        
        seats_matrix = []
        for row in range(1, session.hall_rows + 1):
            row_seats = []
            for seat in range(1, session.hall_seats + 1):
                is_occupied = occupied_seats.filter(row=row, seat=seat).exists()
                row_seats.append({
                    'row': row,
                    'seat': seat,
                    'occupied': is_occupied,
                    'available': not is_occupied
                })
            seats_matrix.append(row_seats)
        
        return Response({
            'session_id': session.id,
            'show_title': session.show.title,
            'date': session.date,
            'hall': session.hall.name,
            'rows': session.hall_rows,
            'seats_per_row': session.hall_seats,
            'seats_matrix': seats_matrix
        })

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    @action(url_path="my", methods=["GET"], detail=False )
    def get_my(self, request, *args, **kwargs):
        return Response({
            'username':request.user.username,
            'is_authenticated':request.user.is_authenticated,
            'is_staff':request.user.is_staff
        })
    @action(url_path="login", methods=["POST"], detail=False)
    def login(self, request, *args, **kwargs):  # ← ДОБАВЬТЕ request параметр
        serializer = LoginSerializer(data=request.data)  # ← используйте request.data
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

    # ФИКС: authenticate требует request и именованные аргументы
        user = authenticate(request, username=username, password=password)
    
        if user:
            login(request, user)
        
        # Получаем профиль пользователя если есть
            try:
                profile = UserProfile.objects.get(user=user)
                profile_id = profile.id
                role = profile.role
            except UserProfile.DoesNotExist:
                profile_id = None
                role = 'user'
        
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'profile_id': profile_id,
                    'role': role
                }
            })
        else:
            return Response({
            "success": False,
            "message": "Неверные учетные данные"
        }, status=status.HTTP_401_UNAUTHORIZED)  # ← используйте status из rest_framework
    


    

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    permission_classes = [AllowAny]
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        email = serializer.validated_data.get('email', '')
        
        if User.objects.filter(username=username).exists():
            return Response({
                'success': False,
                'message': 'Пользователь с таким именем уже существует'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Создаем пользователя
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
            profile = UserProfile.objects.create(
                user=user,
                full_name=serializer.validated_data['full_name'],
                birth_date=serializer.validated_data['birth_date'],
                passport_series=serializer.validated_data['passport_series'],
                passport_number=serializer.validated_data['passport_number'],
                role='user'  
            )
            
            login(request, user)
            
            return Response({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': 'user'
                },
                'message': 'Регистрация успешна'
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Ошибка регистрации: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [Read_only_permission]