import { apiClient } from 'lib/axios/internal'
import { cookieHeader } from 'lib/config'
import { ApiOut, apiOut } from 'lib/error'
import { Req } from 'types/global'
import { Category } from 'types/internal/category'
import { apiMediaCategory } from 'api/uri'

export const getCategories = async (req?: Req): Promise<ApiOut<Category[]>> => {
  return await apiOut(apiClient('json').get(apiMediaCategory, cookieHeader(req)))
}
