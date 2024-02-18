import { HttpStatusCode } from 'axios'
import { apiAddressClient } from 'lib/axios'
import { AddressResult } from 'types/internal/address'
import { apiAddress } from './uri'

// 住所検索APIリファレンス: http://zipcloud.ibsnet.co.jp/doc/api
export const getAddressForm = async (zipcode: string) => {
  const data = await apiAddressClient.get(apiAddress, { params: { zipcode } }).then((res) => {
    if (res.status !== HttpStatusCode.Ok) throw Error
    return res.data.results[0] as AddressResult
  })
  return data
}
