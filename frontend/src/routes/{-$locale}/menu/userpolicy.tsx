import { createFileRoute } from '@tanstack/react-router'
import UserPolicyPage from 'pages/menu/userpolicy'

export const Route = createFileRoute('/{-$locale}/menu/userpolicy')({ component: UserPolicyPage })
