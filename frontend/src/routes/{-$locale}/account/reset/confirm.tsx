import { createFileRoute } from '@tanstack/react-router'
import ResetConfirmPage from 'pages/account/reset/confirm'

export const Route = createFileRoute('/{-$locale}/account/reset/confirm')({ component: ResetConfirmPage })
