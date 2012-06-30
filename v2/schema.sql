CREATE TABLE IF NOT EXISTS scraper_runs (
  date DATE NOT NULL,
  time TIME NOT NULL,
  UNIQUE(date)
);

CREATE TABLE IF NOT EXISTS permits (
  permitId TEXT NOT NULL,
  firstSeen DATE NOT NULL,
  -- ...,
  firstPublicNoticeUrl TEXT NOT NULL,
  firstPublicNoticeMd5 TEXT NOT NULL,
  firstDrawingUrl TEXT NOT NULL,
  firstDrawingMd5 TEXT NOT NULL,
  hasPublicNoticeChanged INTEGER NOT NULL,
  hasDrawingChanged INTEGER NOT NULL,
  UNIQUE(permitId),
  FOREIGN KEY (firstSeen) REFERENCES scraper_runs(date),
  FOREIGN KEY (lastSeen) REFERENCES scraper_runs(date),
);
