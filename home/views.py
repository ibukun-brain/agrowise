from django.http import JsonResponse
from django.views import generic


class RedirectSocial(generic.View):
    def get(self, request, *args, **kwargs):
        code, state = str(request.GET["code"]), str(request.GET["state"])
        json_obj = {"code": code, "state": state}
        print(json_obj)
        return JsonResponse(json_obj)
