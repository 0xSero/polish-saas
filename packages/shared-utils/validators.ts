/**
 * Validate Polish email
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

/**
 * Validate Polish phone number
 */
export function isValidPhonePL(phone: string): boolean {
  const cleaned = phone.replace(/\D/g, '')
  return cleaned.length === 9 || (cleaned.length === 11 && cleaned.startsWith('48'))
}

/**
 * Validate Polish postal code
 */
export function isValidPostalCodePL(code: string): boolean {
  const postalCodeRegex = /^\d{2}-\d{3}$/
  return postalCodeRegex.test(code)
}

/**
 * Validate Polish PESEL (national identification number)
 */
export function isValidPESEL(pesel: string): boolean {
  if (!/^\d{11}$/.test(pesel)) return false

  const weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
  const digits = pesel.split('').map(Number)

  const checksum = digits.slice(0, 10).reduce((sum, digit, i) => {
    return sum + digit * weights[i]
  }, 0)

  const controlDigit = (10 - (checksum % 10)) % 10
  return controlDigit === digits[10]
}

/**
 * Validate password strength
 */
export function isStrongPassword(password: string): boolean {
  // At least 8 characters, 1 uppercase, 1 lowercase, 1 number
  const strongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$/
  return strongPasswordRegex.test(password)
}
