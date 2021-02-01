from django.shortcuts import render, redirect, HttpResponseRedirect, reverse, HttpResponse
from django.db.models import F
from django.urls import reverse_lazy
from bootstrap_modal_forms.generic import BSModalFormView
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .models import Caixa, CreditoNoCaixa, DebitoNoCaixa, Oferta, LancamentoOferta, Contribuinte
from .forms import CaixaForm, DebitoNoCaixaForm, CreditoNoCaixaForm, OfertaForm, LancamentoOfertaForm, FilterLancOfertas
import datetime
from django.contrib.auth.decorators import login_required

# Caixa Views
# ======================================================================================================

@login_required()
def create_caixa(request):
    form = CaixaForm()
    if not request.is_ajax():
        if request.method == 'POST':
            form = CaixaForm(data=request.POST or None)
            if form.is_valid():
                new_caixa = form.save(user=request.user, commit=False)
                new_caixa.save()
                return HttpResponseRedirect(reverse('tesouraria:caixa', args=(new_caixa.pk,)))
        else:
            form = CaixaForm()
    else:
        pass
    return render(request, 'caixas/create_caixa.html', {'title': 'Criar Caixa',
                                                        'active_caixas': 'active',
                                                        'form': form
                                                        })

@login_required
def view_caixa(request, pk):
    dados = Caixa.objects.filter(pk=pk)
    cx = Caixa.objects.get(pk=pk)
    title = 'Caixa' + str(cx.nome)
    return render(request, 'caixas/view_caixa.html', {'title': title,
                                                      'active_caixas': 'active',
                                                      'dados': dados,
                                                      'pk': pk})

@login_required
def caixas(request):
    caixas = request.user.caixa.all()
    # TODO
    """ Pagination, filter """
    return render(request, 'caixas/caixas.html', {'title': 'Caixas',
                                                  'active_caixas': 'active',
                                                  'caixas': caixas})

@login_required
def update_caixa(request, pk):
    obj = Caixa.objects.get(pk=pk)
    title = 'Editar Caixa ' + str(obj.nome)
    if request.method == 'POST':
        form = CaixaForm(request.POST, instance=obj)
        if form.is_valid():
            updated_caixa = form.save(user=request.user)
            return HttpResponseRedirect(reverse('tesouraria:caixa', args=(updated_caixa.pk,)))
    else:
        form = CaixaForm(instance=obj)
    return render(request, 'caixas/update_caixa.html', {'title': title,
                                                        'form': form,
                                                        'nome': obj.nome,
                                                        'pk': obj.pk})


# TODO
@login_required
def delete_caixa(request, pk):
    obj = Caixa.objects.get(pk=pk)
    obj.delete()
    return HttpResponseRedirect(reverse('tesouraria:caixas'))


# ======================================================================================================

# Vizualizar lista de lançamentos específicos de cada caixa
def lancamentos_oferta_caixa(request, pk):
    dados = Caixa.objects.filter(pk=pk)
    lancamentos = LancamentoOferta.objects.filter(lancar_no_caixa__id=pk)
    return render(request, 'caixas/lancamentos_oferta_caixa.html', {'dados': dados,
                                                                    'lancamentos': lancamentos,
                                                                    'pk': pk,
                                                                    })


# Movimentações entre Caixas Views
# ======================================================================================================

# Função adicinal que cria uma sigla com numeros crescentes para Entradas e Sáidas
def incrementar_num_ref(model_, first_ref, ref):
    ultimo_ = model_.objects.all().order_by('id').last()
    if not ultimo_:
        return first_ref
    else:
        referencia = ultimo_.sigla
        ref_int = int(referencia.split(ref)[-1])
        new_ref_int = ref_int + 1
        new_referencia = ref + str(new_ref_int) + datetime.date.today()
        return new_referencia


def create_entrada_no_caixa(request):
    title = 'Trânsferencias | Caixas'
    form = CreditoNoCaixaForm(user=request.user)
    message = False
    message_content = ""
    message_double_cx = False
    # if request.is_ajax():
    if request.method == 'POST':
        form = CreditoNoCaixaForm(data=request.POST or None, user=request.user)
        if form.is_valid():
            valor = form.cleaned_data['valor']
            # congregacao = form.cleaned_data['congregacao']

            pre_save = form.save(user=request.user, commit=False)
            pre_save.sigla = 'ENTRADA'  # incrementar_num_ref(CreditoNoCaixa, 'ENTRADA1', 'ENTRADA')

            if form.cleaned_data['caixa'] == form.cleaned_data['cxa_a_debitar']:
                message_double_cx = True
                CreditoNoCaixa.objects.filter(pk=pre_save.pk).delete()

            sigla = 'SAIDA'  # incrementar_num_ref(DebitoNoCaixa, 'SAIDA1', 'SAIDA')
            nome_do_caixa_a_debitar = pre_save.cxa_a_debitar
            # TODO
            # info_adicional = 'Entrada criada a partir de uma retirada do caixa:' + nome_do_caixa_a_debitar

            # Descontando valor da saida
            get_caixa_a_debitar = request.user.caixa.filter(nome=nome_do_caixa_a_debitar)
            for caixa_a_debitar in get_caixa_a_debitar:
                current_cx_deb = Caixa.objects.get(pk=caixa_a_debitar.pk)
                # current_cx_deb.saldo = F('saldo')  # - pre_save.valor
                if current_cx_deb.saldo <= pre_save.valor:
                    message = True
                    message_content = "O Caixa " + str(
                        form.cleaned_data['cxa_a_debitar']) + " não possui saldo suficiente para ser debitado!"
                    CreditoNoCaixa.objects.filter(pk=pre_save.pk).delete()
                else:
                    current_cx_deb.saldo = F('saldo') - pre_save.valor
                    pre_save.save()
                    current_cx_deb.save()

                    criar_retirada = DebitoNoCaixa(user=request.user,
                                                   sigla=sigla,
                                                   caixa=nome_do_caixa_a_debitar,
                                                   valor=valor,
                                                   congregacao=congregacao,
                                                   responsavel=pre_save.responsavel,
                                                   info_adicional='teste')
                    criar_retirada.save()

                    # Adicionando valor da entrada ao saldo do caixa
                    caixa_nome = pre_save.caixa
                    caixa = request.user.caixa.filter(nome=caixa_nome)
                    for caixa_entrada in caixa:
                        current_caixa_entrada = Caixa.objects.get(pk=caixa_entrada.pk)
                        current_caixa_entrada.saldo = F('saldo') + valor
                        current_caixa_entrada.save()

                        pk = caixa_entrada.pk  # com o auxilio da pk, a proxima pagina é redirecionada corretamente
                        return HttpResponseRedirect(reverse('tesouraria:movimentacoes', args=(pk,)))
        else:
            # TODO
            print(form.errors)
    else:
        form = CreditoNoCaixaForm(user=request.user)
    # else:
    #    pass
    return render(request, 'create_credito_no_caixa.html', {'title': title,
                                                            'active_caixas': 'active',
                                                            'form': form,
                                                            'message': message,
                                                            'message_content': message_content,
                                                            'message_double_cx': message_double_cx,
                                                            })


# TODO Avaliar prioridade
# def create_saida_no_caixa(request):
#    if request.method == 'POST':
#        form = DebitoNoCaixaForm(data=request.POST or None)
#        if form.is_valid():
#            form.sigla = 'SAIDA'  # incrementar_num_ref(DebitoNoCaixa, 'SAIDA1', 'SAIDA')
#            new_saida = form.save(user=request.user, commit=False)
#            new_saida.save()
#            return HttpResponseRedirect(reverse('tesouraria:caixa', args=(new_saida.pk,)))
#        else:
#            print(form.errors)
#    else:
#        form = DebitoNoCaixaForm(user=request.user)
#    return render(request, 'create_debito_no_caixa.html', {'form': form})


# Mostra todas movimentações do caixa específico (Entrada e Saídas)
def movimentacoes(request, pk):
    dados = Caixa.objects.filter(pk=pk)
    title = 'Movimentações | Caixa ' + str(Caixa.objects.get(pk=pk).nome)
    entradas = CreditoNoCaixa.objects.filter(caixa=pk)
    saidas = DebitoNoCaixa.objects.filter(caixa=pk)
    return render(request, 'movimentacoes/entradas_saidas_caixa.html',
                  {'title': title,
                   'dados': dados,
                   'entradas': entradas,
                   'saidas': saidas,
                   'pk': pk,
                   'active_caixas': 'active'})


# Ofertas Views
# ======================================================================================================

def create_oferta(request):
    form = OfertaForm()
    if not request.is_ajax():
        if request.method == 'POST':
            form = OfertaForm(data=request.POST or None)
            if form.is_valid():
                new_oferta = form.save(user=request.user, commit=False)
                new_oferta.save()
                return HttpResponseRedirect(reverse('tesouraria:oferta', args=(new_oferta.pk,)))
            else:
                # TODO
                print(form.errors)
        else:
            form = OfertaForm()
    else:
        pass
    return render(request, 'ofertas/create_oferta.html', {'title': 'Criar Oferta',
                                                          'form': form})


def view_oferta(request, pk):
    ofertas = Oferta.objects.filter(pk=pk)
    title = 'Oferta | ' + str(Oferta.objects.get(pk=pk).nome)
    return render(request, 'ofertas/view_oferta.html', {'title': title,
                                                        'ofertas': ofertas})


def ofertas(request):
    data = request.user.oferta.all()
    # TODO Pagination and filters for searching
    return render(request, 'ofertas/ofertas.html', {'data': data})


# TODO Update function
# TODO Delete function


# Lançamentos Views
# ======================================================================================================

def aux(pk):
    lancamento = LancamentoOferta.objects.filter(pk=pk)
    for i in lancamento:
        return i.lancar_no_caixa


class LancarOfertaView(BSModalFormView):
    template_name = 'lancamentos/create_lanc_oferta.html'
    form_class = LancamentoOfertaForm

    def get_context_data(self, **kwargs):
        context = super(LancarOfertaView, self).get_context_data(**kwargs)
        # array_contribuintes = []
        contribuintes = Contribuinte.objects.filter(user=self.request.user)  # .values('nome')
        # for item in contribuintes:
        #    array_contribuintes.append(str(item))
        # json_contribuintes = json.dumps(array_contribuintes, cls=DjangoJSONEncoder)
        context['contribuintes'] = contribuintes  # json_contribuintes
        return context

    def get_form_kwargs(self):
        kwargs = super(LancarOfertaView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        success_url = HttpResponseRedirect(reverse('tesouraria:lancamentos_oferta'))
        if not self.request.is_ajax():
            nome_oferta = form.cleaned_data['oferta']
            caixa = form.cleaned_data['lancar_no_caixa']

            pre_save = form.save(user=self.request.user, commit=False)

            # Atualizando o saldo do caixa, a partir do lançamento
            get_caixa = self.request.user.caixa.filter(nome=caixa)
            for cx in get_caixa:
                currrent_cx = Caixa.objects.get(pk=cx.pk)
                currrent_cx.saldo = F('saldo') + pre_save.valor
                currrent_cx.save()

            # TODO Implementar numeração adicional
            pre_save.sigla = 'OFERTA/' + str(pre_save.pk) + str(
                datetime.date.today().year)  # incrementar_num_ref(LancamentoOferta, 'OFERTA1', 'OFERTA')
            pre_save.save()
            success_url = HttpResponseRedirect(reverse('tesouraria:lancamento_oferta', args=(pre_save.pk,)))
        else:
            pass
        return success_url


def view_lancamento_oferta(request, pk):
    lancamento = LancamentoOferta.objects.filter(pk=pk)
    cx = request.user.caixa.get(nome=aux(pk))  # Envia a pk para criar um link que redireciona ao caixa especifico
    return render(request, 'lancamentos/view_lancamento_oferta.html', {'active_lancamentos': 'active',
                                                                       'title': 'Lançamento',
                                                                       'cx': cx.pk,
                                                                       'lancamento': lancamento})


def lancamentos_oferta(request):
    lancamentos_ = None
    lancamentos = request.user.lancamentooferta.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(lancamentos, 10)
    try:
        lancamentos_ = paginator.page(page)
    except PageNotAnInteger:
        lancamentos_ = paginator.page(1)
    except EmptyPage:
        lancamentos_ = paginator.page(paginator.num_pages)
    form = FilterLancOfertas(data=request.GET or None, user=request.user)
    if form.is_valid():
        lancamentos = request.user.lancamentooferta.filter(oferta=form.cleaned_data['ofertas'])
        page = request.GET.get('page', 1)
        paginator = Paginator(lancamentos, 10)
        try:
            lancamentos_ = paginator.page(page)
        except PageNotAnInteger:
            lancamentos_ = paginator.page(1)
        except EmptyPage:
            lancamentos_ = paginator.page(paginator.num_pages)
    else:
        # TODO
        print('wait...')
    return render(request, 'lancamentos/lancamentos_oferta.html', {'title': 'Lançamentos Ofertas',
                                                                   'lancamentos_': lancamentos_,
                                                                   'active_lancamentos': 'active',
                                                                   'ofertas': ofertas,
                                                                   'form': form})

# TODO Update function for Lançamentos

# TODO Delete function for Lançamentos


# TODO Receitas
# ======================================================================================================

# TODO Despesas
# ======================================================================================================


# def contribuinte_name_search(request):
#    if request.is_ajax():
#        q = request.GET.get('term', '')
#        names = Contribuinte.objects.filter(nome__istartswith=q)
#        result = []
#        for n in names:
#            name_json = n.nome
#            result.append(name_json)
#        data = json.dumps(result)
#    return JsonResponse(data, safe=False)


# def create_lanc_oferta(request):
#    title = 'Criar Lançamento'
#    #form = LancamentoOfertaForm(user=request.user, data=request.POST or None)
#
#    if request.method == 'POST':
#        form = LancamentoOfertaForm(user=request.user, data=request.POST or None)
#        if form.is_valid():
#            nome_oferta = form.cleaned_data['oferta']
#            caixa = form.cleaned_data['lancar_no_caixa']
#
#            pre_save = form.save(user=request.user, commit=False)
#
#            # Atualizando o saldo do caixa, a partir do lançamento
#            get_caixa = request.user.caixa.filter(nome=caixa)
#            for cx in get_caixa:
#                currrent_cx = Caixa.objects.get(pk=cx.pk)
#                currrent_cx.saldo = F('saldo') + pre_save.valor
#                currrent_cx.save()
#
#                pre_save.sigla = 'OFERTA'  # incrementar_num_ref(LancamentoOferta, 'OFERTA1', 'OFERTA')
#                new_lanc = form.save(user=request.user, commit=False)
#                new_lanc.save()
#                return HttpResponseRedirect(reverse('tesouraria:lancamento_oferta', args=(new_lanc.pk,)))
#    else:
#        form = LancamentoOfertaForm(user=request.user)
#    return render(request, 'ofertas/create_lanc_oferta.html', {'title': title, 'form': form})


# def aux(pk):
#    lancamento = LancamentoOferta.objects.filter(pk=pk)
#    for i in lancamento:
#        return i.lancar_no_caixa


# @login_required
# def dizimos(request):
#    user_id = request.user.pk
#    user = User.objects.get(pk=user_id)
#    print(user.coordenador)
#    return render(request, 'dizimos.html')
