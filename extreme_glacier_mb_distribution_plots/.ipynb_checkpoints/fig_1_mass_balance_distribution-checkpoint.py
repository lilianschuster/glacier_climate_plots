#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to reproduce the glacier mass-balance distribution plot (Fig. 1 of Voordendag, Prinz, Schuster, Kaser, 2023, https://tc.copernicus.org/preprints/tc-2023-49/)
@author: Lilian Schuster
"""

# Glacier MB distribution plot inspired by Matthias Huss 
# overall idea: plot specific MB distributions and show that this year (2022) is an extreme melt year. Every vertical line represents the observation of one year
# the original idea is from Matthias Huss, we just replotted it for other glaciers and added some new ideas inside
# original post from Matthias Huss: https://twitter.com/matthias_huss/status/1575539821493293058
# other variants of this Fig. can be found here: https://github.com/lilianschuster/glacier_climate_plots/tree/main/extreme_glacier_mb_distribution_plots

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib import cm
import scipy
from scipy.stats import norm
import seaborn as sns

plt.rcParams['savefig.dpi'] = 300
%matplotlib inline

# load the data
### here we have the data for Hintereisferner and Kesselwandferner, 
### but the code should similarly work for other glaciers (with some tiny manual adjustments)
spec_mb = pd.read_csv('spec_mb_hef_kwf_oct2022.csv', sep=';')
spec_mb.index = spec_mb['calender year']
# check if there are any missing columns and if yes drop them
spec_mb = spec_mb.dropna()

base_col = sns.color_palette([sns.color_palette('colorblind')[0], sns.color_palette('colorblind')[2], sns.color_palette('colorblind')[3]])

col_sp_yr = {2020: base_col[0],
            2021: base_col[1],
            2022: base_col[2]}

version = 'tc'
glacier = 'Hintereisferner'
for save in ['save_pdf_svg']: # 'save_png',
    # the arrow - line connections to display the ranges somehow work differently if saved as png or as pdf svg, therefore I need different numbers to get "similar" outcomes
    if save == 'save_png':
        armB = 150
    elif save == 'save_pdf_svg':
        armB = 45
    arrowprops = {"arrowstyle":"-", "color":"gray", "connectionstyle":f"arc,angleA=0,angleB=90,armA=0,armB={armB},rad=30", "lw":2}

    y_span_text_m = 0.18
    spec_mb_values = spec_mb['HEF mass balance (kg/m�)']/1000 # use 10**3 kg m-2 

    # get maximum specific mb and use them as limits for the plots and for the colormap scales 
    # we center the mass balance at 0, hence we just get the maximum absolute value 
    xlims_abs = np.max([np.absolute(spec_mb_values.max()),
            np.absolute(spec_mb_values.min())])*1.1

    fig,_ = plt.subplots(1,1,figsize=(10,6))
    fig.set_dpi(300)

    # plot each year as vertical line 
    for j, yr in enumerate(spec_mb.index):
        if yr in [2020,2021,2022]:
            color = col_sp_yr[yr]
            lw=5
            plt.axvline(spec_mb_values.loc[yr], color = color, lw=lw, label =f'{yr-1}/{str(yr)[2:]}')

        else:
            color = 'black'
            lw = 0.5
            plt.axvline(spec_mb_values.loc[yr], color = color, lw=lw)
    plt.legend(fontsize=20)

    plt.xlim([-xlims_abs, xlims_abs])

    # fit and plot the generalized extreme value distribution (fitted from the observations)
    params = scipy.stats.genextreme.fit(spec_mb_values)
    xmin, xmax = -xlims_abs,xlims_abs
    x = np.linspace(xmin, xmax, 100)
    y = scipy.stats.genextreme.pdf(x, *params)
    # get mean and std of the observed specific mb values by using the generalized extreme value distribution ... 
    # median = scipy.stats.genextreme.median(*params)
    # std = scipy.stats.genextreme.std(*params)
    # No, actually, showing the percentiles is much better! 
    
    # Create the GEV distribution object
    gev_dist = scipy.stats.genextreme(*params)

    # Define the probability levels for which you want to find the quantiles
    # For example, to find the 10th, 50th, and 90th percentiles (quantiles), you can use:
    prob_levels = [0.001, 0.01,0.1, 0.5, 0.9, 0.99,0.999]

    # Calculate the quantiles
    quantiles = gev_dist.ppf(prob_levels)
    
         

    plt.xlabel(r'mass balance (10$^{3}$ kg m$^{-2}$)', fontsize=24)
    ax = plt.gca()
    ax.plot(x, y, lw=4, color='black')

    ax.set_xticks(np.arange(-int(xlims_abs)-1, int(xlims_abs)+1.01,0.1), minor=True)
    plt.xticks(ticks=np.arange(-int(xlims_abs), int(xlims_abs)+0.01,1), fontsize=22) 
    ax.tick_params(axis='x', which='major', labelsize=22, width=2) 

    plt.xlim([-xlims_abs, xlims_abs])

    plt.text(0.77, 0.5,
             f'n={len(spec_mb_values)} years:\n1952-2022', 
             transform=plt.gca().transAxes, fontsize=20)

    # create secondary axis and plot the quantiles 
    ax2 = ax.secondary_xaxis(location='top')
    #ax2.plot(x, y, lw=4, color='black')

    ax2.set_xticks(quantiles)
    ax2.set_xticklabels(labels= ['0.1%','1%','10%','median','90%','99%','99.9%']) 
    
    #ax2.set_xticks([mean-3*std,mean-2*std,median-1*std,mean,mean+1*std,mean+2*std,mean+3*std])
    #ax2.set_xticklabels(labels= [r'-3$\sigma$',r'-2$\sigma$',r'-1$\sigma$',
    #                             r'mean',r'+1$\sigma$', r'+2$\sigma$', r'+3$\sigma$']) 
    ax2.set_zorder(2)

    # remove yticks
    plt.yticks(ticks=[])
    #remove yline axis
    ax.spines['left'].set_linewidth(0)
    ax.spines['right'].set_linewidth(0)
    # make sure that 0 "probability" is directly on the x-axis
    plt.ylim([0,y.max()*1.01])


    #if save=='save_png':
    plt.tight_layout()
    # set the parameters for both axis: label size in font points, the line tick line width and length in pixels
    ax2.tick_params(axis='x', which='major', labelsize=14, width=2, length=7)

    plt.savefig(f'fig_1_hef_mb_distributions_tc_gev.svg', bbox_inches='tight')
    plt.savefig(f'fig_1_hef_mb_distributions_tc_gev.pdf', bbox_inches='tight')
    # we manually changed the labels, to not overlap anymore by using inkscape