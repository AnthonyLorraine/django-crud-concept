def request_user_passes_base_protected_view_test(view: View):
    return view.request.user.is_superuser
