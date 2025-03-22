import axios, { AxiosResponse } from 'axios'
import { ok, err } from 'neverthrow'
import type { Result } from 'neverthrow'

export interface ApiError {
  status: number
  message?: string
}

export type ApiOut<T> = Result<T, ApiError>

export const apiOut = async <T>(apiCall: Promise<AxiosResponse<T>>): Promise<ApiOut<T>> => {
  try {
    const res = await apiCall
    return ok(res.data)
  } catch (e) {
    if (axios.isAxiosError(e)) {
      return err({ status: e.response?.status ?? 500, message: e.message })
    }
    return err({ status: 500, message: 'Unknown Error' })
  }
}
