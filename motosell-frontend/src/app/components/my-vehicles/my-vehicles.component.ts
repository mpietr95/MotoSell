import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { VehicleService, Vehicle } from '../../services/vehicle.service';

@Component({
  selector: 'app-my-vehicles',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './my-vehicles.component.html',
  styleUrl: './my-vehicles.component.css'
})
export class MyVehiclesComponent implements OnInit {
  vehicles: Vehicle[] = [];
  loading = true;
  error = '';
  uploadingFor: number | null = null;

  constructor(private vehicleService: VehicleService) { }

  ngOnInit() {
    this.vehicleService.getMine().subscribe({
      next: (data) => {
        this.vehicles = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Nie udało się pobrać ogłoszeń.';
        this.loading = false;
      }
    });
  }

  publish(id: number) {
    this.vehicleService.publish(id).subscribe({
      next: (updated) => {
        const v = this.vehicles.find(v => v.id === id);
        if (v) v.published_at = updated.published_at;
      }
    });
  }

  delete(id: number) {
    this.vehicleService.delete(id).subscribe({
      next: () => {
        this.vehicles = this.vehicles.filter(v => v.id !== id);
      }
    });
  }

  onGalleryUpload(event: Event, id: number) {
    const input = event.target as HTMLInputElement;
    if (!input.files?.length) return;

    const data = new FormData();
    data.append('image', input.files[0]);
    this.uploadingFor = id;

    this.vehicleService.uploadImage(id, data).subscribe({
      next: () => {
        this.uploadingFor = null;
        input.value = '';
      },
      error: () => {
        this.uploadingFor = null;
      }
    });
  }
}
