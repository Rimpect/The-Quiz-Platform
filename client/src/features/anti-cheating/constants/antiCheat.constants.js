export const ANTI_CHEAT_CONFIG = {
  MAX_WARNINGS: 3,
  HEARTBEAT_INTERVAL: 5000,
  TAB_SWITCH_WARNING: 'Предупреждение! Не переключайте вкладки',
  COPY_PASTE_WARNING: 'Копирование и вставка запрещены',
  DEV_TOOLS_WARNING: 'Инструменты разработчика обнаружены',

  DEFAULT_SETTINGS: {
    maxWarnings: 3,
    autoSubmitOnViolation: true,
    blockCopyPaste: true,
    blockDevTools: true,
    requireFullscreen: true,
    logViolations: true,
  },
}
