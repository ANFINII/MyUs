import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/{-$locale}/media/chat/$ulid/thread/$messageUlid')({ component: () => null })
