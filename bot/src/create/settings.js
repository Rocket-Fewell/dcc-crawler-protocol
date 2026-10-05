/** Per-session /create settings, read from <data>/session.json -> "create": {...}. Defaults are the spec's. */
import { readProfile } from '../session.js';
import { layerFlags } from './layers.js';

export function createSettings(config) {
  const id = config.campaign.sessionId;
  const c = readProfile(id, { ...process.env, DCC_CAMPAIGN_DIR: config.campaign.dir })?.create ?? {};
  const mode = ['off', 'notify', 'hold'].includes(c.review_mode) ? c.review_mode : id === 'alpha' ? 'off' : 'hold';
  return {
    reviewMode: mode,
    allowRoll: typeof c.allow_roll === 'boolean' ? c.allow_roll : true, // decision 024: the Roll method is ON unless the session says false
    speciesClassReskin: c.species_class_reskin === true, // flavor names for species/classes (tables/species-class-reskins.json): OFF unless the session says true (Caleb has not approved the names yet)
    backgroundReskin: c.background_reskin === true, // flavor names for S7 backgrounds/feats/bonus choices/gear packages (tables/background-reskins.json): OFF unless the session says true (Caleb has not approved them yet)
    layers: layerFlags(c),   // { layerId: true|false } for every registered display layer (layers.js): ON only when create.<flag> is exactly true
    contentSource: c.content_source === 'srd' ? 'srd' : 'phb', // Open Q7 default: 2024 PHB
    staffChannelId: c.staff_channel_id || null,
    reviewerIds: Array.isArray(c.reviewer_ids) ? c.reviewer_ids.map(String) : [],
  };
}
