# See the fixtures/ directory for examples of the request bodies
# needed to create objects using the ListCreateAPIViews below.

from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.contenttypes.models import ContentType

from api.models import Payment, CreditCard, Order, EBTCard
from api.serializers import PaymentSerializer, CreditCardSerializer, OrderSerializer, EBTCardSerializer
from processor import processPayment

class ListCreateCreditCard(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/credit_cards/ <- returns a list of all CreditCard objects
    2. POST http://localhost:8000/api/credit_cards/ <- creates a single CreditCard object and returns it

    """
    queryset = CreditCard.objects.all()
    serializer_class = CreditCardSerializer

    # Creates a CreditCard object and returns it.
    def post(self, request):
        serializer = CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDeleteCreditCard(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/credit_cards/:id/ <- returns a CreditCard object provided its id.
    2. DELETE http://localhost:8000/api/credit_cards/:id/ <- deletes a CreditCard object by id.

    """
    # queryset = CreditCard.objects.all()
    # serializer_class = CreditCardSerializer
    
    # Deletes a CreditCard object by id.
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            credit_card = CreditCard.objects.get(id=pk)
            credit_card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CreditCard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ListCreateEBTCard(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/ebt_cards/ <- returns a list of all EBTCard objects
    2. POST http://localhost:8000/api/ebt_cards/ <- creates a single EBTCard object and returns it

    """
    queryset = EBTCard.objects.all()
    serializer_class = EBTCardSerializer

    # Creates an EBTCard object and returns it.
    def post(self, request):
        serializer = EBTCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDeleteEBTCard(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/ebt_cards/:id/ <- returns an EBTCard object provided its id.
    2. DELETE http://localhost:8000/api/ebt_cards/:id/ <- deletes an EBTCard object by id.

    """
    
    # Deletes an EBTCard object by id.
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            ebt_card = EBTCard.objects.get(id=pk)
            ebt_card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CreditCard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ListCreateOrder(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/orders/ <- returns a list of all Order objects
    2. POST http://localhost:8000/api/orders/ <- creates a single Order object and returns it

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request):
        # Creates an Order object and returns it.
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveDeleteOrder(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/orders/:id/ <- returns an Order object provided its id.
    2. DELETE http://localhost:8000/api/orders/:id/ <- deletes an Order object by id.

    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Deletes an Order object by id.
    def delete(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        try:
            order = Order.objects.get(id=pk)
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CreditCard.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ListCreatePayment(ListCreateAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/payments/ <- returns a list of all Payment objects
    2. POST http://localhost:8000/api/payments/ <- creates a single Payment object and associates it with the Order in the request body.

    """
    # Returns a list of all Payment objects.
    def get(self, request):
        queryset = Payment.objects.all()
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    # Creates a Payment object and returns it.
    '''
        payment_option -> the payment option selected either credit_card or ebt_card
        payment_method -> the id of the payment option model selected
        order -> the id of the order to associate the payment with
    '''
    def post(self, request):
        all_content_types = ContentType.objects.all()

        selected_model_index = None
        model_selected = None
        if request.data['payment_option'] == "credit_card":
            model_selected = CreditCard
        elif request.data['payment_option'] == "ebt_card":
            model_selected = EBTCard
        else:
            raise Exception("Invalid payment option")

        # Iterate through the content types to find the one associated with the model selected
        for content_type in all_content_types:
            if content_type.model_class() == model_selected:
                selected_model_index = content_type.id
                break

        instance_id = request.data['payment_method']

        payment_data = {
            "order": request.data.get('order'),
            "amount": request.data.get('amount'),
            "description": request.data.get('description'),
            "payment_option": request.data.get('payment_option'),
            "payment_method_types": selected_model_index,
            "target_id": instance_id
        }

        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveDeletePayment(RetrieveDestroyAPIView):
    """ Exposes the following routes,
    
    1. GET http://localhost:8000/api/payments/:id/ <- returns a Payment object provided its id.
    2. DELETE http://localhost:8000/api/payments/:id/ <- deletes a Payment object by id.

    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def delete(self, request, pk, *args, **kwargs):
        try:
            credit_card = Payment.objects.get(id=pk)
            if credit_card:
                credit_card.delete()
            return Response(status=204)  # Return a 204 No Content response on successful deletion.
        except CreditCard.DoesNotExist:
            return Response(status=404)

class CaptureOrder(APIView):
    """ Provided an Order's id, submit all associated payments to the payment processor.

    Payments will change status to either failed or succeeded, depending on the
    response from the payment processor.

    Once all payments have been processed, the status of the Order object will be updated
    to 'suceeded' if all of the payments were successful or 'failed' if at least one payment
    was not successful.
    """

    def post(self, request, id):
        try:
            order_obj = Order.objects.get(id=id) # throws if order_id not found

            # Find all Payments associated with this Order via /api/payments/
            payment_queryset = Payment.objects.filter(order__id=id)

            # Payments must satisfy the order_total
            total_payment_amount = sum([x.amount for x in payment_queryset])
            # EBT payments must satisfy the ebt_total
            total_ebt_payment_amount = sum([x.amount for x in payment_queryset if x.payment_option == "ebt_card"])
            if total_ebt_payment_amount > order_obj.ebt_total:
                return Response({
                    "error_message": "EBT total exceeds ebt order total for Order with id {}".format(id)
                }, status=status.HTTP_400_BAD_REQUEST)
            if total_payment_amount != order_obj.order_total:
                return Response({
                    "error_message": "Payment total does not match order total for Order with id {}".format(id)
                }, status=status.HTTP_400_BAD_REQUEST)

            potential_errors = []
            for payment in payment_queryset:
                potential_error = processPayment(payment)

                if potential_error:
                    potential_errors.append(potential_error)

            if potential_errors:
                order_obj.status = Order.TYPE_FAILED
            else:
                order_obj.status = Order.TYPE_SUCCEEDED
                order_obj.success_date = timezone.now()

            order_obj.save() # write status back to database

            return Response(
                OrderSerializer(order_obj).data
            )

        except Order.DoesNotExist:
            return Response({
                "error_message": "Unable to find Order with id {}".format(id)
            }, status=status.HTTP_404_NOT_FOUND)
