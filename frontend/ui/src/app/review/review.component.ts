import { Component, OnInit } from '@angular/core';
import {NgForm} from '@angular/forms';
import {ReviewService} from "./review.service";
import {Review} from "./review";

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.css']
})
export class ReviewComponent implements OnInit {
  link: string;
  toggleReview: boolean;
  // toggleAdd: boolean;
  // toggleUpdate: boolean;
  reviewService: ReviewService;
  reviewInfo: Review[];
  // notice: string;

  constructor(reviewService: ReviewService) {
    this.link = undefined;
    this.toggleReview = false;
    this.reviewService = reviewService;
    this.reviewInfo = undefined;
  }

  ngOnInit(): void {
  }

  toggleCard(cardId): void {
      this.toggleReview = !this.toggleReview;
  }

  setReviewInfo(theReview: Review): void {
    this.reviewInfo = [theReview];
  }




  onLookup(): void {
    if(this.link.length>0) {
      this.reviewInfo = [];
      this.reviewService.getCreativity(this.link)
        .subscribe((data) => {
          this.setReviewInfo(data);
        });
    }
    else {
      this.reviewInfo=[];
    }
  }

  // onShowAdd(): void {
  //   this.toggleAdd = true;
  // }
  //
  // onAdd(): void {
  //   let theCustomer = new Review();
  //   theCustomer.emailID = this.addEmailId;
  //   theCustomer.username = this.addUserName;
  //   theCustomer.firstname = this.addFirstName;
  //   theCustomer.lastname = this.addLastName;
  //   theCustomer.phone = this.addPhone;
  //   this.reviewService.addCustomers(theCustomer)
  //     .subscribe((response:any) => {
  //       if(response.status===200){
  //         this.toggleAdd=false;
  //         this.notice='Add success!';
  //       }
  //       else{
  //         this.notice='Add fail!';
  //       }
  //     });
  // }
  //
  // onShowUpdate(customerID): void {
  //   this.toggleUpdate = true;
  //   this.updateEmailID = customerID;
  // }
  //
  // onUpdate(): void {
  //   let theCustomer = new Review();
  //   theCustomer.emailID = this.updateEmailID;
  //   theCustomer.username = this.updateUserName;
  //   theCustomer.firstname = this.updateFirstName;
  //   theCustomer.lastname = this.updateLastName;
  //   theCustomer.phone = this.updatePhone;
  //   this.reviewService.updateCustomers(theCustomer)
  //     .subscribe((response:any) => {
  //       if(response.status===200){
  //         this.toggleUpdate=false;
  //         this.notice='Update success!';
  //         this.onLookup();
  //       }
  //       else{
  //         this.notice='Update fail!';
  //       }
  //     });
  // }
  // onDelete(customerID): void {
  //   this.reviewService.deleteCustomers(customerID) .subscribe((response:any) => {
  //       console.log(response.status);
  //       if(response.status===200){
  //         this.onLookup();
  //         this.notice='Delete success!';
  //       }
  //       else{
  //         this.notice='Delete fail!';
  //       }
  //     });
  //
  // }

}
