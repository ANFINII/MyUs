import { createFileRoute } from '@tanstack/react-router'
import PasswordChangeDonePage from 'pages/setting/password/change-done'

export const Route = createFileRoute('/{-$locale}/setting/password/change-done')({ component: PasswordChangeDonePage })
