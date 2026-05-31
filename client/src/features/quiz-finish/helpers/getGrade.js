export function getGrade(percent) {
  if (percent >= 90) return 'A'
  if (percent >= 80) return 'B'
  if (percent >= 70) return 'C'
  if (percent >= 60) return 'D'

  return 'F'
}
