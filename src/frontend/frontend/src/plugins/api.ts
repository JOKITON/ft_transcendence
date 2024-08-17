import Api from '../utils/Api/Api'

const api: Api<any, any> = new Api<any, any>()

export default {
  install: (Vue: any): void => {
    Vue.provide('$api', api)
  }
}
