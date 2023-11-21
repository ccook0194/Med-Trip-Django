from django.contrib import admin
from django.urls import NoReverseMatch, reverse
from django.utils.text import capfirst
from django.apps import apps


class MyAdminSite(admin.AdminSite):
    # site_header = 'My Project Title'
    # site_title  = 'My Project Title Administration'
    # index_title = 'My Project Title Administration'


    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}
        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry
        for model, model_admin in models.items():
            app_label = model._meta.app_label
            show_model_count = False
            
            if hasattr(apps.get_app_config(app_label), "show_model_count"):
                show_model_count = apps.get_app_config(app_label).show_model_count

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'perms': perms,
                'admin_url': None,
                'add_url': None
            }
            
            if show_model_count and show_model_count == True and hasattr(model_admin, "get_count") and callable(model_admin.get_count):
                model_dict["count"] = model_admin.get_count()

            if perms.get('change') or perms.get('view'):
                model_dict['view_only'] = not perms.get('change')
                try:
                    model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            if perms.get('add'):
                try:
                    model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=self.name)
                except NoReverseMatch:
                    pass
            
            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'app_url': reverse(
                        'admin:app_list',
                        kwargs={'app_label': app_label},
                        current_app=self.name,
                    ),
                    'has_module_perms': has_module_perms,
                    'models': [model_dict],
                    'count': 0,
                }
            
            if show_model_count and show_model_count == True:
                app_dict[app_label]["show_model_count"] = True
                if "count" in model_dict:
                    app_dict[app_label]["count"] += model_dict["count"]

        if label:
            return app_dict.get(label)
        return app_dict