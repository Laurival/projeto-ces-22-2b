from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from .forms import QuestionForm,ChoiceForm


def question_new(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            return redirect('polls:detail', pk=question.id)
    else:
        form = QuestionForm()
    return render(request, 'question_edit.html', {'form': form})

class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        "Return the last five published questions.( not including those set to be in the future)"
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'detail.html'
    def get_queryset(self):
        "Exclude any question that aren't puvblished yet."
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'detail.html',{
            'question': question,
            'error_message':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def choice_new(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = question.choice_set.create(choice_text= form.cleaned_data['choice_text'])
            choice.save()
            return redirect('polls:detail', pk=question.id)
    else:
        form = ChoiceForm()
    return render(request, 'choice_edit.html', {'form': form})

