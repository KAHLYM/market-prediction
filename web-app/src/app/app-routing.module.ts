import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { DummySearchComponent } from './components/dummy-search/dummy-search.component';

const routes: Routes = [
  { path: '', component: DummySearchComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
  })],
  exports: [RouterModule],
})
export class AppRoutingModule { }
