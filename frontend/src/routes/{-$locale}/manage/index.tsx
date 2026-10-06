import { createFileRoute } from '@tanstack/react-router'
import ManagePage from 'pages/manage'

export const Route = createFileRoute('/{-$locale}/manage/')({ component: ManagePage })
