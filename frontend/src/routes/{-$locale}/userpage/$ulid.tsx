import { createFileRoute } from '@tanstack/react-router'
import UserpagePage from 'pages/userpage/[ulid]'

export const Route = createFileRoute('/{-$locale}/userpage/$ulid')({ component: UserpagePage })
