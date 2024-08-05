export function validateForm(form: any) {
  if (form.password.length < 8) {
    throw new Error('Password must be at least 8 characters long')
  } else if (!validateEmail(form.email)) {
    throw new Error('Invalid email format')
  } else if (form.password !== form.password_confirm) {
    throw new Error('Passwords do not match.')
  }
}

function validateEmail(email: string): boolean {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}
