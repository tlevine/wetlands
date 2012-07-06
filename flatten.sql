-- Generate flat CSV files
.mode csv
.header on

SELECT
  -- I changed the order slightly. This order is better.

  -- Identifiers
  [Public Notice Download].[PermitApplication No.],
  [Public Notice].scraper_run,

  -- Meat
  ListingData.[Project Description],
  Applicant,
  [Location],

  [Public Notice Date],
  [Expiration Date],

  [Project Manager Name],
  [Project Manager Email],
  [Project Manager Phone],

  -- References
  "http://www.mvn.usace.army.mil/ops/regulatory/" || [Public Notice] AS "Public Notice URL",
  "http://www.mvn.usace.army.mil/ops/regulatory/" || [Drawings] AS "Drawings URL",

  -- Further extracts
  [Public Notice Download].text AS pdf_text

FROM
  [Public Notice]
  -- Add rows
  JOIN Listing ON
    [Public Notice].scraper_run =Listing.scraper_run AND
    [Public Notice].motherkwargs = Listing.kwargs

  -- Add columns
  JOIN [Public Notice Download] ON
   [Public Notice].scraper_run = [Public Notice Download].scraper_run AND
   [Public Notice].kwargs=[Public Notice Download].kwargs
  JOIN ListingData ON
    [Public Notice Download].scraper_run = ListingData.scraper_run AND
    [Public Notice Download].[PermitApplication No.]=ListingData.[PermitApplication No.]
ORDER BY
  [Public Notice Download].[PermitApplication No.],
  [Public Notice].scraper_run
;
