import user_agents

from visitors.models import Visitor


class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith('/admin/'):  # Don't track admin access
            # print(request.META)
            ip_address = self.get_client_ip(request)
            user_agent_string = request.META.get('HTTP_USER_AGENT', '')
            language = request.META.get('LANGUAGE', '')
            remote_host = request.META.get('REMOTE_HOST', '')
            user_agent = user_agents.parse(user_agent_string)

            device_name = request.META.get('REMOTE_HOST', '')  # May not always work

            visitor, created = Visitor.objects.get_or_create(
                ip_address=ip_address,
                defaults={
                    'language': language,
                    'remote_host': remote_host,
                    'user_agent': user_agent_string,
                    'device_name': device_name,
                    'operating_system': user_agent.os.family,
                    'browser': user_agent.browser.family,
                    'referrer': request.META.get('HTTP_REFERER', '')
                }
            )

            if not created:
                visitor.user_agent = user_agent_string
                visitor.device_name = device_name
                visitor.operating_system = user_agent.os.family
                visitor.browser = user_agent.browser.family
                visitor.save()

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
