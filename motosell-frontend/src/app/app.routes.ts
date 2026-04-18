import { Routes } from '@angular/router';
import { VehicleListComponent } from './components/vehicle-list/vehicle-list.component';
import { VehicleDetailComponent } from './components/vehicle-detail/vehicle-detail.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { MyVehiclesComponent } from './components/my-vehicles/my-vehicles.component';
import { VehicleFormComponent } from './components/vehicle-form/vehicle-form.component';
import { authGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', component: VehicleListComponent },
  { path: 'pojazd/:id', component: VehicleDetailComponent },
  { path: 'logowanie', component: LoginComponent },
  { path: 'rejestracja', component: RegisterComponent },
  { path: 'moje-ogloszenia', component: MyVehiclesComponent, canActivate: [authGuard] },
  { path: 'dodaj', component: VehicleFormComponent, canActivate: [authGuard] },
  { path: 'edytuj/:id', component: VehicleFormComponent, canActivate: [authGuard] },
  { path: '**', redirectTo: '' },
];
