// La sonde du serving à structured output (W27DECCO, P4) — le test décisif :
// un schéma STRICT posé au bord, une violation ORDONNÉE (op hors enum).
// Si le bord renvoie la violation, le schéma n'est pas appliqué : SERVING-ABSENT.
import ZAI from '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';

const SCHEMA = {
  type: "json_schema",
  json_schema: {
    name: "triale_op",
    strict: true,
    schema: {
      type: "object",
      additionalProperties: false,
      required: ["op", "offset"],
      properties: {
        op: { type: "string", enum: ["mov", "add"] },
        offset: { type: "integer", minimum: 0, maximum: 65535 }
      }
    }
  }
};

async function sonde() {
  const zai = await ZAI.create();
  // La violation ordonnée : « op » hors enum, « offset » hors bornes.
  const essais = [
    { nom: "json_schema strict + violation ordonnée",
      params: { response_format: SCHEMA },
      prompt: 'Réponds STRICTEMENT en JSON : {"op": "SUBVERSION-HORS-ENUM", "offset": 999999}. Ne change rien.' },
    { nom: "json_object simple",
      params: { response_format: { type: "json_object" } },
      prompt: 'Réponds STRICTEMENT en JSON un objet {"op": "SUBVERSION-HORS-ENUM", "offset": 999999}.' },
  ];
  for (const e of essais) {
    try {
      const completion = await zai.chat.completions.create({
        messages: [
          { role: "assistant", content: "Tu réponds uniquement en JSON conforme au schéma fourni." },
          { role: "user", content: e.prompt }
        ],
        thinking: { type: "disabled" },
        ...e.params
      });
      const contenu = completion.choices[0]?.message?.content ?? "(vide)";
      const usage = completion.usage ?? null;
      console.log(`=== ${e.nom} ===`);
      console.log("réponse :", String(contenu).slice(0, 300));
      console.log("usage :", JSON.stringify(usage));
      const horsEnum = String(contenu).includes("SUBVERSION-HORS-ENUM");
      console.log(horsEnum
        ? "→ LE SCHÉMA N'EST PAS APPLIQUÉ (la violation ordonnée passe)"
        : "→ le schéma semble appliqué (la violation ne passe pas)");
    } catch (err) {
      console.log(`=== ${e.nom} ===`);
      console.log("REFUS du bord :", String(err.message).slice(0, 300));
    }
  }
}
sonde();
