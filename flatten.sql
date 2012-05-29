-- Generate flat CSV files
.mode csv
.header on

select * from
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
--Listing.scraper_run = ListingData.scraper_run AND Listing.kwargs=ListingData.kwargs
limit 1;
