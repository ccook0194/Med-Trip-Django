from django.apps import apps

import importlib
# import treatment.models.blogcontactproxy

def UpdateSeenMiddleWare(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = get_response(request)

        if "admin" in request.path and not 'jsi18n' in request.path:
            path = request.path
            path = path.split("/")
            path = list(filter(lambda x: x != "", path))
            if len(path) > 2:
                app_name = path[1]
                model_name = path[2]
                # print(apps)
                if hasattr(apps.get_app_config(app_name), 'show_model_count') and apps.get_app_config(app_name).show_model_count == True:
                    model = apps.get_app_config(app_name).get_model(model_name)
                    if model:
                        model.objects.filter(is_seen=False).update(is_seen=True)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware