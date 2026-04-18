import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface VehicleImage {
  id: number;
  image: string;
  uploaded_at: string;
}

export interface Vehicle {
  id: number;
  title: string;
  description: string;
  category: string;
  category_display: string;
  brand: string;
  model: string;
  year: number;
  mileage: number;
  engine_capacity: number;
  power: number;
  fuel_type: string;
  fuel_type_display: string;
  user: string;
  image: string | null;
  images: VehicleImage[];
  created_at: string;
  published_at: string | null;
}

@Injectable({ providedIn: 'root' })
export class VehicleService {

  private apiUrl = `${environment.apiUrl}/pojazdy`;

  constructor(private http: HttpClient) { }

  getAll() {
    return this.http.get<Vehicle[]>(`${this.apiUrl}/`);
  }

  getOne(id: number) {
    return this.http.get<Vehicle>(`${this.apiUrl}/${id}/`);
  }

  getMine() {
    return this.http.get<Vehicle[]>(`${this.apiUrl}/moje/`);
  }

  create(data: FormData) {
    return this.http.post<Vehicle>(`${this.apiUrl}/`, data);
  }

  update(id: number, data: FormData) {
    return this.http.patch<Vehicle>(`${this.apiUrl}/${id}/edytuj/`, data);
  }

  publish(id: number) {
    return this.http.post<Vehicle>(`${this.apiUrl}/${id}/publikuj/`, {});
  }

  delete(id: number) {
    return this.http.delete(`${this.apiUrl}/${id}/usun/`);
  }

  uploadImage(id: number, data: FormData) {
    return this.http.post(`${this.apiUrl}/${id}/galeria/`, data);
  }
}
