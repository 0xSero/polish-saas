# Stripe Integration Setup Guide

This monorepo includes complete Stripe payment integration for all paid apps. Follow this guide to set up Stripe and start accepting payments.

## Monetization Models

| App | Model | Price | Features |
|-----|-------|-------|----------|
| Imieniny Reminder | One-time purchase | 49 PLN | Full access |
| AirAware Polska | Freemium subscription | 19 PLN/month | Unlimited alerts |
| CenWatch PL | Freemium | 14 PLN/month | Unlimited price tracking |
| Dział Kowiec Planner | One-time purchase | 39 PLN | Full access |
| PupilCare | One-time purchase | 29 PLN | Full access |
| PolishWriter | Subscription | 24 PLN/month | Full grammar checking |

## Prerequisites

1. **Stripe Account**
   - Sign up at [stripe.com](https://stripe.com)
   - Get your API keys from the Dashboard
   - Set up webhook endpoints

2. **Environment Variables**
   - Each app has `.env.stripe.example` files
   - Copy to `.env` and add your keys

## Quick Setup

### 1. Get Stripe API Keys

1. Log in to [Stripe Dashboard](https://dashboard.stripe.com)
2. Go to **Developers** → **API keys**
3. Copy your:
   - **Publishable key** (starts with `pk_test_` or `pk_live_`)
   - **Secret key** (starts with `sk_test_` or `sk_live_`)

### 2. Configure Backend

For each paid app (e.g., `imieniny-reminder`):

```bash
cd apps/imieniny-reminder/backend
cp .env.stripe.example .env
```

Edit `.env`:
```bash
STRIPE_PUBLIC_KEY=pk_test_your_actual_key_here
STRIPE_SECRET_KEY=sk_test_your_actual_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
FRONTEND_URL=http://localhost:3001
```

### 3. Configure Frontend

```bash
cd apps/imieniny-reminder/frontend
cp .env.local.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=pk_test_your_actual_key_here
```

### 4. Set Up Webhooks

Webhooks are essential for processing completed payments.

#### Development (Using Stripe CLI)

1. Install Stripe CLI:
```bash
# macOS
brew install stripe/stripe-cli/stripe

# Linux
wget https://github.com/stripe/stripe-cli/releases/download/v1.19.4/stripe_1.19.4_linux_x86_64.tar.gz
tar -xvf stripe_1.19.4_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin/
```

2. Login to Stripe:
```bash
stripe login
```

3. Forward webhooks to your local server:
```bash
stripe listen --forward-to localhost:8001/api/payments/webhook/
```

4. Copy the webhook signing secret (`whsec_...`) to your `.env` file

#### Production

1. Go to **Developers** → **Webhooks** in Stripe Dashboard
2. Click **Add endpoint**
3. Set URL: `https://yourdomain.com/api/payments/webhook/`
4. Select events to listen for:
   - `checkout.session.completed`
   - `customer.subscription.created`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
5. Copy the webhook signing secret to your production `.env`

## Testing Payments

### Test Card Numbers

Stripe provides test cards that simulate different scenarios:

| Card Number | Scenario |
|-------------|----------|
| 4242 4242 4242 4242 | Successful payment |
| 4000 0025 0000 3155 | Requires authentication (3D Secure) |
| 4000 0000 0000 9995 | Declined (generic) |
| 4000 0000 0000 0002 | Declined (insufficient funds) |

- **Expiry**: Any future date
- **CVC**: Any 3 digits
- **ZIP**: Any 5 digits

### Test Payment Flow

1. Start the app:
```bash
# Terminal 1: Backend
cd apps/imieniny-reminder/backend
source venv/bin/activate
python manage.py runserver 8001

# Terminal 2: Frontend
cd apps/imieniny-reminder/frontend
npm run dev

# Terminal 3: Stripe webhooks
stripe listen --forward-to localhost:8001/api/payments/webhook/
```

2. Navigate to `http://localhost:3001`
3. Click **"Kup teraz"** (Buy now)
4. Use test card `4242 4242 4242 4242`
5. Complete the checkout
6. Verify the payment in Stripe Dashboard

## API Endpoints

Each app includes these payment endpoints:

### Create Checkout Session
```http
POST /api/payments/create-checkout/
Authorization: Bearer <jwt_token>

Response:
{
  "sessionId": "cs_test_...",
  "url": "https://checkout.stripe.com/..."
}
```

### Handle Webhook
```http
POST /api/payments/webhook/
Stripe-Signature: <signature>

Body: (Stripe webhook event)
```

### Check Payment Status
```http
GET /api/payments/status/
Authorization: Bearer <jwt_token>

Response:
{
  "has_purchased": true,
  "purchase_date": "2025-01-15T10:30:00Z"
}
```

## Frontend Integration

### Checkout Button Example

```tsx
'use client'

import { loadStripe } from '@stripe/stripe-js'
import axios from 'axios'

const stripePromise = loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY!)

export function CheckoutButton() {
  const handleCheckout = async () => {
    const token = localStorage.getItem('access_token')
    const response = await axios.post(
      '/api/payments/create-checkout/',
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    )

    const stripe = await stripePromise
    await stripe!.redirectToCheckout({
      sessionId: response.data.sessionId
    })
  }

  return (
    <button onClick={handleCheckout}>
      Kup teraz - 49 zł
    </button>
  )
}
```

## Subscription Models

For subscription-based apps (AirAware Polska, PolishWriter, CenWatch PL):

### Create Subscription

```python
# backend/core/payments.py
checkout_session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_monthly_subscription_id',  # Create in Stripe Dashboard
        'quantity': 1,
    }],
    mode='subscription',  # Not 'payment'
    success_url=settings.FRONTEND_URL + '/subscription/success',
    cancel_url=settings.FRONTEND_URL + '/pricing',
)
```

### Handle Subscription Events

```python
# In webhook handler
if event['type'] == 'customer.subscription.created':
    # Activate user's subscription
    pass
elif event['type'] == 'customer.subscription.deleted':
    # Deactivate user's subscription
    pass
```

## Security Best Practices

1. **Never expose secret keys**
   - Keep `STRIPE_SECRET_KEY` server-side only
   - Use `.env` files (already in `.gitignore`)

2. **Verify webhooks**
   - Always validate webhook signatures
   - Use `STRIPE_WEBHOOK_SECRET`

3. **Use HTTPS in production**
   - Stripe requires HTTPS for webhooks
   - Get free SSL with Let's Encrypt

4. **Validate amounts**
   - Never trust client-side prices
   - Always set prices server-side

## Production Checklist

Before going live:

- [ ] Switch to live API keys (`pk_live_...`, `sk_live_...`)
- [ ] Set up production webhook endpoint
- [ ] Enable SSL/HTTPS
- [ ] Test live mode with real card (small amount)
- [ ] Set up Stripe email notifications
- [ ] Configure tax settings (if applicable)
- [ ] Set up refund policy
- [ ] Enable fraud prevention (Radar)
- [ ] Add terms of service link
- [ ] Test subscription cancellation flow
- [ ] Set up customer support email

## Troubleshooting

### Payment succeeds but webhook doesn't fire

- Check webhook endpoint is accessible
- Verify webhook signature is correct
- Check Stripe Dashboard → Webhooks → Event logs

### "Invalid API key" error

- Ensure you're using correct environment (test vs live)
- Check key is not expired
- Verify no extra spaces in `.env` file

### 3D Secure failing

- Use test card `4000 0025 0000 3155`
- Ensure frontend handles redirect properly
- Check Stripe Dashboard for details

### Subscription not activating

- Verify webhook event `customer.subscription.created` is processed
- Check database for subscription record
- Review webhook logs in Stripe Dashboard

## Support

- **Stripe Docs**: [stripe.com/docs](https://stripe.com/docs)
- **Stripe Support**: [support.stripe.com](https://support.stripe.com)
- **Test Mode**: Use test keys for development
- **Dashboard**: Monitor all payments at [dashboard.stripe.com](https://dashboard.stripe.com)

## Polish Payment Methods

Stripe supports popular Polish payment methods:

- **Credit/Debit Cards**: Visa, Mastercard
- **P24 (Przelewy24)**: Popular in Poland
- **BLIK**: Mobile payment method
- **Bank transfers**: Available for larger amounts

To enable:
1. Go to Stripe Dashboard → Settings → Payment methods
2. Enable desired methods
3. Update checkout session to include them

```python
payment_method_types=['card', 'p24', 'blik']
```

---

**Ready to accept payments!** 🚀

For questions or issues, check the Stripe documentation or contact support.
