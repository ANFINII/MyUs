import { createFileRoute } from '@tanstack/react-router'
import SignupEmailPage from 'pages/account/signup/email'

export const Route = createFileRoute('/{-$locale}/account/signup/email')({ component: SignupEmailPage })
