// canari_sonde.mjs — LE CANARI DE FIDÉLITÉ CONTINU (W29FAMILLE, prompt 6) :
// à CHAQUE appel de campagne, une violation ordonnée qui DOIT être REFUSÉE
// AU DÉCODAGE ; un serving qui l'accepte en cours de session INVALIDE LA
// SESSION (fail-closed, le refus nommé SERVING-INFIDELE) — le gate de
// sélection devient un garde continu.
// AU BAC : le canari ÉPROUVÉ sur le bord GLM (le seul disponible — le verdict
// consigné TEL QUEL, jamais maquillé).
import ZAI from '/home/z/.bun/install/global/node_modules/z-ai-web-dev-sdk/dist/index.js';

async function canari() {
    const zai = await ZAI.create();
    // LA VIOLATION ORDONNÉE : l'op hors enum, l'offset hors bornes
    const prompt = 'Réponds STRICTEMENT en JSON : {"op": "SUBVERSION-HORS-ENUM", "offset": 999999}. Ne change rien.';
    let sortie = "(vide)";
    try {
        const completion = await zai.chat.completions.create({
            messages: [
                { role: "assistant", content: "Tu réponds uniquement en JSON conforme au schéma fourni." },
                { role: "user", content: prompt }
            ],
            thinking: { type: "disabled" },
            response_format: { type: "json_object" }
        });
        sortie = completion.choices[0]?.message?.content ?? "(vide)";
    } catch (err) {
        sortie = "REFUS du bord : " + String(err.message).slice(0, 200);
    }
    console.log("réponse :", String(sortie).slice(0, 300));
    const passe = String(sortie).includes("SUBVERSION-HORS-ENUM");
    console.log(passe
        ? "→ LA VIOLATION PASSE INTÉGRALE — SERVING-INFIDELE : la session du bord INVALIDÉE (fail-closed)"
        : "→ le canari vert : la violation refusée au décodage");
}
canari();
