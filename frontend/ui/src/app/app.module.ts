import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


import { ReactiveFormsModule } from '@angular/forms';
import {NgbNavModule} from "@ng-bootstrap/ng-bootstrap";
import { ReviewComponent } from './review/review.component';



@NgModule({
  declarations: [
    AppComponent,
    ReviewComponent
  ],
    imports: [
        BrowserModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        NgbNavModule
    ],
  providers: [
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }


