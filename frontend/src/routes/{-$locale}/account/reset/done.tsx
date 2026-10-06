import { createFileRoute } from '@tanstack/react-router'
import ResetDonePage from 'pages/account/reset/done'

export const Route = createFileRoute('/{-$locale}/account/reset/done')({ component: ResetDonePage })
