const LEVELS = { debug: 10, info: 20, warn: 30, error: 40 };

/** Tiny leveled logger (no dependencies). */
export function createLogger(level = 'info', scope = '') {
  const threshold = LEVELS[level] ?? LEVELS.info;
  const emit = (lvl, args) => {
    if (LEVELS[lvl] < threshold) return;
    const ts = new Date().toISOString();
    const prefix = `${ts} ${lvl.toUpperCase().padEnd(5)}${scope ? ` [${scope}]` : ''}`;
    const fn = lvl === 'error' ? console.error : lvl === 'warn' ? console.warn : console.log;
    fn(prefix, ...args);
  };
  return {
    debug: (...a) => emit('debug', a),
    info: (...a) => emit('info', a),
    warn: (...a) => emit('warn', a),
    error: (...a) => emit('error', a),
    child: (name) => createLogger(level, scope ? `${scope}:${name}` : name),
  };
}
