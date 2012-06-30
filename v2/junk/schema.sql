CREATE TABLE IF NOT EXISTS scraper_runs (
  date DATE NOT NULL,
  time TIME NOT NULL,
  UNIQUE(date)
);

CREATE TABLE IF NOT EXISTS permits (
  projectDescription TEXT NOT NULL,
  applicant TEXT NOT NULL,
  publicNoticeDate DATE NOT NULL,
  expirationDate DATE NOT NULL,
  permitId TEXT NOT NULL,
  firstPublicNoticeUrl TEXT NOT NULL,
  firstPublicNoticeMd5 TEXT NOT NULL,
  hasPublicNoticeChanged INTEGER NOT NULL,
  firstDrawingUrl TEXT NOT NULL,
  firstDrawingMd5 TEXT NOT NULL,
  hasDrawingChanged INTEGER NOT NULL,
  projectManagerPhone TEXT NOT NULL,
  projectManagerEmail TEXT NOT NULL,
  WQC TEXT NOT NULL,
  CUP TEXT NOT NULL,
  mitigationBank TEXT NOT NULL,
  firstSeen DATE NOT NULL,
  -- ...,
  UNIQUE(permitId),
  FOREIGN KEY (firstSeen) REFERENCES scraper_runs(date),
  FOREIGN KEY (lastSeen) REFERENCES scraper_runs(date),




);

Acres1
Acres2
Acres3
Acres4
Acres5
Acres6
Acres7
Acres8
Parish
Coord1
Coord2
Coord3
Basin
HUC
10 acre
Section 10
Section 404

