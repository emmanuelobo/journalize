from django.shortcuts import render
from .forms import JournalForm
from django.contrib.auth.models import User



def all_entries(request):
    data = {"entries": request.user.entry_set.all()}
    return render(request, 'subtemplate/journal_entries.html', data)

def create_entry(request):
    form = JournalForm()
    data = {'form':form}
    return render(request, 'subtemplate/new_journal_entry.html', data)

def edit_entry(request, id):
    data = {}
    return render(request, 'subtemplate/edit_journal_entry.html', data)