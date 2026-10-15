import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const sourcePath = "C:/Users/DELL/Desktop/msfabric-minor/French/Module 9 Utiliser Copilot dans MS Fabric/sample.csv";
const outputPath = "C:/Users/DELL/Desktop/msfabric-minor/French/Module 9 Utiliser Copilot dans MS Fabric/sample.xlsx";
const previewPath = "C:/Users/DELL/Desktop/msfabric-minor/.codex_work/sample_xlsx/sample_preview.png";

function parseFrenchDate(value) {
  const iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (iso) return new Date(Date.UTC(Number(iso[1]), Number(iso[2]) - 1, Number(iso[3])));
  const fr = /^(\d{2})\/(\d{2})\/(\d{4})$/.exec(value);
  if (fr) return new Date(Date.UTC(Number(fr[3]), Number(fr[2]) - 1, Number(fr[1])));
  throw new Error(`Date non reconnue: ${value}`);
}

function parseFrenchNumber(value) {
  const normalized = String(value).replace(/\s/g, "").replace(",", ".");
  const parsed = Number(normalized);
  if (!Number.isFinite(parsed)) throw new Error(`Nombre non reconnu: ${value}`);
  return parsed;
}

const csvText = await fs.readFile(sourcePath, "utf8");
const workbook = await Workbook.fromCSV(csvText, { sheetName: "Données" });
const sheet = workbook.worksheets.getItemAt(0);
const used = sheet.getUsedRange();
const values = used.values;

for (let row = 1; row < values.length; row += 1) {
  values[row][0] = Number(values[row][0]);
  values[row][2] = parseFrenchDate(values[row][2]);
  values[row][5] = Number(values[row][5]);
  values[row][6] = parseFrenchNumber(values[row][6]);
}
used.values = values;

sheet.showGridLines = false;
sheet.freezePanes.freezeRows(1);
used.format.font = { name: "Arial", size: 10, color: "#1F2937" };
used.format.verticalAlignment = "center";
sheet.getRange("A1:H1").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  borders: { preset: "outside", style: "thin", color: "#17365D" },
};
sheet.getRange("A2:A10").format.numberFormat = "0";
sheet.getRange("C2:C10").format.numberFormat = "dd/mm/yyyy";
sheet.getRange("F2:F10").format.numberFormat = "0";
sheet.getRange("G2:G10").format.numberFormat = "#,##0.00";
sheet.getRange("B2:B10").format.numberFormat = "@";
sheet.getRange("D2:E10").format.numberFormat = "@";
used.format.autofitColumns();
used.format.autofitRows();
sheet.getRange("A:A").format.columnWidth = 11;
sheet.getRange("B:B").format.columnWidth = 12;
sheet.getRange("C:C").format.columnWidth = 14;
sheet.getRange("D:E").format.columnWidth = 14;
sheet.getRange("F:F").format.columnWidth = 11;
sheet.getRange("G:G").format.columnWidth = 14;
sheet.getRange("H:H").format.columnWidth = 12;
sheet.getRange("1:1").format.rowHeight = 22;

workbook.recalculate();

const inspection = await workbook.inspect({
  kind: "table",
  range: "Données!A1:H10",
  include: "values,formulas",
  tableMaxRows: 12,
  tableMaxCols: 10,
});
console.log("INSPECTION");
console.log(inspection.ndjson);

const errors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!",
  options: { useRegex: true, maxResults: 100 },
  summary: "final formula error scan",
});
console.log("ERROR_SCAN");
console.log(errors.ndjson);

const preview = await workbook.render({
  sheetName: "Données",
  range: "A1:H10",
  scale: 2,
  format: "png",
});
await fs.mkdir(path.dirname(previewPath), { recursive: true });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(`OUTPUT=${outputPath}`);
console.log(`PREVIEW=${previewPath}`);
