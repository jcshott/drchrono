from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    user = request.session.get("user", None)
    if user:
        return redirect("/patients")

    else:
        params = {"redirect": "http%3A//127.0.0.1%3A8000/medications/authorize",
                "client_id": os.environ["DRCHRONO_MEDS_CLIENT_ID"]}

        return render(request, "medications/index.html", params)


def authorize(request):
    """
    Handles authorizing application.  Stores drchrono API tokens in db

    """

def patients(request):
    """
    View for patient list to access medications
    """

    return HttpResponse("hello medications app")
