import { createFileRoute } from '@tanstack/react-router'
import PaymentPage from 'pages/setting/payment'

export const Route = createFileRoute('/{-$locale}/setting/payment/')({ component: PaymentPage })
