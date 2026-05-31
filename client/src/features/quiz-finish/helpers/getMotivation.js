export function getMotivation(percent) {
  if (percent >= 90) {
    return 'Фантастический результат! Попробуйте более сложный квиз.'
  }

  if (percent >= 70) {
    return 'Отличная база знаний. Следующий квиз ждёт!'
  }

  return 'Каждая попытка помогает учиться. Попробуйте ещё раз.'
}
