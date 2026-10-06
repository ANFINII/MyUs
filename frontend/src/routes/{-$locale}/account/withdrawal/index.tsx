import { createFileRoute } from '@tanstack/react-router'
import WithdrawalPage from 'pages/account/withdrawal'

export const Route = createFileRoute('/{-$locale}/account/withdrawal/')({ component: WithdrawalPage })
