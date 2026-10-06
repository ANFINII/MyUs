import { createFileRoute } from '@tanstack/react-router'
import PaymentSuccessPage from 'pages/setting/payment/success'

export const Route = createFileRoute('/{-$locale}/setting/payment/success')({ component: PaymentSuccessPage })
