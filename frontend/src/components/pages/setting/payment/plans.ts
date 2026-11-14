import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    features: [{ key: 'individualAds', count: 1 }, { key: 'hideGlobalAds' }],
  },
  {
    name: 'Standard',
    features: [{ key: 'individualAds', count: 2 }, { key: 'hideGlobalAds' }],
  },
  {
    name: 'Premium',
    features: [{ key: 'individualAds', count: 3 }, { key: 'hideGlobalAds' }, { key: 'musicDownload' }],
  },
  {
    name: 'Free',
    features: [{ key: 'basic' }, { key: 'withAds' }],
  },
]
