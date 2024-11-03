import Socket from '../utils/socket/imp/socket'

const socket: Socket = new Socket()

export default {
  install: (Vue: any): void => {
    Vue.provide('$socket', socket)
  }
}
