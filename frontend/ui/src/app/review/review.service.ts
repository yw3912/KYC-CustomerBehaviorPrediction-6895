import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Review } from './review';
import { CustomerRsp } from "./review";
import { Observable } from 'rxjs';;


@Injectable({
  providedIn: 'root'
})
export class ReviewService {

  reviews: Review[];
  reviewServiceUrl: string;

  constructor(private http: HttpClient) {
    this.reviews = undefined;
  }

  getReviewServiceUrl(): string {
    const theUrl = window.location.href;
    let result: string;

    result = 'http://127.0.0.1:5011/api/review/';

    return result;
  }
  /** GET heroes from the server */
  getCreativity(reviewURL): Observable<Review> {
    let theUrl: string;

    theUrl = this.getReviewServiceUrl() + reviewURL;
    return this.http.get<Review>(theUrl);
  }
}
