from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect#look up redirect
from django import forms
from django.urls import reverse #look this up
from django.db.models import Q
from markdown2 import Markdown
import random

from . import util

markdown = Markdown()

class ArticleForm(forms.Form):
 #search = forms.CharField(label = "Search Encyclopedia")
 #rating = forms.IntegerField(label = "rating", min_value=1, max_value=5)

    articleSubject = forms.CharField(label="Subject ")
    articleBody = forms.CharField(  label = "Body", widget=forms.Textarea(attrs={'id': 'myFIELD', 'label': "Body ",
     'rows' : '4', 'cols': '40',
     'placeholder': 'Enter the atricle text here, you have to start the article with # and a newline for it to display properly!'
      }) )

def index(request ):
    if request.method == 'POST': # from create new page
        form = ArticleForm(request.POST)
        if form.is_valid():
            newSubject = form.cleaned_data["articleSubject"]
            newArticle = form.cleaned_data["articleBody"]
            print("enterecd " + newSubject)
            print("looking for ")   
            print(util.list_search(newSubject))
            if util.list_search(newSubject):
                return render(request, "encyclopedia/error.html")

            util.save_entry(newSubject, newArticle)
            
            url = reverse('wiki' , kwargs={'subject': newSubject})
            
            return HttpResponseRedirect(url)
           
    
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, subject):
  
    article = util.get_entry(subject)

    if not article:
        return render(request, "encyclopedia/article.html", {
        "article": "Article does not exist", "subject": subject
    })
    return render(request, "encyclopedia/article.html", {
        "article": markdown.convert(article), "subject": subject
        })

def search(request):
 
    query = request.GET.get('q').lower() #search form is called q in the layout.html file
    
    article = util.get_entry(query)
    if article:
        url = reverse('wiki' , kwargs={'subject': query})
        return HttpResponseRedirect(url)
      
    print( util.list_search(query))
    return render (request, "encyclopedia/index.html", {"entries": util.list_search(query) })
    
    
   
def createNewPage(request):
    return render(request, 'encyclopedia/createNewPage.html', {"form" : ArticleForm().as_p()})

def editPage(request, subject):
    
    if request.method == 'POST': #from edit page
        newArticle = request.POST.get('article')
        newSubject = request.POST.get('subject')

        util.save_entry(newSubject, newArticle)
        url = reverse('wiki' , kwargs={'subject': subject})
        return HttpResponseRedirect(url)

    article = util.get_entry(subject)
    return render(request, "encyclopedia/editPage.html", {
        "article": article, "subject": subject
    })
   


def randomPage(request):
    randomArt = random.choice(util.list_entries())
    article = util.get_entry(randomArt)
    return render(request, "encyclopedia/article.html", {
        "article": markdown.convert(article), "subject": randomArt
        })
# 

    
