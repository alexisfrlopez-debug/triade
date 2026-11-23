#!/usr/bin/env bun
// appel_contraint.js — LE PONT SDK (81eruqtl6, la campagne du décodage
// contraint) : le même appel que le CLI `z-ai chat` MAIS PAR LE SDK
// DIRECTEMENT, avec LE CHAMP response_format QUE LE CLI N'EXPOSE PAS
// (l'écart d'instrument nommé aux rapports v5/v6 — le SDK 0.0.18 laisse
// passer les champs additionnels : CreateChatCompletionBody à l'index
// ouvert [key: string]: any, le constat à la congélation du présent
// plan). LE JUGE N'EST JAMAIS ICI — l'émission seule.
//
// Usage : bun appel_contraint.js <fichier-prompt> <fichier-schéma|-> <fichier-sortie>
//   <fichier-prompt>  le prompt complet (l'utilisateur), lu du fichier
//   <fichier-schéma>  l'objet response_format EN JSON (« - » = sans)
//   <fichier-sortie>  la réponse API complète (id, model, usage, choices)
// Sortie : exit 0 + la réponse au fichier ; exit 1 + l'erreur à stderr.
import fs from 'fs';

const [promptPath, schemaPath, outPath] = process.argv.slice(2);
if (!promptPath || !outPath) {
    console.error('usage: bun appel_contraint.js <prompt> <schema|-> <out>');
    process.exit(1);
}

const { default: ZAI } = await import(
    '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js');

const prompt = fs.readFileSync(promptPath, 'utf-8');
const body = {
    messages: [{ role: 'user', content: prompt }],
    thinking: { type: 'disabled' },      // le défaut du CLI, reconduit
};
if (schemaPath && schemaPath !== '-') {
    body.response_format = JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
}

try {
    const client = await ZAI.create();
    const reponse = await client.chat.completions.create(body);
    fs.writeFileSync(outPath, JSON.stringify(reponse, null, 1));
} catch (e) {
    // l'erreur VERBATIM (le 400 d'un champ refusé, le corps rendu) —
    // la sonde en fait son pièce, jamais étouffée
    console.error('ERREUR_APPEL: ' + String(e && e.message ? e.message : e));
    process.exit(1);
}
