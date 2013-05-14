#Django Tutorial

##PART 1

**Create a project**
```
django-admin startproject [project_name]
```

*Note: In Ubuntu’s distrobution of Django, django-admin.py is renamed to django-admin. Leave of .py. It doesn’t do this for manage.py, however.*

**Create an app**
```
manage.py startapp [app_name]
```

**Project vs App**
An app is a webapp with a specific function. A project can include many apps. Apps are pluggable, meaning that they can be plugged into many other projects.

* settings.py
    * database configuration
    * timezone
    * installed apps
    * many other settings relating to overall site configuration, such as user upload URL, etc.

```
manage.py syncdb    #important
```

Used to create database tables found in the settings.py installed apps section. For example, when the Polls app was created, I had to add it to the settings.py installed apps section, and then call syncdb so it would create the tables I needed for that app.

**Models**
* located in models.py, inside the app folder
* each model class extends models.Model
* by convention, class instances map to db columns using their name
* you can override this by providing a human-readable name as the first param
* supports typical relationships 1-1, 1-*, *-*

```
manage.py shell
```

Goes through manage.py to import your project’s settings.py

```
from django.utils import timezone
p = Poll(question=”What’s new?”, pub_date=timezone.now())
```

Why? pub_date expects a timezone, because of the default settings.

p.save()

Must call to save to the database, every time. (Is this like Rails, where validations are performed on save and returns false if it fails?) Also, this gives it an ID.

__unicode__()

Instead of overriding the string method (__str__()), you override the __unicode__() method to provide readable ouput from Poll.objects.all(). The Django str method just calls the unicode method.

**Filtering and getting**

By ID
```
Poll.objects.filter(id=1)
```

Starts With
```
Poll.objects.filter(question__startswith(‘What’))
```

By primary key
```
Poll.objects.get(pk=1)
```

**Create a Poll with its constructor**
```
p = Poll(question=”Whatevs”, pub_date=timezone.now())
p.save()
```

**Add choices**
```
p.choice_set.create(choice_text=”Yo”, votes=0)
```

^The thing there is that p’s choice “set” gives access to the choice table and allows you to use the create method to invoke choice’s constructor.

You can separate names with “__” in order to deal with those relationships, like
```
Choice.objects.filter(poll__pub_date__year=current_year)
```

This will get all the choices from polls that were published this year.

##Part 2
**Activate the admin site**
https://docs.djangoproject.com/en/1.5/intro/tutorial02/#activate-the-admin-site

Pretty straightforward, add it to the installed apps section in settings.py, run syncdb, then open up urls.py and follow the comment instructions.

**Adding models to an admin site**
create an admin.py file in the root of the app directory and register it

Admin forms are generated based on the model

Just registering related tables isn’t user-friendly enough. It’s better to create Inlines. You can add them to the admin class of the object that will contain it. Also have to create a class for the actual inline item, with something like ChoiceInline and then you can set its model (Choice).

Using admin.TabularInline, rather than admin.StackedInline condenses the items and saves a lot of space on the screen.

*# Notes from this point on for part 2 are mostly inline with the code, except for important notes*

##Part 3
**Mapping views to URLs**
* Django uses URLconf. URLconfs map patterns (regexes) to views
* url() needs a regex and a view
* it compares each URL to the regex for a match
* the passed view is called when it matches
* it passes in the values from the query string

the routing seems to be that the app itself has to call the view and that’s where its view is contained, but you have to let the project know by including it in its URLconf as well

> When somebody requests a page from your Web site – say, “/polls/34/”, Django will load the mysite.urls Python module because it’s pointed to by the ROOT_URLCONF setting. It finds the variable named urlpatterns and traverses the regular expressions in order. The include() functions we are using simply reference other URLconfs. Note that the regular expressions for the include() functions don’t have a $ (end-of-string match character) but rather a trailing slash. Whenever Django encounters include(), it chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.

The project’s URLconf will actually handle /polls/ or whatever the app is mapped to. Then that’s stripped off and the rest is sent to the URLconf for the app itself. It then uses its own regex to determine what it’s looking for and which variables it should keep.

**View with templates**
* create a directory in the app called ‘templates’
* create a directory in that called ‘polls’ (or whatever the app name is)
* create an html file with the name of the method in the controller (ease of use)
* use the django templating language to make the page
* in the controller and in the correct method, load the template
* set the context and fill it with the variables you’re using in the view (the context is a dictionary containing the values mapped to the view’s variable names)
* return the rendered template in HttpResponse

**render()**
```
return render(request, ‘imaview.html’, context)
```

**Http404**
raise this when someone attempts to access a resource that doesn’t exist.

**get_object_or_404()**
```
poll = get_object_or_404(Poll, pk=poll_id) #this is awesome
```

**Custom error pages**
handler404 #set this in the root project urlconf file
handler500

**Templating**
template code is python between {% %} and html

##Part 4

all POST forms should use {% csrf_token %} to prevent cross site request forgeries

Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from being posted twice if a user hits the Back button.

request.POST is a dictionary-like structure that lets you access data submitted by key

KeyError is raised if there is no POST data

Use generic views for views that only differ on the template they use but essentially pass the same data.
