import { createFileRoute } from '@tanstack/react-router'
import LoginPage from 'pages/account/login'

export const Route = createFileRoute('/{-$locale}/account/login')({ component: LoginPage })
