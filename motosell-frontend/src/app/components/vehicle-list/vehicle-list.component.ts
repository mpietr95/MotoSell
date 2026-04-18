import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { VehicleService, Vehicle } from '../../services/vehicle.service';

@Component({
  selector: 'app-vehicle-list',
  standalone: true,
  imports: [RouterLink, FormsModule],
  templateUrl: './vehicle-list.component.html',
  styleUrl: './vehicle-list.component.css'
})
export class VehicleListComponent implements OnInit {
  vehicles: Vehicle[] = [];
  filtered: Vehicle[] = [];
  paginated: Vehicle[] = [];
  loading = true;
  error = '';

  searchBrand = '';
  searchCategory = '';
  searchYear = '';

  currentPage = 1;
  pageSize = 6;

  categories = [
    { value: '', label: 'Wszystkie' },
    { value: 'osobowy', label: 'Osobowy' },
    { value: 'motocykl', label: 'Motocykl' },
    { value: 'ciezarowy', label: 'Ciężarowy' },
  ];

  constructor(private vehicleService: VehicleService) { }

  ngOnInit() {
    this.vehicleService.getAll().subscribe({
      next: (data) => {
        this.vehicles = data;
        this.filtered = data;
        this.updatePage();
        this.loading = false;
      },
      error: () => {
        this.error = 'Nie udało się pobrać ogłoszeń.';
        this.loading = false;
      }
    });
  }

  filter() {
    this.filtered = this.vehicles.filter(v => {
      const brandMatch = v.brand.toLowerCase().includes(this.searchBrand.toLowerCase());
      const categoryMatch = !this.searchCategory || v.category === this.searchCategory;
      const yearMatch = !this.searchYear || v.year === Number(this.searchYear);
      return brandMatch && categoryMatch && yearMatch;
    });
    this.currentPage = 1;
    this.updatePage();
  }

  reset() {
    this.searchBrand = '';
    this.searchCategory = '';
    this.searchYear = '';
    this.filtered = this.vehicles;
    this.currentPage = 1;
    this.updatePage();
  }

  updatePage() {
    const start = (this.currentPage - 1) * this.pageSize;
    this.paginated = this.filtered.slice(start, start + this.pageSize);
  }

  get totalPages(): number {
    return Math.ceil(this.filtered.length / this.pageSize);
  }

  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
      this.updatePage();
    }
  }

  nextPage() {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
      this.updatePage();
    }
  }
}
