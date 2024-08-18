import Api from '../utils/Api/Api'

const api: Api = new Api()

export default {
  install: (Vue: any): void => {
    Vue.provide('$api', api)
  }
}
