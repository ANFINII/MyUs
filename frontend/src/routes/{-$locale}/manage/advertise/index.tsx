import { createFileRoute } from '@tanstack/react-router'
import ManageAdvertisesPage from 'pages/manage/advertise'

export const Route = createFileRoute('/{-$locale}/manage/advertise/')({ component: ManageAdvertisesPage })
