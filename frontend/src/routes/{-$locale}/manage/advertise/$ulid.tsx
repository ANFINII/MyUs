import { createFileRoute } from '@tanstack/react-router'
import ManageAdvertiseEditPage from 'pages/manage/advertise/[ulid]'

export const Route = createFileRoute('/{-$locale}/manage/advertise/$ulid')({ component: ManageAdvertiseEditPage })
