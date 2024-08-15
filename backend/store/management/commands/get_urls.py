from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'List all URLs registered with the router'

    def handle(self, *args, **kwargs):
        resolver = get_resolver()
        url_patterns = resolver.url_patterns

        def list_urls(urlpatterns, depth=0):
            for pattern in urlpatterns:
                if hasattr(pattern, 'url_patterns'):
                    self.stdout.write(' ' * depth + str(pattern.pattern))
                    list_urls(pattern.url_patterns, depth + 2)
                else:
                    self.stdout.write(' ' * depth + str(pattern.pattern))

        list_urls(url_patterns)