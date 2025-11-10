from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Servicio, Vehiculo
from django.urls import reverse


def inicio_taller(request):
    # página principal de la app (taller)
    return render(request, 'inicio.html', {})


def agregar_clientes(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        email = request.POST.get('email', '').strip() or None
        rfc = request.POST.get('rfc', '').strip() or None
        telefono = request.POST.get('telefono', '').strip() or None
        direccion = request.POST.get('direccion', '').strip() or None
        cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            email=email,
            rfc=rfc,
            telefono=telefono,
            direccion=direccion,
        )
        cliente.save()
        return redirect('ver_clientes')
    return render(request, 'clientes/agregar_clientes.html', {})

def ver_clientes(request):
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'clientes/ver_clientes.html', {'clientes': clientes})

def actualizar_clientes(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/actualizar_clientes.html', {'cliente': cliente})

def realizar_actualizacion_clientes(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.nombre = request.POST.get('nombre', cliente.nombre).strip()
        cliente.apellido = request.POST.get('apellido', cliente.apellido).strip()
        email = request.POST.get('email', '').strip()
        cliente.email = email or None
        rfc = request.POST.get('rfc', '').strip()
        cliente.rfc = rfc or None
        telefono = request.POST.get('telefono', '').strip()
        cliente.telefono = telefono or None
        direccion = request.POST.get('direccion', '').strip()
        cliente.direccion = direccion or None
        cliente.save()
        return redirect('ver_clientes')
    # si llama GET, redirigir a formulario de edición
    return redirect('actualizar_clientes', cliente_id=cliente.id)

def borrar_clientes(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    return render(request, 'clientes/borrar_clientes.html', {'cliente': cliente})



def agregar_servicio(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        descripcion = request.POST.get('descripcion', '') # Permite que sea opcional
        precio_base = request.POST['precio_base']
        # el modelo define el campo como tiempo_est (minutos)
        tiempo_est = request.POST.get('tiempo_est', '0')
        aplica_garantia = 'aplica_garantia' in request.POST # True si está marcado, False si no

        Servicio.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio_base=precio_base,
            tiempo_est=tiempo_est,
            aplica_garantia=aplica_garantia
        )
        return redirect('ver_servicio')
    return render(request, 'servicio/agregar_servicio.html')

def ver_servicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicio/ver_servicio.html', {'servicios': servicios})

def actualizar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    return render(request, 'servicio/actualizar_servicio.html', {'servicio': servicio})

def realizar_actualizacion_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre', servicio.nombre)
        servicio.descripcion = request.POST.get('descripcion', servicio.descripcion)
        servicio.precio_base = request.POST.get('precio_base', servicio.precio_base)
        servicio.tiempo_est = request.POST.get('tiempo_est', servicio.tiempo_est)
        servicio.aplica_garantia = 'aplica_garantia' in request.POST
        servicio.save()
        return redirect('ver_servicio')
    return redirect('ver_servicio')

def borrar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('ver_servicio')
    return render(request, 'servicio/borrar_servicio.html', {'servicio': servicio})



def agregar_vehiculo(request):
    clientes = Cliente.objects.all()
    servicios = Servicio.objects.all()
    if request.method == 'POST':
        matricula = request.POST['matricula']
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        anio = request.POST['anio']
        kilometraje = request.POST['kilometraje']
        color = request.POST['color']
        cliente_id = request.POST['cliente']
        servicios_ids = request.POST.getlist('servicios') # getlist para ManyToMany

        cliente_seleccionado = get_object_or_404(Cliente, pk=cliente_id)

        vehiculo = Vehiculo.objects.create(
            cliente=cliente_seleccionado,
            matricula=matricula,
            marca=marca,
            modelo=modelo,
            anio=anio,
            kilometraje=kilometraje,
            color=color
        )
        # Asignar servicios ManyToMany
        if servicios_ids:
            vehiculo.servicios.set(servicios_ids) # set() para asignar múltiples servicios
        
        return redirect('ver_vehiculo')
    return render(request, 'vehiculo/agregar_vehiculo.html', {'clientes': clientes, 'servicios': servicios})

def ver_vehiculo(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo/ver_vehiculo.html', {'vehiculos': vehiculos})

def actualizar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    clientes = Cliente.objects.all()
    servicios = Servicio.objects.all()
    return render(request, 'vehiculo/actualizar_vehiculo.html', {
        'vehiculo': vehiculo,
        'clientes': clientes,
        'servicios': servicios
    })

def realizar_actualizacion_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)

    if request.method == 'POST':
        vehiculo.matricula = request.POST['matricula']
        vehiculo.marca = request.POST['marca']
        vehiculo.modelo = request.POST['modelo']
        vehiculo.anio = request.POST['anio']
        vehiculo.kilometraje = request.POST['kilometraje']
        vehiculo.color = request.POST['color']

        cliente_id = request.POST['cliente']
        vehiculo.cliente = get_object_or_404(Cliente, pk=cliente_id)

        servicio_id = request.POST.get('servicio')
        vehiculo.servicio = get_object_or_404(Servicio, pk=servicio_id)

        vehiculo.save()
        return redirect('ver_vehiculo')

    return redirect('ver_vehiculo')


def borrar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('ver_vehiculo')
    return render(request, 'vehiculo/borrar_vehiculo.html', {'vehiculo': vehiculo})