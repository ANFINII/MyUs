import { createFileRoute } from '@tanstack/react-router'
import FollowersPage from 'pages/menu/follower'

export const Route = createFileRoute('/{-$locale}/menu/follower')({ component: FollowersPage })
