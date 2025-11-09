from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_checkout_session(request):
    """Create a Stripe checkout session for one-time purchase"""
    try:
        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'pln',
                        'product_data': {
                            'name': 'Imieniny Reminder - Pełny Dostęp',
                            'description': 'Jednorazowa płatność za dożywotni dostęp',
                        },
                        'unit_amount': 4900,  # 49.00 PLN
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=settings.FRONTEND_URL + '/payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.FRONTEND_URL + '/payment/cancel',
            customer_email=request.user.email,
            metadata={
                'user_id': request.user.id,
            }
        )

        return Response({
            'sessionId': checkout_session.id,
            'url': checkout_session.url
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return Response(status=400)
    except stripe.error.SignatureVerificationError as e:
        return Response(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Get user from metadata
        user_id = session['metadata']['user_id']

        from django.contrib.auth.models import User
        from core.models import Payment

        user = User.objects.get(id=user_id)

        # Create payment record
        Payment.objects.create(
            user=user,
            stripe_session_id=session['id'],
            amount=session['amount_total'] / 100,  # Convert from cents
            currency=session['currency'],
            status='completed'
        )

        # Mark user as having purchased
        profile, created = user.profile.get_or_create(user=user)
        profile.has_purchased = True
        profile.save()

    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_payment_status(request):
    """Check if user has purchased the app"""
    try:
        from core.models import UserProfile
        profile = UserProfile.objects.get(user=request.user)
        return Response({
            'has_purchased': profile.has_purchased,
            'purchase_date': profile.purchase_date
        })
    except UserProfile.DoesNotExist:
        return Response({
            'has_purchased': False,
            'purchase_date': None
        })
