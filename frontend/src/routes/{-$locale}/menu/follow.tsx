import { createFileRoute } from '@tanstack/react-router'
import FollowsPage from 'pages/menu/follow'

export const Route = createFileRoute('/{-$locale}/menu/follow')({ component: FollowsPage })
