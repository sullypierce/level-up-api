"""View module for handling requests about events"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, Event, Gamer, Rsvp
from levelupapi.views.game import GameSerializer
from django.db.models import Count


class Events(ViewSet):
    """Level up events"""
    

    def create(self, request):
        """Handle POST operations for events

        Returns:
            Response -- JSON serialized event instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)

        event = Event()
        event.time = request.data["time"]
        event.date = request.data["date"]
        event.description = request.data["description"]
        event.organizer = gamer

        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized game instance
        """
        events = Event.objects.annotate(registration_count=Count('registrations'))
        event = None
        for ev in events:
            if int(ev.id) == int(pk):
                event = ev
        print(event)
        if event == None:
            return Response({'message': 'No matching id'}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        #try:
        #    event = Event.objects.get(pk=pk)
        #    serializer = EventSerializer(event, context={'request': request})
        #    return Response(serializer.data)
        #except Exception:
        #    return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        organizer = Gamer.objects.get(user=request.auth.user)

        event = Event.objects.get(pk=pk)
        event.description = request.data["description"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.organizer = organizer

        game = Game.objects.get(pk=request.data["gameId"])
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource

        Returns:
            Response -- JSON serialized list of events
        """
        # Get the current authenticated user
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.annotate(registration_count=Count('registrations'))

        # Set the `joined` property on every event
        for event in events:
            event.joined = None

            try:
                Rsvp.objects.get(event=event, gamer=gamer)
                event.joined = True
            except Rsvp.DoesNotExist:
                event.joined = False

        # Support filtering events by game
        game = self.request.query_params.get('gameId', None)
        if game is not None:
            events = events.filter(game__id=type)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing gamers signing up for events"""

        # A gamer wants to sign up for an event
        if request.method == "POST":
            # The pk would be `2` if the URL above was requested
            event = Event.objects.get(pk=pk)

            # Django uses the `Authorization` header to determine
            # which user is making the request to sign up
            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                # Determine if the user is already signed up
                registration = Rsvp.objects.get(
                    event=event, gamer=gamer)
                return Response(
                    {'message': 'Gamer already signed up this event.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except Rsvp.DoesNotExist:
                # The user is not signed up.
                registration = Rsvp()
                registration.event = event
                registration.gamer = gamer
                registration.save()

                return Response({}, status=status.HTTP_201_CREATED)
            
    

        # User wants to leave a previously joined event
        elif request.method == "DELETE":
            # Handle the case if the client specifies a game
            # that doesn't exist
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get the authenticated user
            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                # Try to delete the signup
                registration = Rsvp.objects.get(
                    event=event, gamer=gamer)
                registration.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except Rsvp.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for event.'},
                    status=status.HTTP_404_NOT_FOUND
                )

        # If the client performs a request with a method of
        # anything other than POST or DELETE, tell client that
        # the method is not supported
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
    


class EventUserSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EventGamerSerializer(serializers.ModelSerializer):
    """JSON serializer for event organizer"""
    user = EventUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    class Meta:
        model = Game
        fields = ('id', 'name', 'maker', 'number_of_players', 'skill_level')
        
class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    organizer = EventGamerSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'organizer',
                  'description', 'date', 'time', 'joined', 'registration_count')
        
