from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm


@login_required
def profile_edit(request):
    submitted = False
    message = False
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            if form.cleaned_data['nome_da_igreja'] == '':
                print('deu ruim')
                message = True
            else:
                saved = form.save(commit=False)
                if 'profile_image' in request.FILES:
                    saved.profile_image = request.FILES['profile_image']
                    saved.save()
                    submitted = True
                else:
                    #TODO
                    saved.save()
        else:
            #TODO
            print(form.errors)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'config/config_perfil_igreja.html', {'form': form,
                                                                'title': 'Configurar Perfil',
                                                                'active_perfil': 'active',
                                                                'submitted': submitted,
                                                                'message': message})
