import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { VehicleService, Vehicle } from '../../services/vehicle.service';

@Component({
  selector: 'app-vehicle-detail',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './vehicle-detail.component.html',
  styleUrl: './vehicle-detail.component.css'
})
export class VehicleDetailComponent implements OnInit {
  vehicle: Vehicle | null = null;
  loading = true;
  error = '';

  constructor(
    private route: ActivatedRoute,
    private vehicleService: VehicleService
  ) { }

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.vehicleService.getOne(id).subscribe({
      next: (data) => {
        this.vehicle = data;
        this.loading = false;
      },
      error: () => {
        this.error = 'Nie znaleziono ogłoszenia.';
        this.loading = false;
      }
    });
  }
}
