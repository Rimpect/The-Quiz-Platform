export function getMessage(percent) {
  if (percent >= 90) return 'Превосходный результат!'

  if (percent >= 80) return 'Отличная работа!'

  if (percent >= 70) return 'Хороший результат!'

  if (percent >= 60) return 'Неплохо, но есть куда расти'

  return 'Попробуйте еще раз'
}
