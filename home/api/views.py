from openai import OpenAI
from rest_framework import generics, status
from rest_framework.response import Response

from agrowise.utils.env_variable import get_env_variable
from home.api.serializers import OpenAPISerializer

client = OpenAI(api_key=get_env_variable("OPEN_AI_KEY"))


class OpenAPIView(generics.CreateAPIView):
    serializer_class = OpenAPISerializer

    def post(self, request, *args, **kwargs):
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
