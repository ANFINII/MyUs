import { createFileRoute } from '@tanstack/react-router'
import PasswordChangePage from 'pages/setting/password/change'

export const Route = createFileRoute('/{-$locale}/setting/password/change')({ component: PasswordChangePage })
