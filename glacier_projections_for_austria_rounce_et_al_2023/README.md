# Future evolution of glaciers in Austria as projected by Rounce et al., 2023

illustrates the evolution of the volume of the Austrian glaciers by using the data of [Rounce, D.R., R. Hock, and F. Maussion. 2022. Global PyGEM-OGGM Glacier Projections with RCP and SSP Scenarios, Version 1](https://doi.org/10.5067/P8BN9VO9N5C7), which results were published in [Rounce et al. 2023](https://www.science.org/doi/10.1126/science.abo1324)


if you want to use or adapt the figure, you need to cite the dataset and the paper of Rounce et al. 2023. 

Within the folder data/ you can find 
- a list of RGI ids with corresponding countries for the Alps (file created by Fabien Maussion): `data/rgi62_era5_itmix_country_df.h5`
- the glacier mass projections of Rounce_et_al_2023 as downloaded from [Rounce, D.R., R. Hock, and F. Maussion. 2022. Global PyGEM-OGGM Glacier Projections with RCP and SSP Scenarios, Version 1](https://doi.org/10.5067/P8BN9VO9N5C7)
    - e.g. `data/Rounce_et_al_2023/R11_glac_mass_annual_50sets_2000_2100-ssp119.nc`
- the global mean temp. deviations from 2081 to 2100 relative to 1850 to 1900 (computed by David Rounce): `data/Rounce_et_al_2023/Global_mean_temp_deviation_2081_2100_rel_1850_1900.csv`


I used the exact same definition as in Rounce et al. 2023 (e.g. for the temp. scenario classification). The lines correspond to the median estimates, the range for when 50% is lost shows the IPCC defined likely range (17, 83 percentile). Here numbers are
relative to 2024, but you can adapt that quickly.

Lilian

Creator of the figure:
- [Lilian Schuster](https://github.com/lilianschuster) (Department of Atmospheric and Cryospheric Sciences (ACINN), Universität Innsbruck)



License: BSD3

