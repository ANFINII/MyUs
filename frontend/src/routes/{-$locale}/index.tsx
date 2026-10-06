import { createFileRoute } from '@tanstack/react-router'
import HomesPage from 'pages/index'

export const Route = createFileRoute('/{-$locale}/')({ component: HomesPage })
