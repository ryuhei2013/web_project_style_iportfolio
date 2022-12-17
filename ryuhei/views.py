from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import TemplateView

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """The home page for ryuhei"""
    return render(request, 'ryuhei/index.html')

def about(request):
    """The about page for ryuhei"""
    return render(request, 'ryuhei/about.html')



@login_required
def topics(request):
    """Show all topics."""
    topics_list = Topic.objects.order_by('date_added')
    context = {'topics': topics_list}
    return render(request, 'ryuhei/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'ryuhei/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ryuhei:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'ryuhei/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic."""
    entry_topic = Topic.objects.get(id=topic_id)
    entry_user = request.user

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry_input = form.save(commit=False)
            new_entry_input.topic = entry_topic
            new_entry_input.owner = entry_user
            new_entry_input.save()
            return redirect('ryuhei:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': entry_topic, 'form': form}
    return render(request, 'ryuhei/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if entry.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('ryuhei:topic', topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'ryuhei/edit_entry.html', context)


class HomeView(TemplateView):
    template_name = 'index.html'
