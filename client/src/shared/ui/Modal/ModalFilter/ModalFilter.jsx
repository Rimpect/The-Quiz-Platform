import React from 'react'

import { Button } from '@shared'
import { X } from 'lucide-react'

import styles from './ModalFilter.module.scss'
import {
  DIFFICULTY_OPTIONS,
  TYPE_QUESTION_OPTIONS,
  MEDIA_OPTIONS,
} from './model/filterOptions'
import {
  useFilterDraft,
  QUESTION_MIN,
  QUESTION_MAX,
  DURATION_MIN,
  DURATION_MAX,
} from './model/useFilterDraft'
import {
  FilterSection,
  CheckboxItem,
  RadioItem,
  RangeField,
} from './ui/FilterControls'

export function ModalFilter({
  isOpen,
  onClose,
  onApply,
  onReset,
  filter,
  categories = [],
}) {
  if (!isOpen) return null
  return (
    <ModalFilterContent
      onClose={onClose}
      onApply={onApply}
      onReset={onReset}
      filter={filter}
      categories={categories}
    />
  )
}

function ModalFilterContent({ onClose, onApply, onReset, filter, categories }) {
  const {
    draftFilters,
    toggleArrayValue,
    setDifficulty,
    setQuestionCount,
    setDuration,
    validationError,
    reset,
    apply,
  } = useFilterDraft(filter, { onApply, onReset, onClose })

  const categoryNames = categories
    .map((c) => c.category_type || c)
    .filter(Boolean)

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.content} onClick={(e) => e.stopPropagation()}>
        <div className={styles.header}>
          <h2 className={styles.title}>Фильтры квизов</h2>
          <button className={styles.closeBtn} onClick={onClose}>
            <X className={styles.closeIcon} />
          </button>
        </div>

        <div className={styles.body}>
          <FilterSection label="Категории">
            <div className={styles.categoriesGrid}>
              {categoryNames.map((category) => (
                <CheckboxItem
                  key={category}
                  id={`cat-${category}`}
                  label={category}
                  checked={draftFilters.categories.includes(category)}
                  onChange={() => toggleArrayValue('categories', category)}
                />
              ))}
            </div>
          </FilterSection>

          <FilterSection label="Сложность">
            <div className={styles.radioGroup}>
              {DIFFICULTY_OPTIONS.map((opt) => (
                <RadioItem
                  key={opt.id}
                  id={opt.id}
                  name="difficulty"
                  label={opt.label}
                  checked={
                    opt.value === 'all'
                      ? draftFilters.difficulty === null
                      : draftFilters.difficulty === opt.value
                  }
                  onChange={() => setDifficulty(opt.value)}
                />
              ))}
            </div>
          </FilterSection>

          <FilterSection label="Тип вопросов">
            <div className={styles.checkboxGroup}>
              {TYPE_QUESTION_OPTIONS.map((opt) => (
                <CheckboxItem
                  key={opt.id}
                  id={opt.id}
                  label={opt.label}
                  checked={draftFilters.typeQuestions.includes(opt.value)}
                  onChange={() => toggleArrayValue('typeQuestions', opt.value)}
                />
              ))}
            </div>
          </FilterSection>

          <FilterSection label="Содержит медиа">
            <div className={styles.checkboxGroup}>
              {MEDIA_OPTIONS.map((opt) => (
                <CheckboxItem
                  key={opt.id}
                  id={opt.id}
                  label={opt.label}
                  icon={<opt.Icon className={styles.mediaIcon} />}
                  checked={draftFilters.mediaType.includes(opt.value)}
                  onChange={() => toggleArrayValue('mediaType', opt.value)}
                />
              ))}
            </div>
          </FilterSection>

          <RangeField
            label="Количество вопросов"
            hint={`Диапазон: ${QUESTION_MIN}–${QUESTION_MAX} вопросов`}
            min={QUESTION_MIN}
            max={QUESTION_MAX}
            fromValue={draftFilters.numberOfQuestionsFrom}
            toValue={draftFilters.numberOfQuestionsTo}
            onFromChange={(v) => setQuestionCount('numberOfQuestionsFrom', v)}
            onToChange={(v) => setQuestionCount('numberOfQuestionsTo', v)}
          />

          <RangeField
            label="Длительность (мин)"
            hint={`Диапазон: ${DURATION_MIN}–${DURATION_MAX} минут`}
            min={DURATION_MIN}
            max={DURATION_MAX}
            fromValue={draftFilters.durationFrom}
            toValue={draftFilters.durationTo}
            onFromChange={(v) => setDuration('durationFrom', v)}
            onToChange={(v) => setDuration('durationTo', v)}
          />

          {validationError && (
            <p className={styles.errorText}>{validationError}</p>
          )}
        </div>

        <div className={styles.footer}>
          <Button variant="white" fullWidth onClick={reset}>
            Сбросить все
          </Button>
          <Button
            variant="black"
            fullWidth
            onClick={apply}
            disabled={Boolean(validationError)}
          >
            Применить фильтры
          </Button>
        </div>
      </div>
    </div>
  )
}
