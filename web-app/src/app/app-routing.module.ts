import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import {SearchComponent} from './components/search/search.component';
import { TabulatedComponent } from './components/tabulated/tabulated.component';

const routes: Routes = [
  {path: '', component: SearchComponent},
  {path: 'tabulated', component: TabulatedComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
  })],
  exports: [RouterModule],
})
export class AppRoutingModule { }
