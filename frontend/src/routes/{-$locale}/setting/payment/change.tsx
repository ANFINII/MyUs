import { createFileRoute } from '@tanstack/react-router'
import PaymentChangePage from 'pages/setting/payment/change'

export const Route = createFileRoute('/{-$locale}/setting/payment/change')({ component: PaymentChangePage })
