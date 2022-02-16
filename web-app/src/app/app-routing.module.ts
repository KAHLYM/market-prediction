import {NgModule} from '@angular/core';
import {RouterModule, Routes} from '@angular/router';
import { LatestComponent } from './components/latest/latest.component';
import {ResultComponent} from './components/result/result.component';

const routes: Routes = [
  {path: '', component: LatestComponent},
  {path: 'result', component: ResultComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes, {
    scrollPositionRestoration: 'enabled',
  })],
  exports: [RouterModule],
})
export class AppRoutingModule { }
