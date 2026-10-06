import { QueryClient } from '@tanstack/react-query'
import { ApiError, ApiOut } from 'lib/error'

// useQueryのerrorをApiError型として扱う
declare module '@tanstack/react-query' {
  interface Register {
    defaultError: ApiError
  }
}

// TanStack Queryはエラーをthrowで扱うため、Result型をthrowに変換する
export const toQuery = async <T>(apiCall: Promise<ApiOut<T>>): Promise<T> => {
  const ret = await apiCall
  if (ret.isErr()) throw ret.error
  return ret.value
}

const MAX_RETRY = 1

// 5xxに加え、レスポンスのないネットワークエラー（apiOutでstatus: 500に変換）も一時的な障害としてリトライする
const shouldRetry = (failureCount: number, error: ApiError): boolean => {
  return error.status >= 500 && failureCount < MAX_RETRY
}

export const createQueryClient = (): QueryClient => {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // SSRと同じく、ページを開くたびに最新を取得する（キャッシュは取得完了までの表示に使う）
        staleTime: 0,
        refetchOnWindowFocus: false,
        retry: shouldRetry,
      },
    },
  })
}
