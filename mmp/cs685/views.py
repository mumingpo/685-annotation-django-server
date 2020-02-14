import json

from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Annotator, Annotation, Tweet

# Create your views here.
def index(request):
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    try:
        annotator = Annotator.objects.get(email=username, password=password)
    except Exception:
        return redirect("login")

    annotations = Annotation.objects.filter(annotator=annotator)
    num_remain = annotations.filter(choice=0).count()

    annotation_list = [{
        "id": annotation.order,
        "sample_text": annotation.tweet.text[:40],
        "status": annotation.get_choice_text()
    } for annotation in annotations.order_by("order")]

    context = {
        "annotator": annotator,
        "num_remain": num_remain,
        "annotation_list": annotation_list,
    }
    return render(request, "cs685/index.html", context)


def login(request):
    if request.method == "GET":
        request.session["username"] = None
        request.session["password"] = None
        return render(request, "cs685/login.html")
    elif request.method == "POST":
        username = request.POST.get("email", None)
        password = request.POST.get("password", None)
        try:
            Annotator.objects.get(email=username, password=password)
        except Exception:
            return redirect("login")
        request.session["username"] = username
        request.session["password"] = password
        return redirect("index")


def annotate(request, tweet_id):
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    try:
        annotator = Annotator.objects.get(email=username, password=password)
    except Exception:
        return redirect("login")

    annotation = Annotation.objects.filter(annotator=annotator).get(order=tweet_id)
    tweet = annotation.tweet
    if request.method == "GET":
        tweet_id = annotation.order
        context = {
            "tweet": tweet.text,
            "tweet_id": tweet_id,
        }
        return render(request, "cs685/annotate.html", context)
    elif request.method == "POST":
        annotation.choice = int(request.POST["sentiment"])
        annotation.save()
        next_annotation = Annotation.objects.filter(annotator=annotator, choice=0).order_by("order")[0]
        return redirect("/cs685/{}/".format(next_annotation.order))


def data(request):
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    try:
        annotator = Annotator.objects.get(email=username, password=password)
        assert(annotator.name == "Steven Qiu")
    except Exception:
        return redirect("login")

    annotators = Annotator.objects.all()
    tweets = Tweet.objects.all()

    header = [annotator.name for annotator in annotators]
    rows = [
        [tweet.text] + [Annotation.objects.get(
            annotator=annotator,
            tweet=tweet
        ).get_choice_text() for annotator in annotators] \
        for tweet in tweets.order_by("id")
    ]
    context = {
        "annotators": header,
        "rows": rows,
    }
    return render(request, "cs685/data.html", context)

def download(request):
    username = request.session.get("username", None)
    password = request.session.get("password", None)
    try:
        annotator = Annotator.objects.get(email=username, password=password)
        assert(annotator.name == "Steven Qiu")
    except Exception:
        return redirect("login")

    annotators = Annotator.objects.all()
    tweets = Tweet.objects.all()
    header = ["Tweet content"] + [annotator.name for annotator in annotators]
    rows = [
        [tweet.text] + [Annotation.objects.get(
            annotator=annotator,
            tweet=tweet
        ).get_choice_text() for annotator in annotators] \
        for tweet in tweets.order_by("id")
    ]
    json_obj = {
        "header": header,
        "rows": rows
    }
    response = HttpResponse(json.dumps(json_obj), content_type="application/json")
    response["Content-Disposition"] = "attachment; filename=annotation_data.json"
    return response

