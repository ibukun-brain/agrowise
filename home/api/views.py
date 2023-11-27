import json

import requests
from drf_spectacular.utils import extend_schema
from openai import OpenAI
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from agrowise.utils.env_variable import get_env_variable
from home.api.serializers import (
    AIChatHistorySerializer,
    OpenAPISerializer,
    WeatherForecastSerializer,
)
from home.models import AIChatHistory

# from home.tasks import weather_forecast_task

client = OpenAI(api_key=get_env_variable("OPEN_AI_KEY", "XXXX_XXX"))
API_KEY = get_env_variable("WEATHER_FORECAST_API_KEY", "XXX_XXX")


class OpenAPIView(generics.CreateAPIView):
    serializer_class = OpenAPISerializer

    @extend_schema(
        request=OpenAPISerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        API endpoint for open api answers response to question is related to crops
        or agriculture or pest or pest alert or weather or weather forecast or crop
        market insight or agricultural market insight.
        """
        serializer = OpenAPISerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.data.get("prompt")
            prompt = (
                "if the question is related to crops or agriculture or"
                + "pest or pest alert or weather or weather forecast or crop market"
                + "insight or agricultural market insight"
                + f" - answer it: {text} else say can't answer this!"
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": text,
                    }
                ],
                model="gpt-3.5-turbo",
                max_tokens=256,
                temperature=0.5,
            )
            response = chat_completion.choices[0].message.content
            resp = Response(data={"data": response}, status=status.HTTP_200_OK)
            AIChatHistory.objects.create(
                title=text,
                user=request.user,
                response=response,
            )
            return resp
        return Response(
            data={"data": "unable to process request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class OpenAIHistoryListView(generics.ListAPIView):
    serializer_class = AIChatHistorySerializer

    def get(self, request, *args, **kwargs):
        """
        Endpoint to return Open AI chat history
        """
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = AIChatHistory.objects.select_related("user") \
            .filter(user=self.request.user)
        return qs


class OpenAIHistoryDetailView(generics.RetrieveAPIView):
    serializer_class = AIChatHistorySerializer
    lookup_url_kwarg = "uid"

    def get(self, request, *args, **kwargs):
        """
        Endpoint to return a single Open AI chat history
        """
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        uid = self.kwargs["uid"]
        qs = AIChatHistory.objects.select_related("user") \
            .get(uid=uid)
        return qs


class WeatherForecastAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=WeatherForecastSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = WeatherForecastSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.data.get("location")
            weather_details = {}
            r = requests.get(
                "http://api.weatherstack.com/current"
                + f"?access_key={API_KEY}&query={query}"
            )
            resp = json.loads(r.text)
            current_weather = resp["current"]
            location_weather = resp["location"]
            weather_details.update(
                {"current": current_weather, "location": location_weather}
            )
            return Response(data=weather_details, status=status.HTTP_200_OK)
        return Response(
            data="Unable to process request", status=status.HTTP_400_BAD_REQUEST
        )
