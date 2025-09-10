from django.shortcuts import redirect
from django.urls import reverse
from functools import wraps

def user_type_required(allowed_types=[]):

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse('gerenciamento_registros:login') + f'?next={request.path}')

            if request.user.tipo_usuario in allowed_types:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('gerenciamento_registros:acesso_negado')
        return _wrapped_view
    return decorator

empresarial_required = user_type_required(allowed_types=['EMPRESA', 'EMPREENDEDOR'])
educacional_required = user_type_required(allowed_types=['APRENDIZ'])