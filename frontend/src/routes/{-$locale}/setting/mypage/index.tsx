import { createFileRoute } from '@tanstack/react-router'
import SettingMypagePage from 'pages/setting/mypage'

export const Route = createFileRoute('/{-$locale}/setting/mypage/')({ component: SettingMypagePage })
