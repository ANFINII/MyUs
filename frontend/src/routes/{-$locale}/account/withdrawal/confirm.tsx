import { createFileRoute } from '@tanstack/react-router'
import WithdrawalConfirmPage from 'pages/account/withdrawal/confirm'

export const Route = createFileRoute('/{-$locale}/account/withdrawal/confirm')({ component: WithdrawalConfirmPage })
