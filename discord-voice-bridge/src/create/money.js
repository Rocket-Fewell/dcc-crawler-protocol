/**
 * Money WORDS for /create: one currency, "credits" (Core 5.10: 1 credit = 1 GP; 1 cp = 0.01 credit). DISPLAY ONLY.
 * Nothing here is ever read back by price math: totals, ledger rows, package values and the {gp} placeholder keep their original integer values
 * (rules.js sums integer coin values; cartLineCost rounds as it always did). These helpers only format text for the player, at the last moment.
 */

/** 5 -> "5", 0.05 -> "0.05", 12.5 -> "12.5" (at most two decimals; cp are integers so two are always exact). Formatting only. */
export function fmtCredits(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return String(value);
  return Number.isInteger(n) ? String(n) : n.toFixed(2).replace(/0+$/, '').replace(/\.$/, '');
}
/** "1 credit" / "5 credits" / "0.05 credits" from a credit amount. */
export const creditsText = (value) => `${fmtCredits(value)} ${Number(value) > 0 && Number(value) <= 1 ? 'credit' : 'credits'}`;   // Lore's unit rule: singular for an amount of 1 or less (0 stays plural)
/** A price held as integer copper, shown in credits (100 cp = 1 credit). The integer is never changed or rounded; null/undefined = "n/a". */
export const cpText = (cp) => (cp === null || cp === undefined ? 'n/a' : creditsText(cp / 100));

const num = (s) => Number(String(s).replace(/,/g, ''));
/**
 * Rewrite the money words of one display string: "8 GP" -> "8 credits", "5 cp" -> "0.05 credits", "gold"/"cash"/"GP" -> "credits", and drops the "(1 gold = 1 credit)" aside.
 * Apply it only to money sentences the bridge shows (labels, hints, help), never to names (Gold Dragonborn) and never to data that is stored or summed.
 */
export function money(text) {
  return String(text ?? '')
    .replace(/\s*\(1 gold = 1 credit\)/gi, '')
    .replace(/(\d[\d,]*(?:\.\d+)?)\s*gp\b/gi, (_, n) => creditsText(num(n)))
    .replace(/(\d[\d,]*)\s*cp\b/g, (_, n) => creditsText(num(n) / 100))
    .replace(/\bGold option\b/g, 'Credits option')
    .replace(/\b(gold|cash|gp|cp)\b/g, 'credits')
    .replace(/\b(Gold|Cash|GP|CP)\b/g, 'Credits')
    .replace(/(?<![\d.,])(1(?:\.0+)?|0\.\d+)\s+credits\b/g, '$1 credit');   // "1 credits" / "0.5 credits" -> singular
}

/** money() on a string that also carries a player-facing name that must not be touched: the name is swapped for a token while rewriting. */
export const TOKEN = '\u0001OWNER\u0001';
export const moneyKeeping = (text, name) => money(text).split(TOKEN).join(name);
