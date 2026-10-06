import { createFileRoute } from '@tanstack/react-router'
import SettingNotificationPage from 'pages/setting/notification'

export const Route = createFileRoute('/{-$locale}/setting/notification')({ component: SettingNotificationPage })
