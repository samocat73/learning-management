from django.forms import model_to_dict
from rest_framework import filters, views, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from materials.models import Course
from users.models import Payment, Subscription, User
from users.serializers import PaymentSerializer, UserSerializer, MyTokenObtainPairSerializer
from users.services import (create_stripe_price, create_stripe_product,
                            create_stripe_sessions)
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_fields = ["course", "lesson", "payment_method"]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["payment_dates"]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        stripe_product = create_stripe_product(payment.course.title)
        price = create_stripe_price(payment.amount, stripe_product.id)
        session_id, payment_link = create_stripe_sessions(price.id)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class SubscriptionAPIView(views.APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item, created = Subscription.objects.get_or_create(
            user=user, course=course_item
        )
        if not created:
            subs_item.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка создана"
        return Response({"message": message})

    def get(self, request, *args, **kwargs):
        user = self.request.user
        subs_item = Subscription.objects.filter(user=user).values()
        return Response({"subscriptions": subs_item})
