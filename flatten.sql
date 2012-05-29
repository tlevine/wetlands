-- Generate flat CSV files
-- select count(*), Listing.scraper_run, ListingData.[PermitApplication No.] from Listing JOIN ListingData ON Listing.scraper_run = ListingData.scraper_run AND Listing.kwargs=ListingData.kwargs join [Public Notice] ON Listing.scraper_run = [Public Notice].scraper_run AND Listing.kwargs = [Public Notice].motherkwargs JOIN [Public Notice Download] on [Public Notice].kwargs = [Public Notice Download].kwargs AND [Public Notice].kwargs=[Public Notice Download].kwargs order by ListingData.[PermitApplication No.] limit 30;

select count(*) from [Public Notice];

select count(*)
from
  [Public Notice]
  -- Add rows
  JOIN Listing on Listing.scraper_run = [Public Notice].scraper_run AND Listing.kwargs=[Public Notice].motherkwargs

  -- Add columns
  JOIN [Public Notice Download] ON
   [Public Notice].scraper_run = [Public Notice Download].scraper_run AND
   [Public Notice].kwargs=[Public Notice Download].kwargs
--  JOIN ListingData ON
  --  Listing.scraper_run = ListingData.scraper_run AND
    --Listing.kwargs=ListingData.kwargs
--Listing.scraper_run = ListingData.scraper_run AND Listing.kwargs=ListingData.kwargs
;
