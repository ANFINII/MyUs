import { createFileRoute } from '@tanstack/react-router'
import AdvertiseCreatePage from 'pages/manage/advertise/create'

export const Route = createFileRoute('/{-$locale}/manage/advertise/create')({ component: AdvertiseCreatePage })
