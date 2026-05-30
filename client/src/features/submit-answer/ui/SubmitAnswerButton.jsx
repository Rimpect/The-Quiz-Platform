export function SubmitAnswerButton({ disabled, onSubmit }) {
  return (
    <button disabled={disabled} onClick={onSubmit}>
      Ответить
    </button>
  )
}
