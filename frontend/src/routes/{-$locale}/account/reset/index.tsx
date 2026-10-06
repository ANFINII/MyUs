import { createFileRoute } from '@tanstack/react-router'
import ResetPage from 'pages/account/reset'

export const Route = createFileRoute('/{-$locale}/account/reset/')({ component: ResetPage })
