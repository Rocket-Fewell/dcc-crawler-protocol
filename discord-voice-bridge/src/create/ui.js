/** Small discord.js component helpers for the /create screens. Every customId is `create:<uid>:<screen>:<key>[:<arg>]`. */
import { ActionRowBuilder, ButtonBuilder, ButtonStyle, ModalBuilder, StringSelectMenuBuilder, TextInputBuilder, TextInputStyle } from 'discord.js';

export const cut = (s, n) => (String(s).length > n ? `${String(s).slice(0, n - 1)}…` : String(s));
export const cid = (uid, screen, key, arg) => ['create', uid, screen, key, arg].filter((x) => x !== undefined).join(':');

export function button(id, label, { style = ButtonStyle.Secondary, disabled = false } = {}) {
  return new ButtonBuilder().setCustomId(id).setLabel(cut(label, 80)).setStyle(style).setDisabled(disabled);
}

export const row = (...components) => new ActionRowBuilder().addComponents(...components);

/** Put `btn` on the first row that is all buttons and has room (Discord: 5 per row, 5 rows); false when there is none. Prefers the last row, then a new row. */
export function addButton(components, btn) {
  const buttonsOnly = (r) => r.components.every((c) => c instanceof ButtonBuilder);
  const last = components.at(-1);
  if (last && buttonsOnly(last) && last.components.length < 5) { last.addComponents(btn); return true; }
  if (components.length < 5) { components.push(row(btn)); return true; }
  const r = components.find((x) => buttonsOnly(x) && x.components.length < 5);
  if (r) { r.addComponents(btn); return true; }
  return false;
}

/** options: [{label, value, description?}]; selected: array of values to pre-mark. */
export function select(id, placeholder, options, { min = 1, max = 1, selected = [] } = {}) {
  const opts = options.slice(0, 25).map((o) => {
    const x = { label: cut(o.label, 100), value: String(o.value).slice(0, 100), default: selected.includes(o.value) };
    if (o.description) x.description = cut(o.description, 100);
    return x;
  });
  const m = new StringSelectMenuBuilder().setCustomId(id).setPlaceholder(cut(placeholder, 150)).addOptions(opts);
  m.setMinValues(Math.min(min, opts.length)).setMaxValues(Math.min(max, opts.length));
  return row(m);
}

/** fields: [{id, label, style?: 'short'|'paragraph', required?, max?, min?, value?, placeholder?}] */
export function modal(id, title, fields) {
  const m = new ModalBuilder().setCustomId(id).setTitle(cut(title, 45));
  for (const f of fields) {
    const t = new TextInputBuilder()
      .setCustomId(f.id)
      .setLabel(cut(f.label, 45))
      .setStyle(f.style === 'paragraph' ? TextInputStyle.Paragraph : TextInputStyle.Short)
      .setRequired(f.required !== false)
      .setMaxLength(f.max ?? 100);
    if (f.min) t.setMinLength(f.min);
    if (f.value) t.setValue(cut(f.value, f.max ?? 100));
    if (f.placeholder) t.setPlaceholder(cut(f.placeholder, 100));
    m.addComponents(row(t));
  }
  return m;
}

/** Plain text rules for typed input: no links, no mentions/markdown that would ping or break formatting. */
export function cleanText(s, max) {
  const t = String(s ?? '').replace(/\s+/g, ' ').trim();
  if (!t) return { error: 'empty' };
  if (t.length > max) return { error: `max ${max} characters` };
  if (/https?:\/\/|www\.|discord\.gg/i.test(t)) return { error: 'no links' };
  if (/[@<>`\\]|@everyone|@here/.test(t)) return { error: 'no @, <, >, backticks or backslashes' };
  return { value: t.replace(/[*_~|#]/g, '') };
}
