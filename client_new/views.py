
from rest_framework import viewsets
from .models import Client, RFQ, JobCard, PaymentBall, Task, SubContracting
from .serializers import ClientSerializer, RFQSerializer, JobCardSerializer, PaymentBallSerializer, TaskSerializer, SubContractingSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend  # Add this import
from .filters import RFQFilter, JobCardFilter  # Import the filter


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.order_by('-created_at').all()
    serializer_class = ClientSerializer

class RFQViewSet(viewsets.ModelViewSet):
    queryset = RFQ.objects.order_by('-rfq_date').all()
    serializer_class = RFQSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = RFQFilter

    def get_queryset(self):
        client_id = self.kwargs['client_pk']
        return RFQ.objects.filter(client__client_id=client_id)
    
    
class GlobalRFQViewSet(viewsets.ModelViewSet):
    queryset = RFQ.objects.all()
    serializer_class = RFQSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = RFQFilter


from rest_framework import viewsets
from .models import JobCard, PaymentBall
from .serializers import JobCardSerializer, PaymentBallSerializer

class GlobalJobCardViewSet(viewsets.ModelViewSet):
    queryset = JobCard.objects.order_by('-created_at').all().prefetch_related('payment_balls') 
    serializer_class = JobCardSerializer

    def get_serializer(self, *args, **kwargs):
        """
        Handle both single and multiple objects.
        """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)
    
    filter_backends = [DjangoFilterBackend]
    filterset_class = JobCardFilter
    
    

class PaymentBallViewSet(viewsets.ModelViewSet):
    queryset = PaymentBall.objects.all().select_related('job_card')
    serializer_class = PaymentBallSerializer

    def get_queryset(self):
        queryset = PaymentBall.objects.all().select_related('job_card')
        job_card_id = self.request.query_params.get('job_card', None)
        # print(job_card_id)
        
        if job_card_id:
            queryset = queryset.filter(job_card_id=job_card_id)
            # print(queryset)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_job_card(self, request):
        job_card_id = request.query_params.get('job_card')
        if not job_card_id:
            return Response(
                {"error": "job_card parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_balls = self.get_queryset().filter(job_card_id=job_card_id)
        serializer = self.get_serializer(payment_balls, many=True)
        return Response(serializer.data)



class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('payment_ball', 'assignee').all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all().select_related('payment_ball')
        payment_ball = self.request.query_params.get('payment_ball', None)
        # print(job_card_id)
        
        if payment_ball:
            queryset = queryset.filter(payment_ball=payment_ball)
            print(queryset)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_payment_ball(self, request):
        payment_ball = request.query_params.get('payment_ball')
        if not payment_ball:
            return Response(
                {"error": "payment_ball parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_balls = self.get_queryset().filter(payment_ball=payment_ball)
        serializer = self.get_serializer(payment_balls, many=True)
        return Response(serializer.data)


class SubContractingViewSet(viewsets.ModelViewSet):
    queryset = SubContracting.objects.select_related('task', 'assignee').all()
    serializer_class = SubContractingSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        if task_id:
            return self.queryset.filter(task_id=task_id)
        return self.queryset

class GlobalTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('payment_ball', 'assignee').all()
    serializer_class = TaskSerializer
    print(queryset)
    print(serializer_class)

    def get_queryset(self):
        queryset = Task.objects.all().select_related('payment_ball')
        payment_ball = self.request.query_params.get('payment_ball', None)
        # print(job_card_id)
        
        if payment_ball:
            queryset = queryset.filter(payment_ball=payment_ball)
            print(queryset)
        return queryset
    
    @action(detail=False, methods=['get'])
    def by_payment_ball(self, request):
        payment_ball = request.query_params.get('payment_ball')
        if not payment_ball:
            return Response(
                {"error": "payment_ball parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_balls = self.get_queryset().filter(payment_ball=payment_ball)
        serializer = self.get_serializer(payment_balls, many=True)
        return Response(serializer.data)


class GlobalSubContractingViewSet(viewsets.ModelViewSet):
    queryset = SubContracting.objects.select_related('task', 'assignee').all()
    serializer_class = SubContractingSerializer

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        if task_id:
            return self.queryset.filter(task_id=task_id)
        return self.queryset   














# from django.shortcuts import render

# # Create your views here.
# from rest_framework import status, viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from .models import Client, RFQ, Quotation, LPO,  JobCard
# from .serializers import ClientSerializer, RFQSerializer, QuotationSerializer, LPOSerializer, JobCardSerializer

# class ClientViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer

# class RFQViewSet(viewsets.ModelViewSet):
#     queryset = RFQ.objects.all()
#     serializer_class = RFQSerializer

#     def get_queryset(self):
#         client_id = self.kwargs['client_pk']
#         return RFQ.objects.filter(client__client_id=client_id)

# class QuotationViewSet(viewsets.ModelViewSet):
#     queryset = Quotation.objects.all()
#     serializer_class = QuotationSerializer

#     def get_queryset(self):
#         rfq_id = self.kwargs['rfq_pk']
#         return Quotation.objects.filter(rfq__rfq_id=rfq_id)

# class LPOViewSet(viewsets.ModelViewSet):
#     queryset = LPO.objects.all()
#     serializer_class = LPOSerializer

#     def get_queryset(self):
#         quotation_id = self.kwargs['quotation_pk']
#         return LPO.objects.filter(quotation__quotation_id=quotation_id)

# class RFQViewSet(viewsets.ModelViewSet):
#     serializer_class = RFQSerializer

#     def get_queryset(self):
#         client_id = self.kwargs['client_pk']
#         return RFQ.objects.filter(client__client_id=client_id)

# class QuotationViewSet(viewsets.ModelViewSet):
#     serializer_class = QuotationSerializer

#     def get_queryset(self):
#         rfq_id = self.kwargs['rfq_pk']
#         return Quotation.objects.filter(rfq__rfq_id=rfq_id)

# class LPOViewSet(viewsets.ModelViewSet):
#     serializer_class = LPOSerializer

#     def get_queryset(self):
#         quotation_id = self.kwargs['quotation_pk']
#         return LPO.objects.filter(quotation__quotation_id=quotation_id)

# class JobCardViewSet(viewsets.ModelViewSet):
#     serializer_class = JobCardSerializer

#     def get_queryset(self):
#         lpo_id = self.kwargs['lpo_pk']
#         return JobCard.objects.filter(lpo__lpo_id=lpo_id)








# class JobCardViewSet(viewsets.ModelViewSet):
#     queryset = JobCard.objects.all()
#     serializer_class = JobCardSerializer

#     @action(detail=False, methods=['post'], url_path='create-jobcard')
#     def create_job_card(self, request):
#         quotation_id = request.data.get('quotation_id')
#         lpo_id = request.data.get('lpo_id')
#         job_number = request.data.get('job_number')
#         scope_of_work = request.data.get('scope_of_work')
#         delivery_timelines = request.data.get('delivery_timelines')
#         payment_terms = request.data.get('payment_terms')

#         try:
#             # Retrieve the Quotation and LPO
#             quotation = Quotation.objects.get(pk=quotation_id)
#             lpo = LPO.objects.get(pk=lpo_id)

#             # Create JobCard
#             job_card = JobCard.objects.create(
#                 quotation=quotation,
#                 lpo=lpo,
#                 job_number=job_number,
#                 scope_of_work=scope_of_work,
#                 delivery_timelines=delivery_timelines,
#                 payment_terms=payment_terms,
#                 status='Pending'
#             )

#             # Serialize and return the created JobCard
#             serializer = JobCardSerializer(job_card)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Quotation.DoesNotExist:
#             return Response({"error": "Quotation not found."}, status=status.HTTP_404_NOT_FOUND)
#         except LPO.DoesNotExist:
#             return Response({"error": "LPO not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

