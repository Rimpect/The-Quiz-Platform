import { Input } from '@shared'

import styles from '../ModalFilter.module.scss'

export function FilterSection({ label, children }) {
  return (
    <div className={styles.section}>
      <label className={styles.label}>{label}</label>
      {children}
    </div>
  )
}

export function CheckboxItem({ id, label, checked, onChange, icon = null }) {
  return (
    <div className={styles.checkboxItem}>
      <input
        type="checkbox"
        id={id}
        className={styles.checkboxInput}
        checked={checked}
        onChange={onChange}
      />
      {icon}
      <label htmlFor={id} className={styles.checkboxLabel}>
        {label}
      </label>
    </div>
  )
}

export function RadioItem({ id, name, label, checked, onChange }) {
  return (
    <div className={styles.radioItem}>
      <input
        type="radio"
        name={name}
        id={id}
        className={styles.radioInput}
        checked={checked}
        onChange={onChange}
      />
      <label htmlFor={id} className={styles.radioLabel}>
        {label}
      </label>
    </div>
  )
}

export function RangeField({
  label,
  hint,
  min,
  max,
  fromValue,
  toValue,
  onFromChange,
  onToChange,
}) {
  return (
    <div className={styles.section}>
      <label className={styles.label}>{label}</label>
      <div className={styles.rangeRow}>
        <div className={styles.rangeField}>
          <label className={styles.rangeLabel}>От</label>
          <Input
            type="number"
            min={min}
            max={max}
            value={fromValue}
            className={styles.numberInput}
            onChange={(e) => onFromChange(e.target.value)}
          />
        </div>
        <div className={styles.rangeField}>
          <label className={styles.rangeLabel}>До</label>
          <Input
            type="number"
            min={min}
            max={max}
            value={toValue}
            className={styles.numberInput}
            onChange={(e) => onToChange(e.target.value)}
          />
        </div>
      </div>
      <p className={styles.hintText}>{hint}</p>
    </div>
  )
}
