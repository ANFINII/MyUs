import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    features: [{ key: 'series' }, { key: 'playlist' }, { key: 'individualAds', count: 1 }],
  },
  {
    name: 'Standard',
    features: [{ key: 'series' }, { key: 'playlist' }, { key: 'individualAds', count: 2 }, { key: 'hideGlobalAds' }, { key: 'paidContent' }],
  },
  {
    name: 'Premium',
    features: [{ key: 'series' }, { key: 'playlist' }, { key: 'individualAds', count: 3 }, { key: 'hideGlobalAds' }, { key: 'paidContent' }, { key: 'musicDownload' }],
  },
  {
    name: 'Free',
    features: [{ key: 'basic' }, { key: 'withAds' }],
  },
]
