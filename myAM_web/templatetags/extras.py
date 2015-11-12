from django import template

register = template.Library()

@register.filter(name='get')
def get(d, key_name):
	return d.get(key_name, ' ')

@register.filter(name='days')
def days(share):
	return share.getDays()

