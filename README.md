# API Take Home Challenge

## TimeLine

24th August
6 am - 6:20 am : Read the problem statement
6:20 am - 7:00 am : Searched for Django learning resources, read some django docs, setup the project, installed and run the prject, admin

7:00 pm - 8:15 pm : Read the problem statement again, understood the problem statement, read about few concepts through models, views, etc following the guide - "https://docs.djangoproject.com/en/3.2/intro/tutorial01/"
8 pm - 8:45/9:00 pm : Ran endpoints of credit_card, order, payment, etc. Tried to understand the flow of the code.

25th August
6:45/7 am - 8:00 am : Created EBT model, serializer, views, url. Ran the endpoints of EBT.

26th August
7:00 am - 8:00 am : Read about contentType, GenericForiegnKey and relationships between tables, tried to create payment_method to include the two types of models only.
9:00 am - 10:30 am : Tried to create a new model for payment_method but it was not working so decided to create a new field for choosing the payment method between credit card and ebt card and use GenericForiegnKey to store the id of the model. Formed a simple logic to use it.
10:45 - 11:45/12:00 am : Created a new field to choose payment option in Payment model, edited the serializer to create a function for JSON serialize the payment method object in Payment model at time of returning data, created a new view for Payment model. Ran the endpoints of Payment model.
4:00 pm - 4:30 pm : Read a little about database constraints and added a constraint to the Order model to check if the ebt_total is less than the order_total and edited capture view to put check for ebt_total value.
10:30 pm - 11:30 pm : Edited the fixtures to demonstrate the updated request bodies and added comments to the whole code edited, removed redundant code and increased readability.

## Instructions

You will be extending a Django-based API which processes credit card payments to accept both credit cards and EBT payments. This exercise shows you a challenge ACME has solved for our customers and will allow you to demonstrate your experience with REST APIs. To get started,

1. Clone this repository.
1. Implement the Required Solution below.
1. Push your code changes to a private repository hosted by you on github. 
1. Email your interviewer to invite them to your private repo and to schedule a code review.
1. Do a live code review with your interviewer. 


### Running the code

The following steps walk you through the API requests that would be made during a typical checkout flow for one of ACME's e-commerce customers. We will leave the frontend to your imagination!


- Install all the packages needed with `python -m pip install -r requirements.txt`
- Apply the included migrations with `python manage.py migrate`
- Run the server with `python manage.py runserver`
- Then start a checkout flow by creating a CreditCard with the following cURL,

```
curl -X POST \
-H 'Content-Type:application/json' \
--data-binary @./fixtures/create_credit_card.json \
http://localhost:8000/api/credit_cards/
```

- Similarly, to create an Order use, 

```
curl -X POST \
-H 'Content-Type:application/json' \
--data-binary @./fixtures/create_order.json \
http://localhost:8000/api/orders/
```

- Attach a Payment to the Order by,
  - Setting the payment_method and order fields in the file ./fixtures/create_payment.json to the ids of the CreditCard and Order you just created. Note that the amount should satisfy the full order_total.
  - Then use the following cURL,

```
curl -X POST \
-H 'Content-Type:application/json' \
--data-binary @./fixtures/create_payment.json \
http://localhost:8000/api/payments/
```

- Finally, submit the Order for processing by calling the Order capture endpoint,

```
curl -X POST \
http://localhost:8000/api/orders/1/capture/
```

The Order has been submitted for processing and the status will be changed from `draft` to `failed` or `succeeded`. If the order succeeds, then ACME's clients are done using our API and can begin their fulfillment process.

### Required solution

The goal of the exercise is to extend the API to process both credit cards (which are already supported) and EBT cards (which you will implement support for, you don't need to know what an EBT card is). EBT cards are an entirely separate payment method, which can only be used to pay for certain items such as fruits, vegetables, or dairy products. Other items, such as paper products, are not eligible to be paid for with an EBT card. Keeping track of and enforcing EBT eligibility rules will be a key feature of your API changes.

There are 4 high level changes you will need to make to this codebase,

1. Create a new model for storing EBT cards in api/models.py.
    - Follow a similar pattern to the existing CreditCard model but accounting for the differences with an EBT card which are,
        # - EBT cards have no expiration. On average, recipients of an EBT card use it for 9 months, after which the card number is canceled.
        - EBT card numbers can be from 16 to 19 digits in length, depending on which state issued the card.
    - Also create the serializer class, ListCreateAPIView and RetrieveDestroyAPIView corresponding to this model following the pattern of CreditCards. Make sure you expose URLs in api/urls.py to start using your new views.
2. Allow for the new EBT card model to be passed in the payment_method field of a Payment object.
    - Each Payment will still only be associated with a single CreditCard or EBT card object, but the payment_method field should be able to point to an instance of either.
    - Most orders in grocery e-commerce contain some items which are not EBT eligible, so most orders will also have 2 Payment objects attached to them: one Payment to a CreditCard and one Payment to an EBT card. As you can see in the Order capture endpoint, there is already support for processing multiple Payments on an Order. Please assume that you can use the same processPayment function for all Payments regardless of the payment_method. 
    - There are many ways to accomplish this, so please choose one and be prepared to justify your answer!
3. Add error checking for EBT eligibility to the Order capture view (see line 99)
    - First uncomment the ebt_total field on the Order model. This field will track the EBT eligibility of items in the Order and you can assume it is provided accurately by API clients. 
    - Make sure you uncomment ebt_total in the OrderSerializer class as well!
    - Add a database constraint such that the snap_total is always less than the order_total
    - Finally, add logic to ensure that the sum of the amount fields of Payments to EBT cards is less than the ebt_total of the Order object.
4. Update the fixtures to demonstrate the request bodies after your API changes as needed

Because you are making model changes, you will need to migrate the database after you are done editing the models with,

```sh
python manage.py makemigrations
python manage.py migrate
```

Then you will be able to make API requests again!
