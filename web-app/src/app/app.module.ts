import {NgModule} from '@angular/core';
import {BrowserModule} from '@angular/platform-browser';
import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';

import {SentimentService} from './services/sentiment.service';
import {LatestService} from './services/latest.service';
import {initializeApp, provideFirebaseApp} from '@angular/fire/app';
import {environment} from '../environments/environment';
import {provideAuth, getAuth} from '@angular/fire/auth';
import {provideFirestore, getFirestore} from '@angular/fire/firestore';
import {provideStorage, getStorage} from '@angular/fire/storage';
import {SearchService} from './services/search.service';
import {FooterComponent} from './components/footer/footer.component';
import {HeaderComponent} from './components/header/header.component';
import {SearchComponent} from './components/search/search.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AngularMaterialModule} from './angular-material.module';
import {TabulatedComponent} from './components/tabulated/tabulated.component';
import {ResultComponent} from './components/result/result.component';
import { LatestComponent } from './components/latest/latest.component';
import { DisplayValueComponent } from './components/display-value/display-value.component';
import { AbsolutePipe } from './pipes/absolute.pipe';
import { TrailingZeroPipe } from './pipes/trailing-zero.pipe';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent,
    HeaderComponent,
    SearchComponent,
    TabulatedComponent,
    ResultComponent,
    LatestComponent,
    DisplayValueComponent,
    AbsolutePipe,
    TrailingZeroPipe,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAuth(() => getAuth()),
    provideFirestore(() => getFirestore()),
    provideStorage(() => getStorage()),
    AngularMaterialModule,
    BrowserAnimationsModule,
  ],
  providers: [LatestService, SearchService, SentimentService],
  bootstrap: [AppComponent],
})
export class AppModule { }
