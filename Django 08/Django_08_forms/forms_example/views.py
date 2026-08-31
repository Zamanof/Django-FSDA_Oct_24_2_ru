from django.shortcuts import render, redirect

from .forms import ContactForm, NoteForm


def index(request):
    return render(request, "forms_basic.html")
data = {
    'name':"",
    'email':''
}
def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data['name'] = form.cleaned_data['name']
            data['email'] = form.cleaned_data['email']
            return redirect("contact_success")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})


def contact_success(request):
    return render(
        request,
        "contact_success.html",
        {'data':data}
    )


def note_form(request):
    form = NoteForm(request.POST or None)
    data = None
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
    return render(request, 'noteform.html', {'form': form, 'data': data})

