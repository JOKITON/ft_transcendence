export default interface IKeyboard {
  keys: Set<string>

  addKey(key: string): void
}
