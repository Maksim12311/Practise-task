from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Menu, MenuItem

class IndexView(TemplateView):
	template_name = 'menu/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['menus'] = Menu.objects.all()
		return context

def index(request):
	"""View for the main page that demonstrates menu usage"""
	menus = Menu.objects.all()
	return render(request, 'menu/index.html', {'menus': menus})