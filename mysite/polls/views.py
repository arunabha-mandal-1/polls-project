from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     return render(request, "polls/index.html", {
#         "latest_question_list": latest_question_list
#     })

# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question doesn't exist.")
#     # return render(request, "polls/detail.html", {
#     #     "question": question
#     # })

#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {
#         "question": question
#     })

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {
#         "question": question
#     })

# refactoring code and using django's generic views
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        qlist = Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
        return qlist
        # qlist_with_choices = []
        # for q in qlist:
        #     if q.choice_set.all():
        #         qlist_with_choices.append(q)
        # return qlist_with_choices
    
class DetailView(generic.DeleteView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
    return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

