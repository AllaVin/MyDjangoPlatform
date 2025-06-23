from django.http import HttpResponse


# Create your views here.
def test(request):
    return HttpResponse("Congrats, you are in Library applications!")

