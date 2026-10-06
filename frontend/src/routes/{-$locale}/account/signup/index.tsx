import { createFileRoute } from '@tanstack/react-router'
import SignupPage from 'pages/account/signup'

export const Route = createFileRoute('/{-$locale}/account/signup/')({ component: SignupPage })
