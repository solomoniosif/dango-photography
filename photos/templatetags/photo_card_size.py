from django import template

register = template.Library()


@register.simple_tag
def next_card_size(i):
	card_sizes = [
		'col-lg-8 col-md-12',
		'col-lg-4 col-md-6',
		'col-lg-3 col-md-6',
		'col-lg-6 col-md-6',
		'col-lg-6 col-md-6',
		'col-lg-4 col-md-6',
		'col-lg-4 col-md-6',
		'col-lg-4 col-md-6',
		'col-lg-8 col-md-12',
	]
	i = i % 9
	return card_sizes[i-1]
