import { Plan } from './PlanCard'

export const plans: Plan[] = [
  {
    name: 'Basic',
    features: [{ key: 'individualAds', count: 1 }, { key: 'hideGlobalAds' }, { key: 'playlist' }, { key: 'series' }],
  },
  {
    name: 'Standard',
    features: [{ key: 'individualAds', count: 2 }, { key: 'hideGlobalAds' }, { key: 'playlist' }, { key: 'series' }],
  },
  {
    name: 'Premium',
    features: [{ key: 'individualAds', count: 3 }, { key: 'hideGlobalAds' }, { key: 'playlist' }, { key: 'series' }, { key: 'musicDownload' }],
  },
  {
    name: 'Free',
    features: [{ key: 'basic' }, { key: 'withAds' }],
  },
]
