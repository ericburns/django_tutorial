from django.contrib import admin
from polls.models import Poll, Choice

# This file is used for configuring to display in the Admin page

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 3

class PollAdmin(admin.ModelAdmin):
	# Changes the way the list of polls are displayed to be a detailed
	# view, including all of these columns + methods
	list_display = ('question', 'pub_date', 'was_published_recently')
	
	# Add a filter by date option on the side of the list view
	list_filter = ['pub_date']
	
	# Add a search filter by question on the list view page
	search_fields = ['question']
	
	# Add ability to drill down by date
	date_hierarchy = 'pub_date'
	
	# Changes the way a specific poll is presented in admin, using
	# fieldsets and a css class that actually collapses / expands
	fieldsets = [
		(None,					{'fields': ['question']}),
		('Date information', 	{'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	
	# Sets the Choice model to be inline with the Poll
	inlines = [ChoiceInline]

# Register the custom PollAdmin display
admin.site.register(Poll, PollAdmin)
