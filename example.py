# this is for a django application, I am using the django templates to render out the views.
# I have a base protected view for each Class based view (Create, List, Update & Delete)

def request_user_passes_base_protected_view_test(view: View):
    # this is my user passes test to check if theyre allowed to use this view.
    return view.request.user.is_superuser

# The below are the base views
class BaseProtectedListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    template_name = 'access/object_list.html'

    def test_func(self):
        return request_user_passes_base_protected_view_test(self)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['object'] = self.model
        return context

class BaseProtectedCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    template_name = 'access/settings_object_form.html'

    def test_func(self):
        return request_user_passes_base_protected_view_test(self)

class BaseProtectedUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'access/settings_object_form.html'

    def test_func(self):
        return request_user_passes_base_protected_view_test(self)


class BaseProtectedDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    template_name = 'access/settings_confirm_delete.html'

    def test_func(self):
        return request_user_passes_base_protected_view_test(self)
    
# I have made a function that builds all 4 views for my views folder

def protected_view_crud_builder(model_class, create_update_form, deleted_success_url: str) -> tuple:

    class CreatedListView(BaseProtectedListView):
        model = model_class

    class CreatedCreateView(BaseProtectedCreateView):
        model = model_class
        form_class = create_update_form

    class CreatedUpdateView(BaseProtectedUpdateView):
        model = model_class
        form_class = create_update_form

    class CreatedDeleteView(BaseProtectedDeleteView):
        model = model_class
        success_url = reverse_lazy(deleted_success_url)

    return CreatedListView, CreatedCreateView, CreatedUpdateView, CreatedDeleteView


# Then in my views for each setting type I have done this
SettingTypeListView, SettingTypeCreateView, SettingTypeUpdateView, SettingTypeDeleteView = protected_view_crud_builder(SettingType,
                                                                                                                       SettingTypeCreateModelForm,
                                                                                                                       'setting_type-list')

# repeat as needed, in my case, almost 5 times in the initial build, but I would like to manage more features in future

