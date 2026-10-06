import { createFileRoute } from '@tanstack/react-router'
import SettingMypageEditPage from 'pages/setting/mypage/edit'

export const Route = createFileRoute('/{-$locale}/setting/mypage/edit')({ component: SettingMypageEditPage })
