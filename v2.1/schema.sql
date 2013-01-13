CREATE TABLE IF NOT EXISTS application (
  "permitApplicationNumber" TEXT NOT NULL,
  "pdfParsed" INTEGER,
  UNIQUE("permitApplicationNumber")
);
