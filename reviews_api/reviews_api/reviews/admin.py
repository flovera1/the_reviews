# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Company, Reviews

# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
	model = Reviews
	list_display  = ('company', 'rating', 'user_name', 'comment', 'pub_date', 
		'ip_address',
		)
	list_filter   = ['pub_date', 'user_name', 
					'ip_address',
					]
	search_fields = ['comment', 
	'ip_address',
	]

admin.site.register(Company)
admin.site.register(Reviews, ReviewAdmin)