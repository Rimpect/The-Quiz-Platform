export function QuestionMedia({ type, url }) {
  if (!url) return null

  if (type === 'image') {
    return <img src={url} />
  }

  if (type === 'video') {
    return <video src={url} controls />
  }

  if (type === 'audio') {
    return <audio src={url} controls />
  }

  return null
}
