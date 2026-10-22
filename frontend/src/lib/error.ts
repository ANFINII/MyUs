import axios, { AxiosResponse } from 'axios'
import { ok, err } from 'neverthrow'
import { Result } from 'neverthrow'
import { ErrorType, FetchError } from 'utils/constants/enum'

export interface ApiError {
  status: number
  type?: ErrorType
  message?: string
}

export type ApiOut<T> = Result<T, ApiError>

const toErrorType = (value: unknown): ErrorType | undefined => {
  return Object.values(ErrorType).find((type) => type === value)
}

export const toErrorMessage = (error: ApiError, fallback: FetchError): string => {
  return error.message?.startsWith('error.') ? error.message : fallback
}

export const apiOut = async <T>(apiCall: Promise<AxiosResponse<T>>): Promise<ApiOut<T>> => {
  try {
    const res = await apiCall
    return ok(res.data)
  } catch (e) {
    if (axios.isAxiosError(e)) {
      const data = e.response?.data
      return err({ status: e.response?.status ?? 500, type: toErrorType(data?.type), message: data?.message })
    }
    return err({ status: 500, message: FetchError.Error })
  }
}
