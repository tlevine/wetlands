CREATE TABLE application (
  "permitApplicationNumber" TEXT NOT NULL,
  "pdfParsed" INTEGER NOT NULL,
  UNIQUE("permitApplicationNumber")
);
