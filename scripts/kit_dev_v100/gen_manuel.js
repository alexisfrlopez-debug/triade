// Générateur du Manuel du Développeur — Kit de Développement Triade v1.0.0
// Conforme au skill docx : recette de couverture R1, palette DM-1,
// architecture 3 sections (couverture / sommaire romain / corps arabe).

const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, PageNumber, NumberFormat, AlignmentType, HeadingLevel,
  WidthType, BorderStyle, ShadingType, SectionType, TableOfContents,
  PageBreak, LevelFormat, TableLayoutType,
} = require("docx");
const fs = require("fs");
const path = require("path");
const { chapitres } = require("./manuel_contenu.js");

// ── Palette DM-1 (Deep Cyan — tech / IA) ─────────────────────────────────
const P = {
  bg: "162235",
  accent: "37DCF2",
  cover: {
    titleColor: "FFFFFF", subtitleColor: "B0B8C0",
    metaColor: "90989F", footerColor: "687078",
  },
  table: {
    headerBg: "1B6B7A", headerText: "FFFFFF",
    accentLine: "1B6B7A", innerLine: "C8DDE2", surface: "EDF3F5",
  },
  headingsBody: "0F2233",
  body: "000000",
  secondary: "5B6B7D",
};

const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB };
const allNoBorders = {
  top: NB, bottom: NB, left: NB, right: NB,
  insideHorizontal: NB, insideVertical: NB,
};

// ── Fonctions de couverture (design-system, obligatoires) ────────────────
function splitTitleLines(title, charsPerLine) {
  if (title.length <= charsPerLine) return [title];
  const breakAfter = new Set([
    ...",.;:!?", ..."-_/", ..." \t",
  ]);
  const lines = [];
  let remaining = title;
  while (remaining.length > charsPerLine) {
    let breakAt = -1;
    for (let i = charsPerLine; i >= Math.floor(charsPerLine * 0.6); i--) {
      if (i < remaining.length && breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
    }
    if (breakAt === -1) {
      const limit = Math.min(remaining.length, Math.ceil(charsPerLine * 1.3));
      for (let i = charsPerLine + 1; i < limit; i++) {
        if (breakAfter.has(remaining[i - 1])) { breakAt = i; break; }
      }
    }
    if (breakAt === -1) breakAt = charsPerLine;
    lines.push(remaining.slice(0, breakAt).trim());
    remaining = remaining.slice(breakAt).trim();
  }
  if (remaining) lines.push(remaining);
  if (lines.length > 1 && lines[lines.length - 1].length <= 2) {
    const last = lines.pop();
    lines[lines.length - 1] += " " + last;
  }
  return lines;
}

function calcTitleLayout(title, maxWidthTwips, preferredPt = 40, minPt = 24) {
  const charWidth = (pt) => pt * 20;
  const charsPerLine = (pt) => Math.floor(maxWidthTwips / charWidth(pt));
  let titlePt = preferredPt;
  let lines;
  while (titlePt >= minPt) {
    const cpl = charsPerLine(titlePt);
    if (cpl < 2) { titlePt -= 2; continue; }
    lines = splitTitleLines(title, cpl);
    if (lines.length <= 3) break;
    titlePt -= 2;
  }
  if (!lines || lines.length > 3) {
    lines = splitTitleLines(title, charsPerLine(minPt));
    titlePt = minPt;
  }
  return { titlePt, titleLines: lines };
}

function calcCoverSpacing(params) {
  const {
    titleLineCount = 1, titlePt = 36, hasSubtitle = false,
    hasEnglishLabel = false, metaLineCount = 0,
    fixedHeight = 800, pageHeight = 16838,
    marginTop = 0, marginBottom = 0,
  } = params;
  const SAFETY = 1200;
  const usableHeight = pageHeight - marginTop - marginBottom - SAFETY;
  const titleHeight = titleLineCount * (titlePt * 23 + 200);
  const subtitleHeight = hasSubtitle ? (12 * 23 + 600) : 0;
  const englishLabelHeight = hasEnglishLabel ? (9 * 23 + 600) : 0;
  const metaHeight = metaLineCount * (10 * 23 + 100);
  const implicitParaHeight = 3 * 300;
  const contentHeight = titleHeight + subtitleHeight + englishLabelHeight +
    metaHeight + fixedHeight + implicitParaHeight;
  const remainingSpace = usableHeight - contentHeight;
  const safeRemaining = Math.max(remainingSpace, 400);
  const FOOTER_MIN = 800;
  const rawTop = Math.floor(safeRemaining * 0.45);
  const rawBottom = Math.floor(safeRemaining * 0.45);
  const bottomSpacing = Math.max(rawBottom, FOOTER_MIN);
  const topSpacing = Math.max(rawTop - Math.max(0, FOOTER_MIN - rawBottom), 400);
  const midSpacing = Math.max(safeRemaining - topSpacing - bottomSpacing, 0);
  return { topSpacing, midSpacing, bottomSpacing };
}

// ── Recette R1 : Pure Paragraph Cover (left-aligned) ─────────────────────
function buildCoverR1(config) {
  const C = config.palette;
  const padL = 1200, padR = 800;
  const availableWidth = 11906 - padL - padR - 300;
  const { titlePt, titleLines } = calcTitleLayout(config.title, availableWidth, 40, 24);
  const titleSize = titlePt * 2;
  const spacing = calcCoverSpacing({
    titleLineCount: titleLines.length, titlePt,
    hasSubtitle: !!config.subtitle, hasEnglishLabel: !!config.englishLabel,
    metaLineCount: (config.metaLines || []).length,
    fixedHeight: 400,
  });
  const accentLeft = { style: BorderStyle.SINGLE, size: 8, color: C.accent, space: 12 };
  const children = [];

  children.push(new Paragraph({ spacing: { before: spacing.topSpacing } }));

  if (config.englishLabel) {
    children.push(new Paragraph({
      indent: { left: padL, right: padR }, spacing: { after: 500 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: C.accent, space: 8 } },
      children: [new TextRun({
        text: config.englishLabel.split("").join("  "),
        size: 18, color: C.accent,
        font: { ascii: "Arial", eastAsia: "SimHei" }, characterSpacing: 40,
      })],
    }));
  }

  for (let i = 0; i < titleLines.length; i++) {
    children.push(new Paragraph({
      indent: { left: padL },
      spacing: {
        after: i < titleLines.length - 1 ? 100 : 300,
        line: Math.ceil(titlePt * 23), lineRule: "atLeast",
      },
      children: [new TextRun({
        text: titleLines[i], size: titleSize, bold: true,
        color: C.cover.titleColor,
        font: { eastAsia: "SimHei", ascii: "Arial" },
      })],
    }));
  }

  if (config.subtitle) {
    children.push(new Paragraph({
      indent: { left: padL }, spacing: { after: 800 },
      children: [new TextRun({
        text: config.subtitle, size: 24, color: C.cover.subtitleColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" },
      })],
    }));
  }

  for (const line of (config.metaLines || [])) {
    children.push(new Paragraph({
      indent: { left: padL + 200 }, spacing: { after: 80 },
      border: { left: accentLeft },
      children: [new TextRun({
        text: line, size: 24, color: C.cover.metaColor,
        font: { eastAsia: "Microsoft YaHei", ascii: "Arial" },
      })],
    }));
  }

  children.push(new Paragraph({ spacing: { before: spacing.bottomSpacing } }));

  children.push(new Paragraph({
    indent: { left: padL, right: padR },
    border: { top: { style: BorderStyle.SINGLE, size: 2, color: C.accent, space: 8 } },
    spacing: { before: 200 },
    children: [
      new TextRun({ text: config.footerLeft || "", size: 16, color: C.cover.footerColor, font: { ascii: "Arial" } }),
      new TextRun({ text: "                                        " }),
      new TextRun({ text: config.footerRight || "", size: 16, color: C.cover.footerColor, font: { ascii: "Arial" } }),
    ],
  }));

  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    layout: TableLayoutType.FIXED,
    borders: allNoBorders,
    rows: [new TableRow({
      height: { value: 16838, rule: "exact" },
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: C.bg },
        borders: noBorders,
        verticalAlign: "top",
        children,
      })],
    })],
  })];
}

// ── Constructeurs du corps ───────────────────────────────────────────────
const FONT_CORPS = { ascii: "Calibri", eastAsia: "Microsoft YaHei" };
const FONT_TITRES = { ascii: "Calibri", eastAsia: "SimHei" };

function h1(text, sautPage) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    pageBreakBefore: !!sautPage,
    spacing: { before: 360, after: 200, line: 312 },
    children: [new TextRun({ text, bold: true, size: 32, color: P.headingsBody, font: FONT_TITRES })],
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 140, line: 312 },
    children: [new TextRun({ text, bold: true, size: 26, color: P.headingsBody, font: FONT_TITRES })],
  });
}

function para(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { line: 312, after: 160 },
    children: [new TextRun({ text, size: 24, color: P.body, font: FONT_CORPS })],
  });
}

function question(texte) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    keepNext: true,
    spacing: { before: 220, after: 100, line: 312 },
    children: [new TextRun({ text: texte, bold: true, size: 24, color: P.headingsBody, font: FONT_TITRES })],
  });
}

function puce(texte) {
  return new Paragraph({
    bullet: { level: 0 },
    alignment: AlignmentType.LEFT,
    spacing: { line: 312, after: 80 },
    children: [new TextRun({ text: texte, size: 24, color: P.body, font: FONT_CORPS })],
  });
}

function elementNum(texte, reference) {
  return new Paragraph({
    numbering: { reference, level: 0 },
    alignment: AlignmentType.LEFT,
    spacing: { line: 312, after: 80 },
    children: [new TextRun({ text: texte, size: 24, color: P.body, font: FONT_CORPS })],
  });
}

function titreTableau(texte) {
  return new Paragraph({
    keepNext: true,
    spacing: { before: 200, after: 100, line: 312 },
    children: [new TextRun({ text: texte, bold: true, size: 21, color: P.table.accentLine, font: FONT_CORPS })],
  });
}

function tableau(entetes, lignes, largeurs) {
  const cellule = (texte, entete, pourcentage) => new TableCell({
    width: { size: pourcentage, type: WidthType.PERCENTAGE },
    margins: { top: 60, bottom: 60, left: 120, right: 120 },
    shading: entete ? { type: ShadingType.CLEAR, fill: P.table.headerBg } : undefined,
    children: [new Paragraph({
      alignment: AlignmentType.LEFT,
      spacing: { line: 276 },
      children: [new TextRun({
        text: texte, size: 21, bold: !!entete,
        color: entete ? P.table.headerText : P.body, font: FONT_CORPS,
      })],
    })],
  });
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 2, color: P.table.accentLine },
      bottom: { style: BorderStyle.SINGLE, size: 2, color: P.table.accentLine },
      left: NB, right: NB,
      insideHorizontal: { style: BorderStyle.SINGLE, size: 1, color: P.table.innerLine },
      insideVertical: NB,
    },
    rows: [
      new TableRow({
        tableHeader: true, cantSplit: true,
        children: entetes.map((e, i) => cellule(e, true, largeurs[i])),
      }),
      ...lignes.map((ligne) => new TableRow({
        cantSplit: true,
        children: ligne.map((v, i) => cellule(v, false, largeurs[i])),
      })),
    ],
  });
}

// ── Assemblage du corps ──────────────────────────────────────────────────
const referencesNum = [];
const corps = [];
chapitres.forEach((chapitre, index) => {
  corps.push(h1(chapitre.titre, index > 0));
  for (const bloc of chapitre.blocs) {
    if (bloc.t === "p") corps.push(para(bloc.x));
    else if (bloc.t === "h2") corps.push(h2(bloc.x));
    else if (bloc.t === "q") corps.push(question(bloc.x));
    else if (bloc.t === "liste") bloc.items.forEach((i) => corps.push(puce(i)));
    else if (bloc.t === "num") {
      if (!referencesNum.includes(bloc.ref)) referencesNum.push(bloc.ref);
      bloc.items.forEach((i) => corps.push(elementNum(i, bloc.ref)));
    } else if (bloc.t === "table") {
      corps.push(titreTableau(bloc.titre));
      corps.push(tableau(bloc.entetes, bloc.lignes, bloc.largeurs));
      corps.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    }
  }
});

const numerotation = {
  config: referencesNum.map((reference) => ({
    reference,
    levels: [{
      level: 0, format: LevelFormat.DECIMAL, text: "%1.",
      alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 720, hanging: 360 } } },
    }],
  })),
};

// ── En-têtes et pieds de page ────────────────────────────────────────────
const piedRomain = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "888888", font: FONT_CORPS })],
  })],
});
const piedArabe = new Footer({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "666666", font: FONT_CORPS })],
  })],
});
const enteteCorps = new Header({
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: P.table.innerLine, space: 4 } },
    children: [new TextRun({
      text: "Kit de Développement Triade — Manuel du développeur",
      size: 18, color: P.secondary, font: FONT_CORPS,
    })],
  })],
});

// ── Section sommaire ─────────────────────────────────────────────────────
const sommaire = [
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 480, after: 360 },
    children: [new TextRun({
      text: "Sommaire", bold: true, size: 32,
      color: P.headingsBody, font: FONT_TITRES,
    })],
  }),
  new TableOfContents("Sommaire", { hyperlink: true, headingStyleRange: "1-2" }),
  new Paragraph({
    spacing: { before: 200 },
    children: [new TextRun({
      text: "Remarque : ce sommaire est généré par champs. Après modification du document, faites un clic droit sur le sommaire puis « Mettre à jour les champs » pour actualiser les numéros de page.",
      italics: true, size: 18, color: "888888", font: FONT_CORPS,
    })],
  }),
];

// ── Document ─────────────────────────────────────────────────────────────
const taillePage = { width: 11906, height: 16838 };
const marges = { top: 1440, bottom: 1440, left: 1701, right: 1417 };

const doc = new Document({
  styles: {
    default: {
      document: {
        run: { font: FONT_CORPS, size: 24, color: P.body },
        paragraph: { spacing: { line: 312 } },
      },
      heading1: {
        run: { font: FONT_TITRES, size: 32, bold: true, color: P.headingsBody },
        paragraph: { spacing: { before: 360, after: 200, line: 312 } },
      },
      heading2: {
        run: { font: FONT_TITRES, size: 26, bold: true, color: P.headingsBody },
        paragraph: { spacing: { before: 280, after: 140, line: 312 } },
      },
    },
  },
  numbering: numerotation,
  sections: [
    {
      properties: {
        page: { size: taillePage, margin: { top: 0, bottom: 0, left: 0, right: 0 } },
      },
      children: buildCoverR1({
        title: "Kit de Développement Triade",
        subtitle: "Manuel du développeur — conduite de projet avec agent IA",
        englishLabel: "PROTOCOLE TRIADE",
        metaLines: [
          "Version 1.0.0 du kit",
          "Diffusion publique — aucun jeton embarqué",
          "Git · Google Drive · Zenodo",
        ],
        footerLeft: "Protocole Triade v1.0",
        footerRight: "Novembre 2026",
        palette: P,
      }),
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: taillePage, margin: marges,
          pageNumbers: { start: 1, formatType: NumberFormat.UPPER_ROMAN },
        },
      },
      footers: { default: piedRomain },
      children: sommaire,
    },
    {
      properties: {
        type: SectionType.NEXT_PAGE,
        page: {
          size: taillePage, margin: marges,
          pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
        },
      },
      headers: { default: enteteCorps },
      footers: { default: piedArabe },
      children: corps,
    },
  ],
});

const sortie = path.join(
  "/home/z/my-project/download/kit-dev-triade/docs",
  "MANUEL_DEVELOPPEUR.docx"
);
Packer.toBuffer(doc).then((tampon) => {
  fs.writeFileSync(sortie, tampon);
  console.log("Écrit :", sortie, "—", tampon.length, "octets");
});
