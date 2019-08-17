from django_hosts import (
        patterns,
        host,
    )


host_patterns = patterns(
    '',
    host(r'', 'project.urls.urls', name='api'),
    host(r'admin', 'project.urls.admin', name='admin'),
)