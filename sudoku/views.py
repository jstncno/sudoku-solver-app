from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


from django import forms

import sudoku
import csv

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'.csv'}))

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


def index(request):
    '''latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #data = { 'form': NameForm(),
                     #'data': form.cleaned_data['your_name'] }
            solution = handle_uploaded_file(request.FILES['file'])
            request.session['solution'] = solution

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadFileForm()

        data = {}
        data['form'] = form
        data['solution'] = None

        try:
            if request.session['solution'] != None:
                data['solution'] = []
                for i in range(len(request.session['solution'])):
                    data['solution'].append([])
                    for j in range(len(request.session['solution'])):
                        data['solution'][i].append(request.session['solution'][i][j])
            else:
                data['solution'] = None
            #data['solution'] = request.session['solution']
        except KeyError, TypeError:
            data['solution'] = -1

        request.session['solution'] = None

        if data['solution'] == -1:
            data['error'] = "Oh no! Something was wrong with your input :("

    return render(request, 'sudoku/index.html', data)

# Helper method
def handle_uploaded_file(f):

    board = []
    reader = csv.reader(f)

    for row in reader:
        try:
            board.append(map(int, row))
        except ValueError:
            return -1

    solution = sudoku.solveSudoku(board)
    return solution
    #with open('some/file/name.txt', 'wb+') as destination:
    #    for chunk in f.chunks():
    #        destination.write(chunk)
