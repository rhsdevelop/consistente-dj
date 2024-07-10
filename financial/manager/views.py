from datetime import date, datetime, timedelta
from decimal import Decimal
from calendar import monthrange

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import *
from .models import *

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
        return redirect('/cliente/list')
    form = AddClienteForm()
    template = loader.get_template('cliente/add.html')
    context = {
        'title': 'Adicionar Novo Cliente',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
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
        return redirect('/cliente/list')
    form = AddClienteForm(instance=cliente)
    template = loader.get_template('cliente/edit.html')
    context = {
        'title': 'Dados da clienteregação Selecionada',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
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
        return redirect('/clienteuser/list')
    form = AddClienteUserForm()
    template = loader.get_template('clienteuser/add.html')
    context = {
        'title': 'Adicionar Novo Cliente',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
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
        return redirect('/clienteuser/list')
    form = AddClienteUserForm(instance=clienteuser)
    template = loader.get_template('clienteuser/edit.html')
    context = {
        'title': 'Dados da clienteregação Selecionada',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
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
            for usuariobanco in request['POST'].getlist('allowed_users'):
                item.allowed_users.add(usuariobanco)
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, form.errors)
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
        'form': form,
        'active_register_banco': 'active',
    }
    return HttpResponse(template.render(context, request))


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
    list_banco = Banco.objects.filter(**filter_search)
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
        return redirect('/categoria/list')
    form = AddCategoriaForm(instance=categoria)
    if not request.user.is_staff:
        form.fields['consistente_cliente'].widget = forms.HiddenInput()
    template = loader.get_template('categoria/edit.html')
    context = {
        'title': 'Cadastro de Categorias',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
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
    list_categoria = Categoria.objects.filter(**filter_search)
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
        item.save()
        messages.success(request, 'Registro adicionado com sucesso.')
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
        item.save()
        messages.success(request, 'Registro alterado com sucesso.')
        return redirect('/parceiro/list')
    form = AddParceiroForm(instance=parceiro)
    if not request.user.is_staff:
        form.fields['consistente_cliente'].widget = forms.HiddenInput()
    template = loader.get_template('parceiro/edit.html')
    context = {
        'title': 'Cadastro de Parceiros',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'form': form,
        'active_register_parceiro': 'active',
    }
    return HttpResponse(template.render(context, request))


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
        if key in ['nomeparceiro', 'tipomov', 'doc'] and value:
            filter_search['%s__icontains' % key] = value
    list_parceiro = Parceiro.objects.filter(**filter_search)
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
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, form.errors)
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
        'form': form,
        'active_diario': 'show',
        'active_diario_receber': 'active',
    }
    return HttpResponse(template.render(context, request))


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
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            item.assign_user = request.user
            item.save()
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, form.errors)
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
        'form': form,
        'soma': soma,
        'active_diario': 'show',
        'active_diario_receber': 'active',
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('manager.add_diario')
def add_pagar(request):
    if request.POST:
        form = AddDiarioForm(request.POST)
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
            item.tipomov = 1
            item.save()
            messages.success(request, 'Registro adicionado com sucesso.')
        else:
            messages.error(request, form.errors)
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
    filter_banco['tipomov__in'] = [0, 1, 3]
    form.fields['parceiro'].queryset = Parceiro.objects.filter(**filter_parceiro).order_by('nome')
    form.fields['categoria'].queryset = Categoria.objects.filter(**filter_categoria).order_by('categoria')
    form.fields['banco'].queryset = Banco.objects.filter(**filter_banco).order_by('nomebanco')
    form.fields['datadoc'].initial = str(date.today())
    form.fields['datavenc'].initial = str(date.today())
    template = loader.get_template('diario/pagar/add.html')
    context = {
        'title': 'Contas à Pagar',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'form': form,
        'active_diario': 'show',
        'active_diario_pagar': 'active',
    }
    return HttpResponse(template.render(context, request))


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
    if request.POST:
        form = AddDiarioForm(request.POST, instance=pagar)
        if not request.user.is_staff:
            del form.fields['consistente_cliente']
        if form.is_valid():
            item = form.save(commit=False)
            item.assign_user = request.user
            item.save()
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, form.errors)
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
    template = loader.get_template('diario/pagar/edit.html')
    context = {
        'title': 'Contas à Pagar',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
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
            transferir_rec.descricao = request.POST['descricao']
            transferir_rec.valor = request.POST['valor']
            transferir_rec.assign_user_id = request.user
            transferir_rec.banco_id = request.POST['banco_rec']
            transferir_rec.save()
            messages.success(request, 'Registro alterado com sucesso.')
        else:
            messages.error(request, form.errors)
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
@permission_required('manager.view_diario')
def list_cartoes(request):
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
