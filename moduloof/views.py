from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Orcamento_adesivo, Orcamento_filme
from .forms import OcadesivoForm, OcfilmeForm


# Metodos
# Adesivio
def calculodes(vl, ac):
    vl = float(vl)
    ac = float(ac)
    if ac > 0:
        return float(vl - (vl * (ac/100)))
    else:
        return vl


def calculoaca(vl, ac):
    vl = float(vl)
    ac = float(ac)
    if ac > 0:
        return float(vl + (vl * (ac/100)))
    else:
        return vl


def calculova(mqg, vg, ac):
    # Constantes
    mqg = mqg
    vg = vg
    ac = ac
    mi = float(7)
    a = float(5)
    b = float(3)
    c = float(2)
    d = float(1)
    e = float(0)
    ma = float(80)
    mb = float(100)
    mc = float(200)
    md = float(300)
    me = float(350)

    # Calculos Valores do metro
    if mqg >= me:
        return float(calculoaca(vg + e, ac))
    elif mqg >= md:
        return float(calculoaca(vg + d, ac))
    elif mqg >= mc:
        return float(calculoaca(vg + c, ac))
    elif mqg >= mb:
        return float(calculoaca(vg + b, ac))
    elif mqg >= ma:
        return float(calculoaca(vg + a, ac))
    else:
        return float(calculoaca(vg + mi, ac))

# Filme
def calculovf(mqg, vg, ac):
    # Constantes
    mqg = mqg
    vg = vg
    ac = ac
    mi = float(6)
    a = float(4)
    b = float(3)
    c = float(2)
    d = float(1)
    e = float(0)
    ma = float(20)
    mb = float(40)
    mc = float(60)
    md = float(100)
    me = float(150)

    # Calculos Valores do metro
    if mqg >= me:
        return float(calculoaca(vg + e, ac))
    elif mqg >= md:
        return float(calculoaca(vg + d, ac))
    elif mqg >= mc:
        return float(calculoaca(vg + c, ac))
    elif mqg >= mb:
        return float(calculoaca(vg + b, ac))
    elif mqg >= ma:
        return float(calculoaca(vg + a, ac))
    else:
        return float(calculoaca(vg + mi, ac))


# Views
def home(request):
    return render(request, 'moduloof/home.html')


def locadesivo(request):
    data = {}
    listagem = Orcamento_adesivo.objects.all()
    data['listagem'] = listagem
    return render(request, 'moduloof/locadesivo.html', data)


def locfilme(request):
    data = {}
    listagem = Orcamento_filme.objects.all()
    data['listagem'] = listagem
    return render(request, 'moduloof/locfilme.html', data)


def novo_ocadesivo(request):
    data = {}
    form = OcadesivoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_ladesivo')

    data['form'] = form
    return render(request, 'moduloof/ocadesivobt.html', data)


def novo_ocfilme(request):
    data = {}
    form = OcfilmeForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_lfilme')

    data['form'] = form
    return render(request, 'moduloof/ocfilme.html', data)


def cons_ocadesivo(request, pk):
    data = {}
    cons = Orcamento_adesivo.objects.get(pk=pk)
    form = OcadesivoForm(request.POST or None, instance=cons)

    if form.is_valid():
        form.save()
        return redirect('url_cons_ocadesivo', cons.id)

    # Constantes
    mi = float(7)
    vatmi = int(700)
    conv = int(1000)

    # Dados BD
    larg = float(cons.larg)
    comp = float(cons.comp)
    va = float(cons.material.valor_de_venda)
    inc = cons.acabamento.incremento
    quant = int(cons.quantidade)

    # Calculos Base
    area = float((comp / conv) * (larg / conv))
    quantmi = int(vatmi / (area * (va + mi)))
    quantmi = str(quantmi)

    # Condicional de arredondamento
    if len(quantmi) >= 7:
        unidade = 1000000
    elif len(quantmi) >= 6:
        unidade = 100000
    elif len(quantmi) >= 5:
        unidade = 10000
    elif len(quantmi) >= 4:
        unidade = 1000
    elif len(quantmi) >= 3:
        unidade = 100
    elif len(quantmi) >= 2:
        unidade = 10
    else:
        unidade = 1

    quantmi = (int(quantmi[0]) + 1) * unidade

    if quant < quantmi:
        quanta = quantmi
    else:
        quanta = int(quant * 1)

    quantb = int(quanta * 2)
    quantc = int(quanta * 3)
    mqmi = float(area * quantmi)
    mqa = float(area * quanta)
    mqb = float(area * quantb)
    mqc = float(area * quantc)

    # Calculos Valores
    vaa = calculova(mqa, va, inc)
    vab = calculova(mqb, va, inc)
    vac = calculova(mqc, va, inc)
    vami = calculova(mqmi, va, inc)

    if vab >= vaa:
        quantb = quantb * 2
        mqb = float(area * quantb)
        vab = calculova(mqb, va, inc)
        if vab >= vaa:
            vab = round(calculodes(vaa, 3), 2)


    if vac >= vab:
        quantc = quantb * 2
        mqc = float(area * quantc)
        vac = calculova(mqc, va, inc)
        if vac >= vab:
            vac = round(calculodes(vab, 3), 2)


    # Valor Unitário
    resa = float(round((area * vaa), 4))
    resb = float(round((area * vab), 4))
    resc = float(round((area * vac), 4))


    data['valor_a'] = resa
    data['total_a'] = round(resa * quanta, 4)
    data['valor_b'] = resb
    data['total_b'] = round(resb * quantb, 4)
    data['valor_c'] = resc
    data['total_c'] = round(resc * quantc, 4)
    data['quanta'] = quanta
    data['quantb'] = quantb
    data['quantc'] = quantc
    data['vaa'] = vaa
    data['vab'] = vab
    data['vac'] = vac
    data['vami'] = vami
    data['quantmi'] = quantmi

    data['form'] = form
    return render(request, 'moduloof/ocadesivobt.html', data)


def cons_ocfilme(request, pk):
    data = {}
    cons = Orcamento_filme.objects.get(pk=pk)
    form = OcfilmeForm(request.POST or None, instance=cons)

    if form.is_valid():
        form.save()
        return redirect('url_cons_ocfilme', cons.id)

    # Constantes
    mi = float(6)
    vatmi = int(700)
    conv = int(1000)

    # Dados BD
    larg = float(cons.larg)
    comp = float(cons.comp)
    rend = float(cons.material.rendimento)
    gram = float(cons.material.gramatura)
    va = float(cons.material.valor_de_venda)
    inc = cons.acabamento.incremento
    quant = int(cons.quantidade)

    # Calculos Base
    area = float(round((comp / conv) * (larg / conv), 5))
    kgmi = float(vatmi / (va + mi))
    ar = float(area * rend)
    quantmi = int(round(float((kgmi * float(conv)) / ar), 0))
    quantmi = str(quantmi)

    # Condicional de arredondamento
    if len(quantmi) >= 7:
        unidade = 1000000
    elif len(quantmi) >= 6:
        unidade = 100000
    elif len(quantmi) >= 5:
        unidade = 10000
    elif len(quantmi) >= 4:
        unidade = 1000
    elif len(quantmi) >= 3:
        unidade = 100
    elif len(quantmi) >= 2:
        unidade = 10
    else:
        unidade = 1

    quantmi = (int(quantmi[0]) + 1) * unidade

    if quant < quantmi:
        quanta = quantmi
    else:
        quanta = int(quant * 1)

    quantb = int(quanta * 2)
    quantc = int(quanta * 3)
    mqmi = float((area * rend * quantmi)/conv)
    mqa = float((area * rend * quanta)/conv)
    mqb = float((area * rend * quantb)/conv)
    mqc = float((area * rend * quantc)/conv)

    # Calculos Valores
    vaa = calculovf(mqa, va, inc)
    vab = calculovf(mqb, va, inc)
    vac = calculovf(mqc, va, inc)
    vami = calculovf(mqmi, va, inc)

    if vab >= vaa:
        quantb = quantb * 2
        mqb = float((area * rend * quantb)/conv)
        vab = calculova(mqb, va, inc)
        if vab >= vaa:
            vab = round(calculodes(vaa, 3), 2)

    if vac >= vab:
        quantc = quantb * 2
        mqc = float((area * rend * quantc)/conv)
        vac = calculova(mqc, va, inc)
        if vac >= vab:
            vac = round(calculodes(vab, 3), 2)


    # Valor Unitário
    resa = float(round(((mqa * vaa) / quanta), 4))
    resb = float(round(((mqb * vab) / quantb), 4))
    resc = float(round(((mqc * vac) / quantc), 4))


    data['valor_a'] = resa
    data['total_a'] = round(mqa * vaa, 2)
    data['totalp_a'] = round(mqa, 2)
    data['valor_b'] = resb
    data['total_b'] = round(mqb * vab, 2)
    data['totalp_b'] = round(mqb, 2)
    data['valor_c'] = resc
    data['total_c'] = round(mqc * vac, 2)
    data['totalp_c'] = round(mqc, 2)
    data['quanta'] = quanta
    data['quantb'] = quantb
    data['quantc'] = quantc
    data['vaa'] = vaa
    data['vab'] = vab
    data['vac'] = vac
    data['vami'] = vami
    data['quantmi'] = quantmi
    data['mqa'] = mqa
    data['area'] = area
    data['kgmi'] = kgmi
    data['ar'] = ar

    data['form'] = form
    return render(request, 'moduloof/ocfilme.html', data)


"""
def cons_ocfilme(request, pk):
    data = {}
    cons = Orcamento_filme.objects.get(pk=pk)
    form = OcfilmeForm(request.POST or None, instance=cons)

    if form.is_valid():
        form.save()
        return redirect('url_cons_ocfilme', cons.id)

    larg = float(cons.larg)
    comp = float(cons.comp)
    quanta = int(cons.quantidade * 1)
    quantb = int(cons.quantidade * 2)
    quantc = int(cons.quantidade * 3)
    rend = float(cons.material.rendimento)
    gram = float(cons.material.gramatura)
    va = float(cons.material.valor_de_venda)
    a = float(4)
    b = float(2)
    c = float(0)
    vaa = float(va + a)
    vab = float(va + b)
    vac = float(va + c)
    resa = float(round((((((comp / 1000) * (larg / 1000)) * rend) * vaa) / 1000), 4))
    respa = float(round((((((comp / 1000) * (larg / 1000)) * gram) * quanta) / 1000), 4))
    resb = float(round((((((comp / 1000) * (larg / 1000)) * rend) * vab) / 1000), 4))
    respb = float(round((((((comp / 1000) * (larg / 1000)) * gram) * quantb) / 1000), 4))
    resc = float(round((((((comp / 1000) * (larg / 1000)) * rend) * vac) / 1000), 4))
    respc = float(round((((((comp / 1000) * (larg / 1000)) * gram) * quantc) / 1000), 4))
    data['valor_a'] = resa
    data['total_a'] = round(resa * quanta, 4)
    data['totalp_a'] = round(respa, 2)
    data['valorq_a'] = round(vaa, 2)
    data['valor_b'] = resb
    data['total_b'] = round(resb * quantb, 4)
    data['totalp_b'] = round(respb, 2)
    data['valorq_b'] = round(vab, 2)
    data['valor_c'] = resc
    data['total_c'] = round(resc * quantc, 4)
    data['totalp_c'] = round(respc, 2)
    data['valorq_c'] = round(vac, 2)
    data['quanta'] = quanta
    data['quantb'] = quantb
    data['quantc'] = quantc
    data['form'] = form
    return render(request, 'moduloof/ocfilme.html', data)
"""
