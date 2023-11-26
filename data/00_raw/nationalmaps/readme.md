.shp file `metadata/SA2_2021_AUST_GDA2020.shp` has column `	SA2_CODE21` which maps to `Census_2021_G17_Total_personal_income_weekly_by_age_by_sex_Main_Statistical_Areas_Level_2_and_up_SA2_.txt` column REGION.
- Note the "SA2" in the .txt file name corresponds to the SA2 in the .shp file name.

## Preporcessing Steps

[Digital BoundaRY FILES](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files)

[Dictionary of ABS variable codes to names](https://www.abs.gov.au/census/guide-census-data/census-dictionary/2021/variables-index)
- name as: `data/00_raw/nationalmaps/metadata/variable_indices_mapping.json`
- for each variable mapping, add to json: `data/00_raw/nationalmaps/metadata/variable_indices_mapping.json`

### ABS census data
1. download file from ABS / national maps
2. move to raw data dir.
3. rename the file to take out the weird characters
4. download metadata "Digital boundary files"
5. Use geopandas to convert the ABS data's location identifier, to the corresponding gps location in the metadata.
6. Convert the column variable codes, to names using the ABS variable dictionary.


| file | desctiption |
| --- | --- |
| https://researchdata.edu.au/national-exposure-information-density-exposure/1668471?source=suggested_datasets | poulation desnity as gpd file |
| https://www.abs.gov.au/statistics/people/population/regional-population-age-and-sex/2022 | list of population density files |
| https://www.abs.gov.au/statistics/people/population/regional-population-age-and-sex/2022/32350_ERP_Age_Sex_SA2_2022_gpkg.zip | pop esitimates by age sex, by statistical area: SA2, 2022 |
| https://api.data.abs.gov.au/data/ERP_COMP_SA_ASGS2021/1.SA2..A | population density by statistical area SA2 |
