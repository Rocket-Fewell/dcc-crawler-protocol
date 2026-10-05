// Prints environment diagnostics: Node version, voice dependency report (opus, encryption, DAVE, ffmpeg).
import { generateDependencyReport } from '@discordjs/voice';

const [major, minor] = process.versions.node.split('.').map(Number);
if (major < 22 || (major === 22 && minor < 12)) {
  console.warn(`WARNING: Node ${process.versions.node} detected; @discordjs/voice 0.19 (DAVE support) needs Node >= 22.12.0\n`);
}
console.log(generateDependencyReport());
