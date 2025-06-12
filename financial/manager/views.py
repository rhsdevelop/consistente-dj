import json
from datetime import date, datetime, timedelta
from decimal import Decimal
from calendar import monthrange

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDate, TruncDay
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import *
from .models import *
from .helpers import atualiza_cartao

@login_required
def index(request):
    template = loader.get_template('index.html')
    context = {
        'title': 'Consistente - Gestão de Finanças Pessoais - V.2.0',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'active_dashboard': True,
        'active_dashboard_analise': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_consistentecliente')
def add_cliente(request):
    if request.POST:
        form = AddClienteForm(request.POST)
        item = form.save(commit=False)
        item.create_user = request.user
        item.assign_user = request.user
        item.save()
        messages.success(request, 'Registro adicionado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/cliente/list')
    form = AddClienteForm()
    template = loader.get_template('cliente/add.html')
    context = {
        'title': 'Adicionar Novo Cliente',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_cliente': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_consistentecliente')
def edit_cliente(request, cliente_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            if cliente_id == crc_user.first().consistente_cliente_id:
                cliente = ConsistenteCliente.objects.get(id=cliente_id)
            else:
                raise Http404('Edição da conta indisponível!')
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta.')
            return redirect('/')
    else:
        cliente = ConsistenteCliente.objects.get(id=cliente_id)
    if request.POST:
        form = AddClienteForm(request.POST, instance=cliente)
        item = form.save(commit=False)
        item.assign_user = request.user
        item.save()
        messages.success(request, 'Registro alterado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/cliente/list')
    form = AddClienteForm(instance=cliente)
    template = loader.get_template('cliente/edit.html')
    context = {
        'title': 'Dados da clienteregação Selecionada',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_cliente': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_consistentecliente')
def list_cliente(request):
    form = FindClienteForm(request.GET)
    form.fields['nome'].required = False
    form.fields['fantasia'].required = False
    filter_search = {}
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_search['id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta.')
            return redirect('/')
    for key, value in request.GET.items():
        if key in ['nome', 'fantasia', 'doc'] and value:
            filter_search['%s__icontains' % key] = value
    list_cliente = ConsistenteCliente.objects.filter(**filter_search)
    template = loader.get_template('cliente/list.html')
    context = {
        'title': 'Relação de Clientes do Consistente Cadastrados',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_cliente': list_cliente,
        'form': form,
        'active_register_cliente': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_consistenteusuario')
def add_clienteuser(request):
    if request.POST:
        form = AddClienteUserForm(request.POST)
        item = form.save(commit=False)
        item.create_user = request.user
        item.assign_user = request.user
        item.save()
        messages.success(request, 'Registro adicionado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/clienteuser/list')
    form = AddClienteUserForm()
    template = loader.get_template('clienteuser/add.html')
    context = {
        'title': 'Adicionar Novo Cliente',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_clienteuser': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_consistenteusuario')
def edit_clienteuser(request, usuario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            if usuario_id == crc_user.first().usuario_id:
                cliente = cliente.objects.get(id=usuario_id)
            else:
                raise Http404('clienteregação indisponível!')
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma clienteregação.')
            return redirect('/')
    else:
        clienteuser = ConsistenteUsuario.objects.get(id=usuario_id)
    if request.POST:
        form = AddClienteUserForm(request.POST, instance=clienteuser)
        item = form.save(commit=False)
        item.assign_user = request.user
        item.save()
        messages.success(request, 'Registro alterado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/clienteuser/list')
    form = AddClienteUserForm(instance=clienteuser)
    template = loader.get_template('clienteuser/edit.html')
    context = {
        'title': 'Dados da clienteregação Selecionada',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_clienteuser': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_consistenteusuario')
def list_clienteuser(request):
    form = FindClienteUserForm(request.GET)
    form.fields['consistente_cliente'].required = False
    form.fields['user'].required = False
    filter_search = {}
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_search['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    for key, value in request.GET.items():
        if key in ['nome', 'fantasia', 'doc'] and value:
            filter_search['%s__icontains' % key] = value
    list_clienteuser = ConsistenteUsuario.objects.filter(**filter_search)
    template = loader.get_template('clienteuser/list.html')
    context = {
        'title': 'Relação de Clientes do Consistente Cadastrados',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_clienteuser': list_clienteuser,
        'form': form,
        'active_register_clienteuser': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_banco')
def add_banco(request):
    if request.POST:
        form = AddBancoForm(request.POST)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                crc_user = ConsistenteUsuario.objects.filter(user=request.user)
                if crc_user:
                    item.consistente_cliente = crc_user.first().consistente_cliente
            item.create_user = request.user
            item.assign_user = request.user
            item.save()
            if 'allowed_users' in request.POST and request.POST['allowed_users']:
                for usuariobanco in request.POST.getlist('allowed_users'):
                    item.allowed_users.add(usuariobanco)
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/banco/list')
    form = AddBancoForm()
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            usuarios = [x.user_id for x in ConsistenteUsuario.objects.filter(consistente_cliente_id=crc_user.first().consistente_cliente_id)]
            form.fields['allowed_users'].queryset = User.objects.filter(id__in=usuarios).order_by('username')
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    template = loader.get_template('banco/add.html')
    context = {
        'title': 'Cadastro de Bancos',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_banco': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_banco')
def edit_banco(request, banco_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            banco = Banco.objects.get(id=banco_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        banco = Banco.objects.get(id=banco_id)
    if request.POST:
        form = AddBancoForm(request.POST, instance=banco)
        item = form.save(commit=False)
        item.assign_user = request.user
        item.save()
        item.allowed_users.clear()
        for usuariobanco in request.POST.getlist('allowed_users'):
            item.allowed_users.add(usuariobanco)
        messages.success(request, 'Registro alterado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/banco/list')
    form = AddBancoForm(instance=banco)
    if not request.user.is_staff:
        usuarios = [x.user_id for x in ConsistenteUsuario.objects.filter(consistente_cliente_id=crc_user.first().consistente_cliente_id)]
        form.fields['allowed_users'].queryset = User.objects.filter(id__in=usuarios).order_by('username')
        form.fields['consistente_cliente'].widget = forms.HiddenInput()
    template = loader.get_template('banco/edit.html')
    context = {
        'title': 'Cadastro de Bancos',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_banco': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.delete_banco')
def delete_banco(request, banco_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            banco = Banco.objects.get(id=banco_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        banco = Banco.objects.get(id=banco_id)
    if banco:
        try:
            banco.delete()
            messages.success(request, 'Banco apagado com sucesso!')
        except Exception as err:
            messages.error(request, 'Não é possível apagar o banco!')
            messages.error(request, err)
    else:
        messages.warning(request, 'Não é possível apagar esse banco. Favor, verifique o id.')
    path = request.GET.get('from', None)
    if path:
        return redirect(path)
    else:
        return redirect('/banco/list')


@login_required
@permission_required('manager.view_banco')
def list_banco(request):
    form = FindBancoForm(request.GET)
    form.fields['consistente_cliente'].required = False
    form.fields['nomebanco'].required = False
    form.fields['tipomov'].required = False
    filter_search = {}
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_search['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    for key, value in request.GET.items():
        if key in ['consistente_cliente'] and value:
            filter_search[key] = value
        if key in ['nomebanco', 'tipomov', 'doc'] and value:
            filter_search['%s__icontains' % key] = value
    list_banco = Banco.objects.filter(**filter_search).order_by('nomebanco')
    template = loader.get_template('banco/list.html')
    context = {
        'title': 'Cadastro de Bancos',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_banco': list_banco,
        'form': form,
        'active_register_banco': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_categoria')
def add_categoria(request):
    if request.POST:
        form = AddCategoriaForm(request.POST)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        item = form.save(commit=False)
        if not request.user.is_staff:
            crc_user = ConsistenteUsuario.objects.filter(user=request.user)
            if crc_user:
                item.consistente_cliente = crc_user.first().consistente_cliente
        item.create_user = request.user
        item.assign_user = request.user
        item.save()
        messages.success(request, 'Registro adicionado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/categoria/list')
    form = AddCategoriaForm()
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    template = loader.get_template('categoria/add.html')
    context = {
        'title': 'Cadastro de Categorias',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_categoria': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_categoria')
def edit_categoria(request, categoria_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            categoria = Categoria.objects.get(id=categoria_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        categoria = Categoria.objects.get(id=categoria_id)
    if request.POST:
        form = AddCategoriaForm(request.POST, instance=categoria)
        item = form.save(commit=False)
        item.assign_user = request.user
        item.save()
        messages.success(request, 'Registro alterado com sucesso.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/categoria/list')
    form = AddCategoriaForm(instance=categoria)
    if not request.user.is_staff:
        form.fields['consistente_cliente'].widget = forms.HiddenInput()
    template = loader.get_template('categoria/edit.html')
    context = {
        'title': 'Cadastro de Categorias',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_categoria': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_categoria')
def list_categoria(request):
    form = FindCategoriaForm(request.GET)
    form.fields['consistente_cliente'].required = False
    form.fields['categoria'].required = False
    form.fields['limitemensal'].required = False
    form.fields['tipomov'].required = False
    filter_search = {}
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_search['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    for key, value in request.GET.items():
        if key in ['consistente_cliente'] and value:
            filter_search[key] = value
        if key in ['categoria', 'tipomov', 'doc'] and value:
            filter_search['%s__icontains' % key] = value
    list_categoria = Categoria.objects.filter(**filter_search).order_by('categoria')
    template = loader.get_template('categoria/list.html')
    context = {
        'title': 'Cadastro de Categorias',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_categoria': list_categoria,
        'form': form,
        'active_register_categoria': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_parceiro')
def add_parceiro(request):
    if request.POST:
        form = AddParceiroForm(request.POST)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        item = form.save(commit=False)
        if not request.user.is_staff:
            crc_user = ConsistenteUsuario.objects.filter(user=request.user)
            if crc_user:
                item.consistente_cliente = crc_user.first().consistente_cliente
        item.create_user = request.user
        item.assign_user = request.user
        parceiro_dup = Parceiro.objects.filter(consistente_cliente_id=item.consistente_cliente_id, nome=item.nome)
        if not parceiro_dup:
            item.save()
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, 'Registro não foi criado. Esse parceiro já existe.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/parceiro/list')
    form = AddParceiroForm()
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    template = loader.get_template('parceiro/add.html')
    context = {
        'title': 'Cadastro de Parceiros',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_parceiro': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_parceiro')
def edit_parceiro(request, parceiro_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            parceiro = Parceiro.objects.get(id=parceiro_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        parceiro = Parceiro.objects.get(id=parceiro_id)
    if request.POST:
        form = AddParceiroForm(request.POST, instance=parceiro)
        item = form.save(commit=False)
        item.assign_user = request.user
        parceiro_dup = Parceiro.objects.filter(consistente_cliente_id=item.consistente_cliente_id, nome=item.nome).exclude(id=parceiro.id)
        if not parceiro_dup:
            item.save()
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, 'Registro não foi alterado. Nome já existe em outro fornecedor.')
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/parceiro/list')
    form = AddParceiroForm(instance=parceiro)
    if not request.user.is_staff:
        form.fields['consistente_cliente'].widget = forms.HiddenInput()
    template = loader.get_template('parceiro/edit.html')
    context = {
        'title': 'Cadastro de Parceiros',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_register_parceiro': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.delete_parceiro')
def delete_parceiro(request, parceiro_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            parceiro = Parceiro.objects.get(id=parceiro_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        parceiro = Parceiro.objects.get(id=parceiro_id)
    if parceiro:
        try:
            parceiro.delete()
            messages.success(request, 'Parceiro apagado com sucesso!')
        except Exception as err:
            messages.error(request, 'Não é possível apagar o parceiro!')
            messages.error(request, err)
    else:
        messages.warning(request, 'Não é possível apagar esse parceiro. Favor, verifique o id.')
    path = request.GET.get('from', None)
    if path:
        return redirect(path)
    else:
        return redirect('/parceiro/list')


@login_required
@permission_required('manager.view_parceiro')
def list_parceiro(request):
    form = FindParceiroForm(request.GET)
    form.fields['consistente_cliente'].required = False
    form.fields['nome'].required = False
    form.fields['nomecompleto'].required = False
    form.fields['tipo'].required = False
    form.fields['doc'].required = False
    form.fields['endereco'].required = False
    filter_search = {}
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_search['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    for key, value in request.GET.items():
        if key in ['consistente_cliente'] and value:
            filter_search[key] = value
        if key in ['nome', 'nomecompleto', 'tipo', 'doc'] and value:
            filter_search['%s__icontains' % key] = value
    list_parceiro = Parceiro.objects.filter(**filter_search).order_by('nome')
    template = loader.get_template('parceiro/list.html')
    context = {
        'title': 'Cadastro de Parceiros',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_parceiro': list_parceiro,
        'form': form,
        'active_register_parceiro': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_diario')
def add_receber(request):
    if request.POST:
        form = AddDiarioForm(request.POST)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        del form.fields['parcelas']
        del form.fields['recorrencia']
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                crc_user = ConsistenteUsuario.objects.filter(user=request.user)
                if crc_user:
                    item.consistente_cliente = crc_user.first().consistente_cliente
            item.create_user = request.user
            item.assign_user = request.user
            item.tipomov = 0
            item.save()
            if int(request.POST['parcelas']) > 1:
                origin = dict(Diario.objects.filter(id=item.id).values()[0])
                if 'recorrencia' in request.POST and request.POST['recorrencia']:
                    pass
                else:
                    item.descricao += ' 1/%s' % request.POST['parcelas']
                    item.origin_transfer = item.id
                item.save()
                del origin['id']
                origin['datapago'] = None
                datavenc = origin['datavenc']
                datadoc = origin['datadoc']
                fatura = origin['fatura']
                for i in range(2, int(request.POST['parcelas']) + 1):
                    year = datavenc.year
                    month = datavenc.month + 1
                    day = origin['datavenc'].day
                    if month == 13:
                        year += 1
                        month = 1
                    if day > monthrange(year, month)[1]:
                        day = monthrange(year, month)[1]
                    datavenc = datavenc.replace(year=year, month=month, day=day)
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        year = datadoc.year
                        month = datadoc.month + 1
                        day = origin['datadoc'].day
                        if month == 13:
                            year += 1
                            month = 1
                        if day > monthrange(year, month)[1]:
                            day = monthrange(year, month)[1]
                        datadoc = datadoc.replace(year=year, month=month, day=day)
                    new_item = origin.copy()
                    new_item['datavenc'] = datavenc
                    if fatura:
                        new_item['fatura'] = str(datavenc)[:7]
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        new_item['datadoc'] = datadoc
                    else:
                        new_item['descricao'] += ' %s/%s' % (i, request.POST['parcelas'])
                        new_item['origin_transfer'] = item.id
                    resp = Diario.objects.create(**new_item)
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/receber/list')
    filter_customer = {}
    form = AddDiarioForm()
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 1]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 0
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['datadoc'].initial = str(date.today())
    form.fields['datavenc'].initial = str(date.today())
    template = loader.get_template('diario/receber/add.html')
    context = {
        'title': 'Contas à Receber',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_receber': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_diario')
def duplica_receber(request, diario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            receber = Diario.objects.get(id=diario_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        receber = Diario.objects.get(id=diario_id)
    if request.POST:
        form = AddDiarioForm(request.POST)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        del form.fields['parcelas']
        del form.fields['recorrencia']
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                crc_user = ConsistenteUsuario.objects.filter(user=request.user)
                if crc_user:
                    item.consistente_cliente = crc_user.first().consistente_cliente
            item.create_user = request.user
            item.assign_user = request.user
            item.tipomov = 0
            item.save()
            if int(request.POST['parcelas']) > 1:
                origin = dict(Diario.objects.filter(id=item.id).values()[0])
                if 'recorrencia' in request.POST and request.POST['recorrencia']:
                    pass
                else:
                    item.descricao += ' 1/%s' % request.POST['parcelas']
                    item.origin_transfer = item.id
                item.save()
                del origin['id']
                origin['datapago'] = None
                datavenc = origin['datavenc']
                datadoc = origin['datadoc']
                fatura = origin['fatura']
                for i in range(2, int(request.POST['parcelas']) + 1):
                    year = datavenc.year
                    month = datavenc.month + 1
                    day = origin['datavenc'].day
                    if month == 13:
                        year += 1
                        month = 1
                    if day > monthrange(year, month)[1]:
                        day = monthrange(year, month)[1]
                    datavenc = datavenc.replace(year=year, month=month, day=day)
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        year = datadoc.year
                        month = datadoc.month + 1
                        day = origin['datadoc'].day
                        if month == 13:
                            year += 1
                            month = 1
                        if day > monthrange(year, month)[1]:
                            day = monthrange(year, month)[1]
                        datadoc = datadoc.replace(year=year, month=month, day=day)
                    new_item = origin.copy()
                    new_item['datavenc'] = datavenc
                    if fatura:
                        new_item['fatura'] = str(datavenc)[:7]
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        new_item['datadoc'] = datadoc
                    else:
                        new_item['descricao'] += ' %s/%s' % (i, request.POST['parcelas'])
                        new_item['origin_transfer'] = item.id
                    resp = Diario.objects.create(**new_item)
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/receber/list')
    filter_customer = {}
    form = AddDiarioForm(instance=receber)
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 1]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 0
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    template = loader.get_template('diario/receber/duplica.html')
    context = {
        'title': 'Contas à Receber',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_receber': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.delete_diario')
def delete_receber(request, diario_id):
    diario = Diario.objects.filter(pk=diario_id, tipomov=0, datapago=None)
    if diario:
        # Verificar se tem múltiplos.
        if diario[0].origin_transfer:
            multiple = Diario.objects.filter(origin_transfer=diario[0].origin_transfer, tipomov=0, datapago=None)
            s = ''
            foi = 'i'
            qt = len(multiple)
            if qt > 1:
                s = 's'
                foi = 'ram'
            for item in multiple:
                consistente_cliente = item.consistente_cliente
                banco = item.banco
                tipomov = item.banco.tipomov
                diavenc = item.banco.diavenc
                datavenc = item.datavenc
                fatura = item.fatura
                item.delete()
            #multiple.delete()
            messages.success(request, 'Documento%s apagado%s com sucesso! Pagamento parcelado, fo%s apagado%s %s documento%s.' % (s, s, foi, s, qt, s))
        else:
            item = diario[0]
            consistente_cliente = item.consistente_cliente
            banco = item.banco
            tipomov = item.banco.tipomov
            diavenc = item.banco.diavenc
            datavenc = item.datavenc
            fatura = item.fatura
            item.delete()
            messages.success(request, 'Documento apagado com sucesso!')
    else:
        messages.warning(request, 'Não é possível apagar esse documento. Favor, verifique se está pago.')
    path = request.GET.get('from', None)
    if path:
        return redirect(path)
    else:
        return redirect('/receber/list')


@login_required
@permission_required('manager.change_diario')
def edit_receber(request, diario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            receber = Diario.objects.get(id=diario_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        receber = Diario.objects.get(id=diario_id)
    if request.POST:
        form = AddDiarioForm(request.POST, instance=receber)
        del form.fields['parcelas']
        del form.fields['recorrencia']
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            item.assign_user = request.user
            item.save()
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/receber/list')
    filter_customer = {}
    form = AddDiarioForm(instance=receber)
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 1]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 0
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    template = loader.get_template('diario/receber/edit.html')
    context = {
        'title': 'Contas à Receber',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_receber': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def list_receber(request):
    filter_customer = {}
    filter_search = {}
    if request.GET:
        form = FindDiarioForm(request.GET)
    else:
        form = FindDiarioForm()
        filter_search['datadoc__range'] = date.today().replace(day=1), date.today().replace(day=monthrange(date.today().year, date.today().month)[1])
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 1]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 0
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    filter_customer['tipomov'] = 0
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    for key, value in request.GET.items():
        if key in ['consistente_cliente', 'banco'] and value:
            filter_search[key] = value
        elif key in ['data_inicial', 'venc_inicial', 'pag_inicial'] and value:
            chave = {
                'data_inicial': 'datadoc',
                'venc_inicial': 'datavenc',
                'pag_inicial': 'datapago',
            }
            filter_search['%s__gte' % chave[key]] = value
        elif key in ['data_final', 'venc_final', 'pag_final'] and value:
            chave = {
                'data_final': 'datadoc',
                'venc_final': 'datavenc',
                'pag_final': 'datapago',
            }
            filter_search['%s__lte' % chave[key]] = value
        elif key in ['parceiro', 'categoria'] and value:
            value = request.GET.getlist(key)
            filter_search['%s_id__in' % key] = value
    list_receber = Diario.objects.filter(**filter_customer).filter(**filter_search).order_by('datadoc')
    try:
        soma = round(list_receber.aggregate(Sum('valor'))['valor__sum'], 2)
    except:
        soma = Decimal('0.00')
    template = loader.get_template('diario/receber/list.html')
    context = {
        'title': 'Contas à Receber',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_receber': list_receber,
        'hoje': date.today(),
        'form': form,
        'soma': soma,
        'active_diario': 'show',
        'active_diario_receber': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_diario')
def add_pagar(request):
    if request.GET and 'banco' in request.GET and request.GET['banco']:
        CHOICES = {'cartao': False}
        new_fat = ''
        new_venc = str(date.today())
        banco = Banco.objects.get(id=request.GET['banco'])
        CHOICES['fatura'] = ''
        if banco.tipomov == 2 and banco.diavenc:
            if 'fatura' in request.GET and request.GET['fatura']:
                # Busca somente vencimento
                date_ref = request.GET['fatura']
                new_fat = ''
                new_venc = ''
                date_ref = date_ref.split('-')
                if len(date_ref) == 2:
                    year = range(date.today().year - 10, date.today().year + 10)
                    month = range(1, 13)
                    if int(date_ref[0]) in year and int(date_ref[1]) in month:
                        # Corrigir se fatura acima do dia 28! Bug visto em 27/01/2020.
                        new_fat = '-'.join(date_ref)
                        new_venc = date(int(date_ref[0]), int(date_ref[1]), banco.diavenc).strftime('%Y-%m-%d')
            else:
                # Busca fatura e vencimento
                hoje = datetime.strptime(request.GET['datadoc'], '%Y-%m-%d') + timedelta(days=10)
                dia = hoje.day
                mes = hoje.month
                ano = hoje.year
                if banco.diavenc < dia:
                    mes = mes + 1
                    if mes == 13:
                        mes = 1
                        ano += 1
                new_fat = str(ano) + '-' + str(mes).zfill(2)
                new_venc = date(ano, mes, banco.diavenc).strftime('%Y-%m-%d')
            CHOICES['cartao'] = True
        CHOICES['fatura'] = new_fat
        CHOICES['datavenc'] = new_venc
        json_string = json.dumps(CHOICES)
        return HttpResponse(json_string)
    if request.POST:
        request_post = request.POST.copy()
        if not 'datavenc' in request_post:
            banco_venc = Banco.objects.get(id=request_post['banco'])
            request_post['datavenc'] = request_post['fatura'] + '-%s' % str(banco_venc.diavenc).zfill(2)
        form = AddDiarioForm(request_post)
        form.fields['datavenc'].widget.attrs['readonly'] = False
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                crc_user = ConsistenteUsuario.objects.filter(user=request.user)
                if crc_user:
                    item.consistente_cliente = crc_user.first().consistente_cliente
            # Rotina pra incluir valor em fatura de cartão de crédito
            if item.banco.tipomov == 2 and item.banco.diavenc and item.fatura:
                nomecartao = Diario.objects.filter(fatura=item.fatura, banco=item.banco, tipomov=3)
                if nomecartao and nomecartao[0].datapago:
                    messages.error(request, 'A fatura do cartão de crédito referente ao período informado já foi paga. Não é possível inserir esse pagamento.')
                    path = request.GET.get('next', None)
                    if path:
                        return redirect(path)
                    else:
                        return redirect('/pagar/list')
            ###
            item.create_user = request.user
            item.assign_user = request.user
            item.tipomov = 1
            item.save()
            # Rotina pra incluir valor em fatura de cartão de crédito
            if item.banco.tipomov == 2 and item.banco.diavenc and item.fatura:
                dados_cartao = {
                    'consistente_cliente': item.consistente_cliente, 
                    'user': request.user, 
                    'fatura': item.fatura, 
                    'banco': item.banco, 
                    'datavenc': item.datavenc,
                }
                atualiza_cartao(**dados_cartao)
            #########
            if int(request.POST['parcelas']) > 1:
                origin = dict(Diario.objects.filter(id=item.id).values()[0])
                if 'recorrencia' in request.POST and request.POST['recorrencia']:
                    pass
                else:
                    item.descricao += ' 1/%s' % request.POST['parcelas']
                    item.origin_transfer = item.id
                item.save()
                del origin['id']
                origin['datapago'] = None
                datavenc = origin['datavenc']
                datadoc = origin['datadoc']
                fatura = origin['fatura']
                for i in range(2, int(request.POST['parcelas']) + 1):
                    year = datavenc.year
                    month = datavenc.month + 1
                    day = origin['datavenc'].day
                    if month == 13:
                        year += 1
                        month = 1
                    if day > monthrange(year, month)[1]:
                        day = monthrange(year, month)[1]
                    datavenc = datavenc.replace(year=year, month=month, day=day)
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        year = datadoc.year
                        month = datadoc.month + 1
                        day = origin['datadoc'].day
                        if month == 13:
                            year += 1
                            month = 1
                        if day > monthrange(year, month)[1]:
                            day = monthrange(year, month)[1]
                        datadoc = datadoc.replace(year=year, month=month, day=day)
                    new_item = origin.copy()
                    new_item['datavenc'] = datavenc
                    if fatura:
                        new_item['fatura'] = str(datavenc)[:7]
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        new_item['datadoc'] = datadoc
                    else:
                        new_item['descricao'] += ' %s/%s' % (i, request.POST['parcelas'])
                        new_item['origin_transfer'] = item.id
                    resp = Diario.objects.create(**new_item)
                    # Rotina pra incluir valor em fatura de cartão de crédito
                    if resp.banco.tipomov == 2 and resp.banco.diavenc and resp.fatura:
                        dados_cartao = {
                            'consistente_cliente': resp.consistente_cliente, 
                            'user': request.user, 
                            'fatura': resp.fatura, 
                            'banco': resp.banco, 
                            'datavenc': resp.datavenc,
                        }
                        atualiza_cartao(**dados_cartao)
            messages.success(request, 'Registro adicionado com sucesso.')
            categoria = item.categoria
            year = item.datadoc.year
            month = item.datadoc.month
            selecao_data = item.datadoc.replace(day=1), item.datadoc.replace(day=monthrange(year, month)[1])
            soma_categoria = Diario.objects.filter(categoria=categoria, datadoc__range=selecao_data).aggregate(Sum('valor'))['valor__sum']
            if soma_categoria > categoria.limitemensal:
                messages.warning(request, 'Você estourou seu orçamento do mês na categoria %s.' % categoria.categoria)
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/pagar/list')
    filter_customer = {}
    form = AddDiarioForm()
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    #filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['datadoc'].initial = str(date.today())
    form.fields['datavenc'].initial = str(date.today())
    form.fields['fatura'].widget.attrs['disabled'] = True
    template = loader.get_template('diario/pagar/add.html')
    context = {
        'title': 'Contas à Pagar',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_pagar': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.delete_diario')
def delete_pagar(request, diario_id):
    diario = Diario.objects.filter(pk=diario_id, tipomov=1, datapago=None)
    if diario:
        # Verificar se tem múltiplos.
        if diario[0].origin_transfer:
            multiple = Diario.objects.filter(origin_transfer=diario[0].origin_transfer, tipomov=1, datapago=None)
            s = ''
            foi = 'i'
            qt = len(multiple)
            if qt > 1:
                s = 's'
                foi = 'ram'
            for item in multiple:
                consistente_cliente = item.consistente_cliente
                banco = item.banco
                tipomov = item.banco.tipomov
                diavenc = item.banco.diavenc
                datavenc = item.datavenc
                fatura = item.fatura
                item.delete()
                if tipomov == 2 and diavenc and fatura:
                    dados_cartao = {
                        'user': request.user,
                        'consistente_cliente': consistente_cliente, 
                        'fatura': fatura,
                        'banco': banco,
                        'datavenc': datavenc,
                    }
                    atualiza_cartao(**dados_cartao)
            #multiple.delete()
            messages.success(request, 'Documento%s apagado%s com sucesso! Pagamento parcelado, fo%s apagado%s %s documento%s.' % (s, s, foi, s, qt, s))
        else:
            item = diario[0]
            consistente_cliente = item.consistente_cliente
            banco = item.banco
            tipomov = item.banco.tipomov
            diavenc = item.banco.diavenc
            datavenc = item.datavenc
            fatura = item.fatura
            item.delete()
            if tipomov == 2 and diavenc and fatura:
                dados_cartao = {
                    'user': request.user,
                    'consistente_cliente': consistente_cliente, 
                    'fatura': fatura,
                    'banco': banco,
                    'datavenc': datavenc,
                }
                atualiza_cartao(**dados_cartao)
            #diario.delete()
            messages.success(request, 'Documento apagado com sucesso!')
    else:
        messages.warning(request, 'Não é possível apagar esse documento. Favor, verifique se está pago.')
    path = request.GET.get('from', None)
    if path:
        return redirect(path)
    else:
        return redirect('/pagar/list')


@login_required
@permission_required('manager.change_diario')
def edit_pagar(request, diario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            pagar = Diario.objects.get(id=diario_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        pagar = Diario.objects.get(id=diario_id)
    # Rotina pra alterar fatura de cartão de crédito em caso de alteração de banco.
    banco_antes = None
    if pagar.banco.tipomov == 2 and pagar.banco.diavenc and pagar.fatura:
        banco_antes = pagar.banco
        tipomov_antes = pagar.banco.tipomov
        diavenc_antes = pagar.banco.diavenc
        datavenc_antes = pagar.datavenc
        fatura_antes = pagar.fatura
    #########
    if request.POST:
        request_post = request.POST.copy()
        if not 'datavenc' in request_post:
            banco_venc = Banco.objects.get(id=request_post['banco'])
            request_post['datavenc'] = request_post['fatura'] + '-%s' % str(banco_venc.diavenc).zfill(2)
        form = AddDiarioForm(request_post, instance=pagar)
        del form.fields['parcelas']
        del form.fields['recorrencia']
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            item.assign_user = request.user
            item.save()
            # Rotina pra incluir valor em fatura de cartão de crédito
            if item.banco.tipomov == 2 and item.banco.diavenc and item.fatura:
                dados_cartao = {
                    'consistente_cliente': item.banco.consistente_cliente,
                    'user': request.user,
                    'fatura': item.fatura,
                    'banco': item.banco,
                    'datavenc': item.datavenc,
                }
                atualiza_cartao(**dados_cartao)
            if banco_antes:
                if banco_antes != item.banco or fatura_antes != item.fatura:
                    dados_cartao = {
                        'consistente_cliente': banco_antes.consistente_cliente,
                        'user': request.user,
                        'fatura': fatura_antes,
                        'banco': banco_antes,
                        'datavenc': datavenc_antes,
                    }
                    atualiza_cartao(**dados_cartao)
            #########
            messages.success(request, 'Registro alterado com sucesso.')
            categoria = item.categoria
            year = item.datadoc.year
            month = item.datadoc.month
            selecao_data = item.datadoc.replace(day=1), item.datadoc.replace(day=monthrange(year, month)[1])
            soma_categoria = Diario.objects.filter(categoria=categoria, datadoc__range=selecao_data).aggregate(Sum('valor'))['valor__sum']
            if soma_categoria > categoria.limitemensal:
                messages.warning(request, 'Você estourou seu orçamento do mês na categoria %s.' % categoria.categoria)
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/pagar/list')
    filter_customer = {}
    form = AddDiarioForm(instance=pagar)
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    #filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    voltar = False
    if pagar.fatura:
        form.fields['datavenc'].widget.attrs['disabled'] = True
        form.fields['datapago'].widget.attrs['disabled'] = True
        if pagar.banco.tipomov == 2 and pagar.datapago and pagar.fatura:
            messages.info(request, 'Pagamento já realizado. Não é possível fazer modificações.')
            form.fields['datadoc'].widget.attrs['disabled'] = True
            form.fields['parceiro'].widget.attrs['disabled'] = True
            form.fields['banco'].widget.attrs['disabled'] = True
            form.fields['fatura'].widget.attrs['disabled'] = True
            form.fields['categoria'].widget.attrs['disabled'] = True
            form.fields['descricao'].widget.attrs['disabled'] = True
            form.fields['valor'].widget.attrs['disabled'] = True
            voltar = True
    else:
        form.fields['fatura'].widget.attrs['disabled'] = True
    template = loader.get_template('diario/pagar/edit.html')
    context = {
        'title': 'Contas à Pagar',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'voltar': voltar,
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_pagar': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_diario')
def duplica_pagar(request, diario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            pagar = Diario.objects.get(id=diario_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        pagar = Diario.objects.get(id=diario_id)
    if request.POST:
        request_post = request.POST.copy()
        if not 'datavenc' in request_post:
            banco_venc = Banco.objects.get(id=request_post['banco'])
            request_post['datavenc'] = request_post['fatura'] + '-%s' % str(banco_venc.diavenc).zfill(2)
        form = AddDiarioForm(request_post)
        form.fields['datavenc'].widget.attrs['readonly'] = False
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            if not request.user.is_staff:
                crc_user = ConsistenteUsuario.objects.filter(user=request.user)
                if crc_user:
                    item.consistente_cliente = crc_user.first().consistente_cliente
            # Rotina pra incluir valor em fatura de cartão de crédito
            if item.banco.tipomov == 2 and item.banco.diavenc and item.fatura:
                nomecartao = Diario.objects.filter(fatura=item.fatura, banco=item.banco, tipomov=3)
                if nomecartao and nomecartao[0].datapago:
                    messages.error(request, 'A fatura do cartão de crédito referente ao período informado já foi paga. Não é possível inserir esse pagamento.')
                    path = request.GET.get('next', None)
                    if path:
                        return redirect(path)
                    else:
                        return redirect('/pagar/list')
            ###
            item.create_user = request.user
            item.assign_user = request.user
            item.tipomov = 1
            item.save()
            # Rotina pra incluir valor em fatura de cartão de crédito
            if item.banco.tipomov == 2 and item.banco.diavenc and item.fatura:
                dados_cartao = {
                    'consistente_cliente': item.consistente_cliente, 
                    'user': request.user, 
                    'fatura': item.fatura, 
                    'banco': item.banco, 
                    'datavenc': item.datavenc,
                }
                atualiza_cartao(**dados_cartao)
            #########
            if int(request.POST['parcelas']) > 1:
                origin = dict(Diario.objects.filter(id=item.id).values()[0])
                if 'recorrencia' in request.POST and request.POST['recorrencia']:
                    pass
                else:
                    item.descricao += ' 1/%s' % request.POST['parcelas']
                    item.origin_transfer = item.id
                item.save()
                del origin['id']
                origin['datapago'] = None
                datavenc = origin['datavenc']
                datadoc = origin['datadoc']
                fatura = origin['fatura']
                for i in range(2, int(request.POST['parcelas']) + 1):
                    year = datavenc.year
                    month = datavenc.month + 1
                    day = origin['datavenc'].day
                    if month == 13:
                        year += 1
                        month = 1
                    if day > monthrange(year, month)[1]:
                        day = monthrange(year, month)[1]
                    datavenc = datavenc.replace(year=year, month=month, day=day)
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        year = datadoc.year
                        month = datadoc.month + 1
                        day = origin['datadoc'].day
                        if month == 13:
                            year += 1
                            month = 1
                        if day > monthrange(year, month)[1]:
                            day = monthrange(year, month)[1]
                        datadoc = datadoc.replace(year=year, month=month, day=day)
                    new_item = origin.copy()
                    new_item['datavenc'] = datavenc
                    if fatura:
                        new_item['fatura'] = str(datavenc)[:7]
                    if 'recorrencia' in request.POST and request.POST['recorrencia']:
                        new_item['datadoc'] = datadoc
                    else:
                        new_item['descricao'] += ' %s/%s' % (i, request.POST['parcelas'])
                        new_item['origin_transfer'] = item.id
                    resp = Diario.objects.create(**new_item)
                    # Rotina pra incluir valor em fatura de cartão de crédito
                    if resp.banco.tipomov == 2 and resp.banco.diavenc and resp.fatura:
                        dados_cartao = {
                            'consistente_cliente': resp.consistente_cliente, 
                            'user': request.user, 
                            'fatura': resp.fatura, 
                            'banco': resp.banco, 
                            'datavenc': resp.datavenc,
                        }
                        atualiza_cartao(**dados_cartao)
            messages.success(request, 'Registro adicionado com sucesso.')
            categoria = item.categoria
            year = item.datadoc.year
            month = item.datadoc.month
            selecao_data = item.datadoc.replace(day=1), item.datadoc.replace(day=monthrange(year, month)[1])
            soma_categoria = Diario.objects.filter(categoria=categoria, datadoc__range=selecao_data).aggregate(Sum('valor'))['valor__sum']
            if soma_categoria > categoria.limitemensal:
                messages.warning(request, 'Você estourou seu orçamento do mês na categoria %s.' % categoria.categoria)
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/pagar/list')
    filter_customer = {}
    form = AddDiarioForm(instance=pagar)
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    #filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    voltar = False
    if pagar.fatura:
        form.fields['datavenc'].widget.attrs['disabled'] = True
        form.fields['datapago'].widget.attrs['disabled'] = True
    else:
        form.fields['fatura'].widget.attrs['disabled'] = True
    template = loader.get_template('diario/pagar/duplica.html')
    context = {
        'title': 'Contas à Pagar',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'voltar': voltar,
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_pagar': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def list_pagar(request):
    filter_customer = {}
    filter_search = {}
    if request.GET:
        form = FindDiarioForm(request.GET)
    else:
        form = FindDiarioForm()
        filter_search['datadoc__range'] = date.today().replace(day=1), date.today().replace(day=monthrange(date.today().year, date.today().month)[1])
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    #filter_banco['tipomov__in'] = [0, 1, 3]
    filter_customer['tipomov'] = 1
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    for key, value in request.GET.items():
        if key in ['consistente_cliente', 'banco'] and value:
            filter_search[key] = value
        elif key in ['data_inicial', 'venc_inicial', 'pag_inicial'] and value:
            chave = {
                'data_inicial': 'datadoc',
                'venc_inicial': 'datavenc',
                'pag_inicial': 'datapago',
            }
            filter_search['%s__gte' % chave[key]] = value
        elif key in ['data_final', 'venc_final', 'pag_final'] and value:
            chave = {
                'data_final': 'datadoc',
                'venc_final': 'datavenc',
                'pag_final': 'datapago',
            }
            filter_search['%s__lte' % chave[key]] = value
        elif key in ['parceiro', 'categoria'] and value:
            value = request.GET.getlist(key)
            filter_search['%s_id__in' % key] = value
    list_pagar = Diario.objects.filter(**filter_customer).filter(**filter_search)
    try:
        soma = round(list_pagar.aggregate(Sum('valor'))['valor__sum'], 2)
    except:
        soma = Decimal('0.00')
    template = loader.get_template('diario/pagar/list.html')
    context = {
        'title': 'Contas à Pagar',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_pagar': list_pagar,
        'hoje': date.today(),
        'form': form,
        'soma': soma,
        'active_diario': 'show',
        'active_diario_pagar': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_diario')
def add_transferir(request):
    if request.POST:
        form = TransfereDiarioForm(request.POST)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            try:
                item = form.save(commit=False)
                if not request.user.is_staff:
                    crc_user = ConsistenteUsuario.objects.filter(user=request.user)
                    if crc_user:
                        item.consistente_cliente = crc_user.first().consistente_cliente
                        parceiro = Parceiro.objects.filter(consistente_cliente=crc_user.first().consistente_cliente).order_by('id').first()
                        categoria = Categoria.objects.filter(consistente_cliente=crc_user.first().consistente_cliente, tipomov=2).order_by('id').first()
                else:
                    parceiro = Parceiro.objects.all().order_by('id').first()
                    categoria = Categoria.objects.filter(tipomov=2).order_by('id').first()
                item.parceiro = parceiro
                item.categoria = categoria
                item.create_user = request.user
                item.assign_user = request.user
                item.tipomov = 4
                item.save()
                salvo = Diario.objects.filter(id=item.id).values('consistente_cliente_id', 'datadoc', 'datavenc', 'datapago', 'descricao', 'valor', 'banco_id', 'categoria_id', 'parceiro_id', 'create_user_id', 'assign_user_id')
                new_item = salvo[0].copy()
                new_item['origin_transfer'] = item.id
                new_item['tipomov'] = 3
                new_item['banco_id'] = request.POST['banco_rec']
                Diario.objects.create(**new_item)
                messages.success(request, 'Registro adicionado com sucesso.')
            except Exception as err:
                messages.error(request, str(err))
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/transferir/list')
    filter_customer = {}
    form = TransfereDiarioForm()
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['banco_rec'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['datadoc'].initial = str(date.today())
    form.fields['datavenc'].initial = str(date.today())
    template = loader.get_template('diario/transferir/add.html')
    context = {
        'title': 'Transferências entre Contas',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_transferir': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_diario')
def edit_transferir(request, diario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            transferir = Diario.objects.get(id=diario_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        transferir = Diario.objects.get(id=diario_id)
    transferir_rec = Diario.objects.get(origin_transfer=diario_id)
    if request.POST:
        form = TransfereDiarioForm(request.POST, instance=transferir)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            item.assign_user = request.user
            item.save()
            transferir_rec.consistente_cliente_id = transferir.consistente_cliente_id
            transferir_rec.datadoc = request.POST['datadoc']
            transferir_rec.datavenc = request.POST['datavenc']
            if 'datapago' in request.POST and request.POST['datapago']:
                transferir_rec.datapago = request.POST['datapago']
            else:
                transferir_rec.datapago = None
            transferir_rec.descricao = request.POST['descricao']
            transferir_rec.valor = request.POST['valor']
            transferir_rec.assign_user_id = request.user
            transferir_rec.banco_id = request.POST['banco_rec']
            transferir_rec.save()
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/transferir/list')
    filter_customer = {}
    form = TransfereDiarioForm(instance=transferir)
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['banco_rec'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['banco_rec'].initial = transferir_rec.banco
    form.fields['datadoc'].initial = str(date.today())
    form.fields['datavenc'].initial = str(date.today())
    template = loader.get_template('diario/transferir/edit.html')
    context = {
        'title': 'Transferências entre Contas',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_transferir': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def list_transferir(request):
    filter_customer = {}
    filter_search = {}
    if request.GET:
        form = FindDiarioForm(request.GET)
    else:
        form = FindDiarioForm()
        filter_search['datadoc__range'] = date.today().replace(day=1), date.today().replace(day=monthrange(date.today().year, date.today().month)[1])
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    filter_customer['tipomov__in'] = [4]
    filter_customer['banco__tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].widget = forms.HiddenInput()
    form.fields['categoria'].widget = forms.HiddenInput()
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    for key, value in request.GET.items():
        if key in ['consistente_cliente', 'banco'] and value:
            filter_search[key] = value
        elif key in ['data_inicial', 'venc_inicial', 'pag_inicial'] and value:
            chave = {
                'data_inicial': 'datadoc',
                'venc_inicial': 'datavenc',
                'pag_inicial': 'datapago',
            }
            filter_search['%s__gte' % chave[key]] = value
        elif key in ['data_final', 'venc_final', 'pag_final'] and value:
            chave = {
                'data_final': 'datadoc',
                'venc_final': 'datavenc',
                'pag_final': 'datapago',
            }
            filter_search['%s__lte' % chave[key]] = value
        elif key in ['parceiro', 'categoria'] and value:
            value = request.GET.getlist(key)
            filter_search['%s_id__in' % key] = value
    list_transfere = Diario.objects.filter(**filter_customer).filter(**filter_search).exclude(descricao='<CRED.CARD>').order_by('datadoc')
    try:
        soma = round(list_transfere.aggregate(Sum('valor'))['valor__sum'], 2)
    except:
        soma = Decimal('0.00')
    list_transferir = []
    for item in list_transfere:
        new_item = {
            'id': item.id,
            'datadoc': item.datadoc,
            'banco': item.banco,
            'banco_rec': Diario.objects.get(origin_transfer=item.id, tipomov=3).banco,
            'descricao': item.descricao,
            'valor': item.valor,
            'datavenc': item.datavenc,
            'datapago': item.datapago,
        }
        list_transferir.append(new_item)
    template = loader.get_template('diario/transferir/list.html')
    context = {
        'title': 'Transferências entre Contas',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_transferir': list_transferir,
        'form': form,
        'soma': soma,
        'active_diario': 'show',
        'active_diario_transferir': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_diario')
def edit_cartoes(request, diario_id):
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            cartoes = Diario.objects.get(id=diario_id, consistente_cliente_id=crc_user.first().consistente_cliente_id)
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    else:
        cartoes = Diario.objects.get(id=diario_id)
    cartoes_rec = Diario.objects.get(origin_transfer=diario_id)
    if request.POST:
        form = TransfereDiarioForm(request.POST, instance=cartoes)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        del form.fields['datadoc']
        del form.fields['descricao']
        del form.fields['valor']
        del form.fields['datavenc']
        del form.fields['banco_rec']
        if form.is_valid():
            item = form.save(commit=False)
            item.assign_user = request.user
            item.save()
            if 'datapago' in request.POST and request.POST['datapago']:
                cartoes_rec.datapago = request.POST['datapago']
            else:
                cartoes_rec.datapago = None
            cartoes_rec.assign_user_id = request.user
            cartoes_rec.save()
            cartoes_pago = Diario.objects.get(id=diario_id)
            cartoes_pago.datapago = cartoes_rec.datapago
            cartoes_pago.save()
            pagar = Diario.objects.filter(fatura=cartoes_rec.fatura, banco=cartoes_rec.banco, tipomov=1).update(datapago=cartoes_rec.datapago)
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, form.errors)
        path = request.GET.get('next', None)
        if path:
            return redirect(path)
        else:
            return redirect('/cartoes/list')
    filter_customer = {}
    form = TransfereDiarioForm(instance=cartoes)
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            form.fields['consistente_cliente'].widget = forms.HiddenInput()
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_parceiro = filter_customer.copy()
    filter_parceiro['modo__in'] = [0, 2]
    filter_categoria = filter_customer.copy()
    filter_categoria['tipomov'] = 1
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    filter_banco['tipomov__in'] = [2]
    form.fields['banco_rec'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['banco_rec'].initial = cartoes_rec.banco
    form.fields['banco_rec'].label = 'Cartão de Crédito'
    form.fields['banco_rec'].widget.attrs['disabled'] = True
    form.fields['datadoc'].initial = str(date.today())
    form.fields['datadoc'].widget.attrs['disabled'] = True
    form.fields['datavenc'].initial = str(date.today())
    form.fields['datavenc'].widget.attrs['disabled'] = True
    form.fields['valor'].widget.attrs['disabled'] = True
    template = loader.get_template('diario/cartoes/edit.html')
    context = {
        'title': 'Cartões de Crédito',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'from': request.GET.get('from', None),
        'form': form,
        'active_diario': 'show',
        'active_diario_cartoes': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def list_cartoes(request):
    filter_customer = {}
    filter_search = {}
    if request.GET:
        form = FindDiarioForm(request.GET)
    else:
        form = FindDiarioForm()
        filter_search['datadoc__range'] = date.today().replace(day=1), date.today().replace(day=monthrange(date.today().year, date.today().month)[1])
    crc_user = None
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    filter_banco = filter_customer.copy()
    filter_banco['tipomov__in'] = [0, 1, 3]
    filter_customer['tipomov__in'] = [4]
    filter_customer['banco__tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].widget = forms.HiddenInput()
    form.fields['categoria'].widget = forms.HiddenInput()
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    filter_banco['tipomov__in'] = [2]
    form.fields['banco_rec'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    for key, value in request.GET.items():
        if key in ['consistente_cliente', 'banco'] and value:
            filter_search[key] = value
        elif key in ['data_inicial', 'venc_inicial', 'pag_inicial'] and value:
            chave = {
                'data_inicial': 'datadoc',
                'venc_inicial': 'datavenc',
                'pag_inicial': 'datapago',
            }
            filter_search['%s__gte' % chave[key]] = value
        elif key in ['data_final', 'venc_final', 'pag_final'] and value:
            chave = {
                'data_final': 'datadoc',
                'venc_final': 'datavenc',
                'pag_final': 'datapago',
            }
            filter_search['%s__lte' % chave[key]] = value
        elif key in ['parceiro', 'categoria'] and value:
            value = request.GET.getlist(key)
            filter_search['%s_id__in' % key] = value
        if key in ['banco_rec'] and value:
            filter_cartao = filter_search.copy()
            if crc_user:
                filter_cartao['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
            filter_cartao['tipomov__in'] = [3]
            filter_cartao['banco_id'] = value
            cartao = [x.origin_transfer for x in Diario.objects.filter(**filter_cartao).filter(descricao='<CRED.CARD>').order_by('datadoc')]
            filter_search['id__in'] = cartao
    list_transfere = Diario.objects.filter(**filter_customer).filter(**filter_search).filter(descricao='<CRED.CARD>').order_by('datadoc')
    try:
        soma = round(list_transfere.aggregate(Sum('valor'))['valor__sum'], 2)
    except:
        soma = Decimal('0.00')
    list_cartoes = []
    for item in list_transfere:
        new_item = {
            'id': item.id,
            'datadoc': item.datadoc,
            'banco': item.banco,
            'banco_rec': Diario.objects.get(origin_transfer=item.id, tipomov=3).banco,
            'descricao': item.descricao,
            'valor': item.valor,
            'datavenc': item.datavenc,
            'datapago': item.datapago,
        }
        list_cartoes.append(new_item)
    template = loader.get_template('diario/cartoes/list.html')
    context = {
        'title': 'Cartões de Crédito',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'list_cartoes': list_cartoes,
        'form': form,
        'soma': soma,
        'active_diario': 'show',
        'active_diario_cartoes': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def fluxo_caixa(request):
    filter_customer = {}
    filter_search = {}
    filter_initial = {}
    list_diario = []
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    if request.GET:
        form = FluxoCaixaForm(request.GET)
        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        for key, value in request.GET.items():
            if key in ['consistente_cliente', 'banco'] and value:
                filter_search[key] = value
                filter_initial[key] = value
            elif key in ['venc_inicial', 'pag_inicial'] and value:
                chave = {
                    'venc_inicial': 'datavenc',
                    'pag_inicial': 'datapago',
                }
                filter_search['%s__gte' % chave[key]] = value
                filter_initial['%s__lt' % chave[key]] = value
            elif key in ['data_final', 'venc_final', 'pag_final'] and value:
                chave = {
                    'venc_final': 'datavenc',
                    'pag_final': 'datapago',
                }
                filter_search['%s__lte' % chave[key]] = value
        if not 'banco' in filter_search:
            filter_search['banco__tipomov__in'] = [0, 1]
            filter_initial['banco__tipomov__in'] = [0, 1]
        filter_initial['tipomov__in'] = [0, 3]
        soma_entradas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        filter_initial['tipomov__in'] = [1, 4]
        soma_saidas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        if soma_entradas:
            soma_entradas = soma_entradas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_entradas = Decimal('0.00')
        if soma_saidas:
            soma_saidas = soma_saidas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_saidas = Decimal('0.00')
        saldo_inicial = soma_entradas - soma_saidas
        saldo_inicial = round(saldo_inicial, 2)
        new_item = {
            'banco': '',
            'parceiro': '',
            'categoria': '',
            'valor_entra': '',
            'valor_sai': '',
            'valor_saldo': saldo_inicial,
            'datavenc': '',
            'datapago': '',
        }
        list_diario.append(new_item)
        saldo_atual = saldo_inicial
        soma_entradas = Decimal('0.0')
        soma_saidas = Decimal('0.0')
        diario = Diario.objects.filter(**filter_customer).filter(**filter_search).exclude(datapago=None).order_by('datapago', 'datavenc')
        for i in diario:
            valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor 
            valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor
            soma_entradas += valor_entra
            soma_saidas += valor_sai
            saldo_atual = saldo_atual + valor_entra - valor_sai
            nomecartao = None
            if i.tipomov == 4:
                nomecartao = Diario.objects.filter(origin_transfer=i.id).first().banco.nomebanco
            if i.tipomov == 3:
                nomecartao = Diario.objects.filter(id=i.origin_transfer).first().banco.nomebanco
            new_item = {
                'id': i.id,
                'banco': i.banco,
                'parceiro': i.parceiro if not nomecartao else nomecartao,
                'categoria': i.categoria if not i.descricao == '<CRED.CARD>' else 'Cartão de Crédito',
                'valor_entra': valor_entra if valor_entra else '',
                'valor_sai': valor_sai if valor_sai else '',
                'valor_saldo': saldo_atual,
                'datavenc': i.datavenc,
                'datapago': i.datapago,
            }
            if 'somente_aberto' in request.GET and request.GET['somente_aberto']:
                continue
            list_diario.append(new_item)
        if 'somente_aberto' in request.GET and request.GET['somente_aberto']:
            list_diario[0]['valor_saldo'] = saldo_atual
        diario = Diario.objects.filter(**filter_customer).filter(**filter_search).filter(datapago=None).order_by('datapago', 'datavenc')
        for i in diario:
            valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor 
            valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor
            soma_entradas += valor_entra
            soma_saidas += valor_sai
            saldo_atual = saldo_atual + valor_entra - valor_sai
            if i.tipomov == 4 and i.descricao == '<CRED.CARD>':
                nomecartao = Diario.objects.filter(origin_transfer=i.id).first().banco.nomebanco
            if i.tipomov == 3 and i.descricao == '<CRED.CARD>':
                nomecartao = Diario.objects.filter(id=i.origin_transfer).first().banco.nomebanco
            new_item = {
                'id': i.id,
                'banco': i.banco,
                'parceiro': i.parceiro if not i.descricao == '<CRED.CARD>' else nomecartao,
                'categoria': i.categoria if not i.descricao == '<CRED.CARD>' else 'Cartão de Crédito',
                'valor_entra': valor_entra if valor_entra else '',
                'valor_sai': valor_sai if valor_sai else '',
                'valor_saldo': saldo_atual,
                'datavenc': i.datavenc,
                'datapago': i.datapago,
            }
            list_diario.append(new_item)
    else:
        form = FluxoCaixaForm()
        form.fields['venc_inicial'].initial = str(date.today().replace(day=1))
        form.fields['venc_final'].initial = str(date.today().replace(day=monthrange(date.today().year, date.today().month)[1]))
        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        soma_entradas = Decimal('0.00')
        soma_saidas = Decimal('0.00')
        saldo_atual = Decimal('0.00')
    template = loader.get_template('relatorios/caixa.html')
    context = {
        'title': 'Fluxo de Caixa - Extrato de Movimento',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'hoje': date.today(),
        'list_diario': list_diario,
        'form': form,
        'soma_entradas': soma_entradas,
        'soma_saidas': soma_saidas,
        'confronto': soma_entradas - soma_saidas,
        'saldo_fim': saldo_atual,
        'active_relatorios': 'show',
        'active_relatorios_caixa': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.change_diario')
def pagar_fluxo_caixa(request, diario_id):
    diario = Diario.objects.filter(pk=diario_id, datapago=None)
    if diario:
        if diario[0].tipomov in [0, 1] and diario[0].banco.tipomov != 2:
            diario.update(datapago=date.today())
            messages.success(request, 'Pagamento confirmado com sucesso!')
        elif diario[0].tipomov in [0, 1] and diario[0].banco.tipomov == 2:
            messages.error(request, 'Não é possível fazer pagamento individual de compra realizada em cartão de crédito. Realize o pagamento do cartão.')
        elif diario[0].tipomov == 3 and diario[0].banco.tipomov == 2:
            nomecartao = Diario.objects.filter(id=diario[0].origin_transfer, tipomov=4)
            pagar = Diario.objects.filter(fatura=diario[0].fatura, banco=diario[0].banco, tipomov=1).update(datapago=date.today())
            nomecartao.update(datapago=date.today())
            diario.update(datapago=date.today())
            messages.success(request, 'Pagamento confirmado com sucesso!')
        elif diario[0].tipomov == 4 and diario[0].descricao == '<CRED.CARD>':
            nomecartao = Diario.objects.filter(origin_transfer=diario[0].id, tipomov=3)
            pagar = Diario.objects.filter(fatura=nomecartao[0].fatura, banco=nomecartao[0].banco, tipomov=1).update(datapago=date.today())
            nomecartao.update(datapago=date.today())
            diario.update(datapago=date.today())
            messages.success(request, 'Pagamento confirmado com sucesso!')
        elif diario[0].tipomov == 3 and diario[0].banco.tipomov != 2:
            transf = Diario.objects.filter(id=diario[0].origin_transfer, tipomov=4)
            transf.update(datapago=date.today())
            diario.update(datapago=date.today())
        elif diario[0].tipomov == 4 and diario[0].descricao != '<CRED.CARD>':
            transf = Diario.objects.filter(origin_transfer=diario[0].id, tipomov=3)
            transf.update(datapago=date.today())
            diario.update(datapago=date.today())
    else:
        messages.warning(request, 'Não é possível confirmar esse documento. Favor, verifique se está pago.')
    path = request.GET.get('from', None)
    if path:
        return redirect(path)
    else:
        return redirect('/pagar/list')


@login_required
@permission_required('manager.view_diario')
def resumo_diario(request):
    filter_customer = {}
    filter_search = {}
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    form = ResumoForm()
    form.fields['data_inicial'].label = 'Mês analisado'
    if request.GET:
        request_get = request.GET.copy()
        form = ResumoForm()
        if 'data_inicial' in request_get:
            form.fields['data_inicial'].initial = request_get['data_inicial']
        if 'categoria' in request_get:
            form.fields['categoria'].initial = request_get.getlist('categoria')
        filter_categoria = filter_customer.copy()
        filter_categoria['tipomov'] = 1
        filter_categoria['classifica'] = True
        form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
        for key, value in request.GET.items():
            if key in ['consistente_cliente'] and value:
                filter_search[key] = value
            elif key in ['categoria'] and value:
                filter_search[key + '__in'] = request.GET.getlist(key)
            elif key in ['data_inicial'] and value:
                chave = {
                    'data_inicial': 'datadoc',
                }
                periodo = value.split('-')
                ano = int(periodo[0])
                mes = int(periodo[1])
                filter_search['%s__range' % chave[key]] = [value + '-01', value + '-%s' % monthrange(ano, mes)[1]]
    else:
        form.fields['data_inicial'].initial = date.today().replace(day=1).strftime('%Y-%m')
        filter_search['datadoc__range'] = [date.today().replace(day=1), date.today().replace(day=monthrange(date.today().year, date.today().month)[1])]
        filter_categoria = filter_customer.copy()
        filter_categoria['tipomov'] = 1
        filter_categoria['classifica'] = True
        form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    filter_search['categoria__classifica'] = True
    filter_search['tipomov__in'] = [1, 4]
    if 'categoria' in filter_search:
        filter_categoria['id'] = filter_search['categoria']
    if 'categoria__in' in filter_search:
        filter_categoria['id__in'] = filter_search['categoria__in']
    limites = Categoria.objects.filter(**filter_categoria).aggregate(Sum('limitemensal'))
    saldo = Decimal('0.00')
    if limites['limitemensal__sum']:
        saldo = round(limites['limitemensal__sum'], 2)
    limite = saldo
    list_diario = []
    diario = Diario.objects.annotate(data=TruncDay('datadoc')).filter(**filter_customer).filter(**filter_search).values('data').annotate(valor=Sum('valor')).order_by('data')
    acumulado = Decimal('0.00')
    for i in diario:
        new_item = i.copy()
        new_item['valor'] = round(new_item['valor'], 2)
        acumulado += round(new_item['valor'], 2)
        saldo -= round(new_item['valor'], 2)
        new_item['valor_acum'] = acumulado
        new_item['valor_disp'] = saldo
        list_diario.append(new_item)
    template = loader.get_template('relatorios/diario.html')
    context = {
        'title': 'Relatório - Diário de Compras',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'hoje': date.today(),
        'list_diario': list_diario,
        'limite': limite,
        'acumulado': acumulado,
        'saldo': saldo,
        'form': form,
        'active_relatorios': 'show',
        'active_relatorios_diario': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def resumo_pagamentos(request):
    filter_customer = {}
    filter_search = {}
    filter_initial = {}
    soma_meses = {}
    list_diario = []
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    if request.GET:
        request_get = request.GET.copy()
        form = ResumoForm()
        form.fields['data_inicial'].initial = request_get['data_inicial']
        form.fields['data_final'].initial = request_get['data_final']
        form.fields['banco'].initial = request_get['banco']
        orcado = False
        if 'orcado' in request_get:
            form.fields['orcado'].initial = request_get['orcado']
            orcado = True
            valor_orcado = Categoria.objects.filter(limitemensal__gt=Decimal('0.0'))


        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        somente_efetuados = False
        datadoc = 'datavenc'
        if 'efetuados' in request.GET and request.GET['efetuados']:
            form.fields['efetuados'].initial = request_get['efetuados']
            somente_efetuados = True
            datadoc = 'datapago'
        for key, value in request.GET.items():
            if key in ['consistente_cliente', 'banco'] and value:
                filter_search[key] = value
                filter_initial[key] = value
            elif key in ['data_inicial', 'venc_inicial', 'pag_inicial'] and value:
                chave = {
                    'data_inicial': datadoc,
                    'pag_inicial': 'datapago',
                }
                filter_search['%s__gte' % chave[key]] = value + '-01'
                filter_initial['%s__lt' % chave[key]] = value + '-01'
            elif key in ['data_final', 'venc_final', 'pag_final'] and value:
                chave = {
                    'data_final': datadoc,
                    'pag_final': 'datapago',
                }
                periodo = value.split('-')
                ano = int(periodo[0])
                mes = int(periodo[1])
                filter_search['%s__lte' % chave[key]] = value + '-%s' % monthrange(ano, mes)[1]
        filter_initial['tipomov__in'] = [0, 3]
        soma_entradas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        filter_initial['tipomov__in'] = [1, 4]
        soma_saidas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        if soma_entradas:
            soma_entradas = soma_entradas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_entradas = Decimal('0.00')
        if soma_saidas:
            soma_saidas = soma_saidas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_saidas = Decimal('0.00')
        saldo_inicial = soma_entradas - soma_saidas
        saldo_inicial = round(saldo_inicial, 2)
        new_item = {
            'banco': '',
            'parceiro': '',
            'categoria': '',
            'valor_entra': '',
            'valor_sai': '',
            'valor_saldo': saldo_inicial,
            'datavenc': '',
            'datapago': '',
        }
        #list_diario.append(new_item)
        saldo_atual = saldo_inicial
        soma_entradas = Decimal('0.0')
        soma_saidas = Decimal('0.0')
        filter_search['tipomov__in'] = [1, 4]
        filter_search['categoria__classifica'] = True
        if orcado:
            meses = {}
            data_atual = datetime.strptime(request_get['data_inicial'], '%Y-%m')
            while data_atual <= datetime.strptime(request_get['data_final'], '%Y-%m'):
                if data_atual.day == 1:
                    meses[data_atual.strftime('%Y-%m')] = Decimal('0.00')
                data_atual += timedelta(days=1) # Adiciona um dia à data atual
            soma_meses = meses.copy()
        else:
            meses = Diario.objects.filter(**filter_customer).filter(**filter_search).annotate(mes=TruncMonth(datadoc)).values('mes').annotate(Sum('valor')).order_by('mes')
            meses = {str(x['mes'])[:7]: Decimal('0.00') for x in meses}
            soma_meses = meses.copy()
        diario = Diario.objects.filter(**filter_customer).filter(**filter_search).annotate(mes=TruncMonth(datadoc)).values_list('categoria__categoria', 'mes').annotate(Sum('valor')).order_by('categoria__categoria', 'mes')
        new_item = {'categoria': ''}
        primeiro = True
        for i in diario:
            #valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor 
            #valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor
            #soma_entradas += valor_entra
            #soma_saidas += valor_sai
            #saldo_atual = saldo_atual + valor_entra - valor_sai
            #if i.tipomov == 4 and i.descricao == '<CRED.CARD>':
            #    nomecartao = Diario.objects.filter(origin_transfer=i.id).first().banco.nomebanco
            #if i.tipomov == 3 and i.descricao == '<CRED.CARD>':
            #    nomecartao = Diario.objects.filter(id=i.origin_transfer).first().banco.nomebanco
            if i[0] != new_item['categoria']:
                if not primeiro:
                    list_diario.append(new_item)
                else:
                    primeiro = False
                new_item = {
                    'categoria': i[0],
                    'meses': meses.copy()
                }
            soma_meses[str(i[1])[:7]] += round(i[2], 2)
            new_item['meses'][str(i[1])[:7]] = round(i[2], 2)
        list_diario.append(new_item)
        for i in list_diario:
            categ = i['categoria']
            if 'meses' in i:
                for mes in i['meses']:
                    valor_mes = i['meses'][mes]
                    if orcado and date.today().replace(day=1) <= datetime.strptime(mes, '%Y-%m').date() and valor_orcado.filter(categoria=categ):
                        if valor_orcado.filter(categoria=categ)[0].limitemensal > valor_mes:
                            i['meses'][mes] = valor_orcado.filter(categoria=categ)[0].limitemensal
                            soma_meses[mes] += valor_orcado.filter(categoria=categ)[0].limitemensal
    else:
        form = ResumoForm()
        form.fields['data_inicial'].initial = date.today().replace(month=1, day=1).strftime('%Y-%m')
        form.fields['data_final'].initial = date.today().replace(month=12, day=1).strftime('%Y-%m')
        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        meses = []
        for i in range(1, 13):
            meses.append(str(date.today().replace(day=1).replace(month=i))[:7])
        soma_entradas = Decimal('0.00')
        soma_saidas = Decimal('0.00')
        saldo_atual = Decimal('0.00')
    template = loader.get_template('relatorios/categoria.html')
    context = {
        'title': 'Demonstrativo - Pagamentos por Categoria',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'hoje': date.today(),
        'list_diario': list_diario,
        'form': form,
        'meses': '","'.join([str(x)[:7] for x in meses]),
        'lista_mes': [str(x)[:7] for x in meses],
        'soma_meses': soma_meses,
        'somente_efetuados': True,
        'active_relatorios': 'show',
        'active_relatorios_pagamentos': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def resumo_categoria(request):
    filter_customer = {}
    filter_search = {}
    filter_initial = {}
    soma_meses = {}
    list_diario = []
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    if request.GET:
        request_get = request.GET.copy()
        form = ResumoForm()
        form.fields['data_inicial'].initial = request_get['data_inicial']
        form.fields['data_final'].initial = request_get['data_final']
        form.fields['banco'].initial = request_get['banco']
        orcado = False
        if 'orcado' in request_get:
            form.fields['orcado'].initial = request_get['orcado']
            orcado = True
            valor_orcado = Categoria.objects.filter(limitemensal__gt=Decimal('0.0'))

        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        for key, value in request.GET.items():
            if key in ['consistente_cliente', 'banco'] and value:
                filter_search[key] = value
                filter_initial[key] = value
            elif key in ['data_inicial', 'pag_inicial'] and value:
                chave = {
                    'data_inicial': 'datadoc',
                    'pag_inicial': 'datapago',
                }
                filter_search['%s__gte' % chave[key]] = value + '-01'
                filter_initial['%s__lt' % chave[key]] = value + '-01'
            elif key in ['data_final', 'venc_final', 'pag_final'] and value:
                chave = {
                    'data_final': 'datadoc',
                    'pag_final': 'datapago',
                }
                periodo = value.split('-')
                ano = int(periodo[0])
                mes = int(periodo[1])
                filter_search['%s__lte' % chave[key]] = value + '-%s' % monthrange(ano, mes)[1]
        filter_initial['tipomov__in'] = [0, 3]
        soma_entradas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        filter_initial['tipomov__in'] = [1, 4]
        soma_saidas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        if soma_entradas:
            soma_entradas = soma_entradas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_entradas = Decimal('0.00')
        if soma_saidas:
            soma_saidas = soma_saidas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_saidas = Decimal('0.00')
        saldo_inicial = soma_entradas - soma_saidas
        saldo_inicial = round(saldo_inicial, 2)
        new_item = {
            'banco': '',
            'parceiro': '',
            'categoria': '',
            'valor_entra': '',
            'valor_sai': '',
            'valor_saldo': saldo_inicial,
            'datavenc': '',
            'datapago': '',
        }
        #list_diario.append(new_item)
        saldo_atual = saldo_inicial
        soma_entradas = Decimal('0.0')
        soma_saidas = Decimal('0.0')
        filter_search['tipomov__in'] = [1, 4]
        filter_search['categoria__classifica'] = True
        if orcado:
            meses = {}
            data_atual = datetime.strptime(request_get['data_inicial'], '%Y-%m')
            while data_atual <= datetime.strptime(request_get['data_final'], '%Y-%m'):
                if data_atual.day == 1:
                    meses[data_atual.strftime('%Y-%m')] = Decimal('0.00')
                data_atual += timedelta(days=1) # Adiciona um dia à data atual
            soma_meses = meses.copy()
        else:
            meses = Diario.objects.filter(**filter_customer).filter(**filter_search).annotate(mes=TruncMonth('datadoc')).values('mes').annotate(Sum('valor')).order_by('mes')
            meses = {str(x['mes'])[:7]: Decimal('0.00') for x in meses}
            soma_meses = meses.copy()
        diario = Diario.objects.filter(**filter_customer).filter(**filter_search).annotate(mes=TruncMonth('datadoc')).values_list('categoria__categoria', 'mes').annotate(Sum('valor')).order_by('categoria__categoria', 'mes')
        new_item = {'categoria': ''}
        primeiro = True
        for i in diario:
            #valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor 
            #valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor
            #soma_entradas += valor_entra
            #soma_saidas += valor_sai
            #saldo_atual = saldo_atual + valor_entra - valor_sai
            #if i.tipomov == 4 and i.descricao == '<CRED.CARD>':
            #    nomecartao = Diario.objects.filter(origin_transfer=i.id).first().banco.nomebanco
            #if i.tipomov == 3 and i.descricao == '<CRED.CARD>':
            #    nomecartao = Diario.objects.filter(id=i.origin_transfer).first().banco.nomebanco
            if i[0] != new_item['categoria']:
                if not primeiro:
                    list_diario.append(new_item)
                else:
                    primeiro = False
                new_item = {
                    'categoria': i[0],
                    'meses': meses.copy()
                }
            soma_meses[str(i[1])[:7]] += round(i[2], 2)
            new_item['meses'][str(i[1])[:7]] = round(i[2], 2)
        list_diario.append(new_item)
        for i in list_diario:
            categ = i['categoria']
            if 'meses' in i:
                for mes in i['meses']:
                    valor_mes = i['meses'][mes]
                    if orcado and date.today().replace(day=1) <= datetime.strptime(mes, '%Y-%m').date() and valor_orcado.filter(categoria=categ):
                        if valor_orcado.filter(categoria=categ)[0].limitemensal > valor_mes:
                            i['meses'][mes] = valor_orcado.filter(categoria=categ)[0].limitemensal
                            soma_meses[mes] += valor_orcado.filter(categoria=categ)[0].limitemensal
    else:
        form = ResumoForm()
        form.fields['data_inicial'].initial = date.today().replace(month=1, day=1).strftime('%Y-%m')
        form.fields['data_final'].initial = date.today().replace(month=12, day=1).strftime('%Y-%m')
        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        meses = []
        for i in range(1, 13):
            meses.append(str(date.today().replace(day=1).replace(month=i))[:7])
        soma_entradas = Decimal('0.00')
        soma_saidas = Decimal('0.00')
        saldo_atual = Decimal('0.00')
    template = loader.get_template('relatorios/categoria.html')
    context = {
        'title': 'Demonstrativo - Despesas por Categoria',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'hoje': date.today(),
        'list_diario': list_diario,
        'form': form,
        'meses': '","'.join([str(x)[:7] for x in meses]),
        'lista_mes': [str(x)[:7] for x in meses],
        'soma_meses': soma_meses,
        'active_relatorios': 'show',
        'active_relatorios_categoria': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.view_diario')
def resumo_parceiro(request):
    filter_customer = {}
    filter_search = {}
    filter_initial = {}
    list_diario = []
    if not request.user.is_staff:
        crc_user = ConsistenteUsuario.objects.filter(user=request.user)
        if crc_user:
            filter_customer['consistente_cliente_id'] = crc_user.first().consistente_cliente_id
        else:
            messages.warning(request, 'Seu usuário não está vinculado a nenhuma conta Consistente.')
            return redirect('/')
    if request.GET:
        request_get = request.GET.copy()
        form = ResumoForm()
        form.fields['data_inicial'].initial = request_get['data_inicial']
        form.fields['data_final'].initial = request_get['data_final']
        form.fields['banco'].initial = request_get['banco']

        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        for key, value in request.GET.items():
            if key in ['consistente_cliente', 'banco'] and value:
                filter_search[key] = value
                filter_initial[key] = value
            elif key in ['data_inicial', 'pag_inicial'] and value:
                chave = {
                    'data_inicial': 'datadoc',
                    'pag_inicial': 'datapago',
                }
                filter_search['%s__gte' % chave[key]] = value + '-01'
                filter_initial['%s__lt' % chave[key]] = value + '-01'
            elif key in ['data_final', 'venc_final', 'pag_final'] and value:
                chave = {
                    'data_final': 'datadoc',
                    'pag_final': 'datapago',
                }
                periodo = value.split('-')
                ano = int(periodo[0])
                mes = int(periodo[1])
                filter_search['%s__lte' % chave[key]] = value + '-%s' % monthrange(ano, mes)[1]
        filter_initial['tipomov__in'] = [0, 3]
        soma_entradas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        filter_initial['tipomov__in'] = [1, 4]
        soma_saidas = Diario.objects.filter(**filter_customer).filter(**filter_initial)
        if soma_entradas:
            soma_entradas = soma_entradas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_entradas = Decimal('0.00')
        if soma_saidas:
            soma_saidas = soma_saidas.aggregate(Sum('valor'))['valor__sum']
        else:
            soma_saidas = Decimal('0.00')
        saldo_inicial = soma_entradas - soma_saidas
        saldo_inicial = round(saldo_inicial, 2)
        new_item = {
            'banco': '',
            'parceiro': '',
            'categoria': '',
            'valor_entra': '',
            'valor_sai': '',
            'valor_saldo': saldo_inicial,
            'datavenc': '',
            'datapago': '',
        }
        #list_diario.append(new_item)
        saldo_atual = saldo_inicial
        soma_entradas = Decimal('0.0')
        soma_saidas = Decimal('0.0')
        filter_search['tipomov__in'] = [1, 4]
        filter_search['categoria__classifica'] = True
        meses = Diario.objects.filter(**filter_customer).filter(**filter_search).annotate(mes=TruncMonth('datadoc')).values('mes').annotate(Sum('valor')).order_by('mes')
        meses = {str(x['mes'])[:7]: Decimal('0.00') for x in meses}
        diario = Diario.objects.filter(**filter_customer).filter(**filter_search).annotate(mes=TruncMonth('datadoc')).values_list('parceiro__nome', 'mes').annotate(Sum('valor')).order_by('parceiro__nome', 'mes')
        new_item = {'parceiro': ''}
        primeiro = True
        for i in diario:
            #valor_entra = Decimal('0.00') if i.tipomov in [1, 4] else i.valor 
            #valor_sai = Decimal('0.00') if i.tipomov in [0, 3] else i.valor
            #soma_entradas += valor_entra
            #soma_saidas += valor_sai
            #saldo_atual = saldo_atual + valor_entra - valor_sai
            #if i.tipomov == 4 and i.descricao == '<CRED.CARD>':
            #    nomecartao = Diario.objects.filter(origin_transfer=i.id).first().banco.nomebanco
            #if i.tipomov == 3 and i.descricao == '<CRED.CARD>':
            #    nomecartao = Diario.objects.filter(id=i.origin_transfer).first().banco.nomebanco
            if i[0] != new_item['parceiro']:
                if not primeiro:
                    list_diario.append(new_item)
                else:
                    primeiro = False
                new_item = {
                    'parceiro': i[0],
                    'meses': meses.copy()
                }
            new_item['meses'][str(i[1])[:7]] = round(i[2], 2)
        list_diario.append(new_item)
    else:
        form = ResumoForm()
        form.fields['data_inicial'].initial = date.today().replace(month=1, day=1).strftime('%Y-%m')
        form.fields['data_final'].initial = date.today().replace(month=12, day=1).strftime('%Y-%m')
        filter_banco = filter_customer.copy()
        form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
        meses = []
        for i in range(1, 13):
            meses.append(str(date.today().replace(day=1).replace(month=i))[:7])
        soma_entradas = Decimal('0.00')
        soma_saidas = Decimal('0.00')
        saldo_atual = Decimal('0.00')
    template = loader.get_template('relatorios/parceiro.html')
    context = {
        'title': 'Demonstrativo - Despesas por Parceiro',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'hoje': date.today(),
        'list_diario': list_diario,
        'form': form,
        'meses': '","'.join([str(x)[:7] for x in meses]),
        'lista_mes': [str(x)[:7] for x in meses],
        'active_relatorios': 'show',
        'active_relatorios_parceiro': 'active',
    }
    return HttpResponse(template.render(context, request))
