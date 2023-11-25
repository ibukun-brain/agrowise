import json

import requests
from drf_spectacular.utils import extend_schema
from openai import OpenAI
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from agrowise.utils.env_variable import get_env_variable
from home.api.serializers import OpenAPISerializer, WeatherForecastSerializer

# from home.tasks import weather_forecast_task

client = OpenAI(api_key=get_env_variable("OPEN_AI_KEY"))
API_KEY = get_env_variable("WEATHER_FORECAST_API_KEY")


class OpenAPIView(generics.CreateAPIView):
    serializer_class = OpenAPISerializer

    @extend_schema(
        request=OpenAPISerializer,
    )
    def post(self, request, *args, **kwargs):
        """
        API endpoint for open api answers response to question is related to crops
        or agriculture or pest or pest alert or weather or weather forecast or crop
        market insight or agricultural market insight
        """
        serializer = OpenAPISerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.data.get("prompt")
            prompt = (
                "if the question is related to crops or agriculture or"
                + "pest or pest alert or weather or weather forecast or crop market"
                + "insight or agricultural market insight"
                + f" - answer it: {prompt} else say ask question answer this!"
            )
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-4-1106-preview",
                max_tokens=256,
                temperature=0.5,
            )
            response = chat_completion.choices[0].message.content
            return Response(data={"data": response}, status=status.HTTP_200_OK)
        return Response(
            data={"data": "unable to process request"},
            status=status.HTTP_400_BAD_REQUEST,
        )


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
                "http://api.weatherstack.com/current" +
                f"?access_key={API_KEY}&query={query}"
            )
            resp = json.loads(r.text)
            current_weather = resp["current"]
            location_weather = resp["location"]
            weather_details.update({
                "current": current_weather,
                "location": location_weather
            })
            return Response(
                data=weather_details,
                status=status.HTTP_200_OK
            )
        return Response(
            data="Unable to process request",
            status=status.HTTP_400_BAD_REQUEST
        )
