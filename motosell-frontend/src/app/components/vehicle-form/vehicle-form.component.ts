import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { VehicleService, Vehicle } from '../../services/vehicle.service';

@Component({
  selector: 'app-vehicle-form',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './vehicle-form.component.html',
  styleUrl: './vehicle-form.component.css'
})
export class VehicleFormComponent implements OnInit {
  isEditMode = false;
  vehicleId: number | null = null;
  error = '';

  form = {
    title: '',
    description: '',
    category: 'osobowy',
    brand: '',
    model: '',
    year: new Date().getFullYear(),
    mileage: 0,
    engine_capacity: 0,
    power: 0,
    fuel_type: 'benzyna',
  };

  selectedFile: File | null = null;

  categories = [
    { value: 'osobowy', label: 'Osobowy' },
    { value: 'motocykl', label: 'Motocykl' },
    { value: 'ciezarowy', label: 'Ciężarowy' },
  ];

  fuelTypes = [
    { value: 'benzyna', label: 'Benzyna' },
    { value: 'diesel', label: 'Diesel' },
    { value: 'lpg', label: 'LPG' },
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private vehicleService: VehicleService
  ) { }

  ngOnInit() {
    this.vehicleId = Number(this.route.snapshot.paramMap.get('id')) || null;
    this.isEditMode = !!this.vehicleId;

    if (this.isEditMode && this.vehicleId) {
      this.vehicleService.getOne(this.vehicleId).subscribe({
        next: (v: Vehicle) => {
          this.form = {
            title: v.title,
            description: v.description,
            category: v.category,
            brand: v.brand,
            model: v.model,
            year: v.year,
            mileage: v.mileage,
            engine_capacity: v.engine_capacity,
            power: v.power,
            fuel_type: v.fuel_type,
          };
        }
      });
    }
  }

  onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.selectedFile = input.files[0];
    }
  }

  onSubmit() {
    const data = new FormData();
    Object.entries(this.form).forEach(([key, value]) => {
      data.append(key, String(value));
    });
   
  if(this.selectedFile) {
    data.append('image', this.selectedFile);
  }

  const request = this.isEditMode && this.vehicleId
    ? this.vehicleService.update(this.vehicleId, data)
    : this.vehicleService.create(data);

    request.subscribe({
      next: () => this.router.navigate(['/moje-ogloszenia']),
        error: () => this.error = 'Wystąpił błąd. Sprawdź dane i spróbuj ponownie.'
    });
  }
}
