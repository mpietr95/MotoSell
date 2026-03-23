from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import Vehicle
from .forms import VehicleForm


# a. Wszystkie opublikowane oferty (published_at ustawione, nie usunięte)
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(
        published_at__isnull=False,
        is_deleted=False,
    )
    return render(request, 'motosell/vehicle_list.html', {'vehicles': vehicles})


# b. Oferty zalogowanego użytkownika (wszystkie, nie usunięte)
@login_required
def my_vehicles(request):
    vehicles = Vehicle.objects.filter(
        user=request.user,
        is_deleted=False,
    )
    return render(request, 'motosell/my_vehicles.html', {'vehicles': vehicles})


# c. Dodanie nowej oferty
@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.save()
            return redirect('my_vehicles')
    else:
        form = VehicleForm()
    return render(request, 'motosell/vehicle_form.html', {'form': form})


# d. Edycja oferty — tylko przez właściciela
@login_required
def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, is_deleted=False)
    if vehicle.user != request.user:
        return HttpResponseForbidden('Nie masz uprawnień do edycji tej oferty.')
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('my_vehicles')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'motosell/vehicle_form.html', {'form': form, 'vehicle': vehicle})


# e. Publikacja oferty — tylko przez właściciela
@login_required
def vehicle_publish(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, is_deleted=False)
    if vehicle.user != request.user:
        return HttpResponseForbidden('Nie masz uprawnień do publikacji tej oferty.')
    vehicle.published_at = timezone.now().date()
    vehicle.save()
    return redirect('my_vehicles')


# f. Miękkie usunięcie oferty — tylko przez właściciela
@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, is_deleted=False)
    if vehicle.user != request.user:
        return HttpResponseForbidden('Nie masz uprawnień do usunięcia tej oferty.')
    vehicle.is_deleted = True
    vehicle.save()
    return redirect('my_vehicles')
