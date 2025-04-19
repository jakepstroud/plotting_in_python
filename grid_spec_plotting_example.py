# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:13:38 2020

@author: Jake
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.style.use(['ggplot','paper_plots'])

def colorbar(mappable,label):
    """
    Add a colorbar to the current axes.

    Parameters
    ----------
    mappable : matplotlib.cm.ScalarMappable
        The image, contour set, etc. to which the colorbar applies.
    label : str
        The label for the colorbar.

    Returns
    -------
    matplotlib.colorbar.Colorbar
        The colorbar object.
    """
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    fig = plt.gcf()
    last_axes = plt.gca()
    ax = mappable.axes
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=0.07, pad=0.05)
    cbar = fig.colorbar(mappable, cax=cax)
    cbar.set_label(label, rotation=270, labelpad=10)
    cbar.outline.set_visible(False)
    plt.sca(last_axes)
    return cbar

#%% Plotting functions
def gen_heatmap(ax0):
    """
    Generate and display a 2D heatmap on the given axes.

    Parameters
    ----------
    ax0 : matplotlib.axes.Axes
        The axes on which to draw the heatmap.
    """
    #Create data
    x = y = np.arange(-3.0, 3.01, 0.1)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X**2 + Y**2)/3)
    
    #Plot heatmap
    im = ax0.imshow(Z1,extent=[-3,3,-3,3],vmin=0,vmax=1)
    plt.xlabel('x label'); plt.ylabel('y label')
    plt.xticks(x[::10]);plt.yticks(x[::10])
    
    #Add colorbar
    colorbar(im,'color label')

def gen_scatter(ax0):
    """
    Generate and display a 2-group scatter plot with color mapping on the given axes.

    Parameters
    ----------
    ax0 : matplotlib.axes.Axes
        The axes on which to draw the scatter plot.
    """
    #Create data
    x = np.arange(0,100)
    y = np.zeros((2,100))
    c = np.zeros((2,100))
    y[0,:] = x + np.random.normal(0,10,100)
    y[1,:] = 2*x + np.random.normal(0,20,100) - 20
    c[0,:] = -x + np.random.normal(0,10,100) + 80
    c[1,:] = x + np.random.normal(0,10,100) + 80
    
    #Add legend
    ax0.scatter(-10,0,c='k',label='group 1',linewidths=0.75)
    sc = ax0.scatter(-10,0,edgecolors='k',label='group 2',linewidths=0.75)
    sc.set_facecolor('none')
    plt.legend()
    
    #Plot scatter plot
    ax0.scatter(x,y[0,:],c=c[0,:],linewidths=0.75,
                vmin=np.min(c),vmax=np.max(c))
    sc = ax0.scatter(x,y[1,:],c=c[1,:],linewidths=0.75,
                vmin=np.min(c),vmax=np.max(c))
    sc.set_facecolor('none')
    plt.xlabel('x label'); plt.ylabel('y label')    
    plt.xlim([-5,105])
    
    #Add colorbar
    colorbar(sc,'color label')

def gen_trig_funs(fun_flag,ax0):
    """
    Plot three phase-shifted trigonometric functions on the given axes.

    Parameters
    ----------
    fun_flag : str
        Type of trigonometric function to plot. One of: 'sin', 'cos', or 'tan'.
    ax0 : matplotlib.axes.Axes
        The axes on which to draw the trigonometric plots.
    """
    #Create data
    x = np.linspace(0,4*np.pi,100)
    y = np.zeros((100,3))
    phases = np.array([0,np.pi/3,2*np.pi/3])
    
    if fun_flag=='sin':
        for c,phase in enumerate(phases):
            y[:,c] = np.sin(x-phase)
    elif fun_flag=='cos':
        for c,phase in enumerate(phases):
            y[:,c] = np.cos(x-phase)
    elif fun_flag=='tan':
        for c,phase in enumerate(phases):
            y[:,c] = np.tan(x-phase)
            
    #Plot 3 phases
    [ax0.plot(x,y[:,i],'C'+str(i)) for i in range(3)]
    
    plt.ylim([-1.05,1.05])
    plt.xticks(np.linspace(0,4*np.pi,5),['$0$','$\pi$','$2 \pi$','$3 \pi$','$4 \pi$'])
    plt.ylabel(fun_flag);plt.xlabel('angle (rads.)')
    
    #Add legend
    if fun_flag == 'cos':
        plt.legend(['$0$','$\pi/3$','$2 \pi/3$'],title='phase shift',
                   loc=(-0.28,1.1),ncol=3)
    
#%% Plotting script
fig = plt.figure(figsize = (5.3,4))

#Split top and bottom rows:
two_main_rows = gridspec.GridSpec(2,1, figure=fig, height_ratios = [1,0.8], hspace=0.55)


#Create two panels in top row:
top_2_panels = two_main_rows[0].subgridspec(1,2, width_ratios = [1,1.2], wspace=0.6)

#Heatmap
ax0 = fig.add_subplot(top_2_panels[0])
gen_heatmap(ax0)

#Scatter plot
ax0 = fig.add_subplot(top_2_panels[1])
gen_scatter(ax0)


#Create 3 panels in bottom row:
bottom_3_panels = two_main_rows[1].subgridspec(1,3, width_ratios = [1,1,1], wspace=0.65)

ax0 = fig.add_subplot(bottom_3_panels[0])
gen_trig_funs('sin',ax0)

ax0 = fig.add_subplot(bottom_3_panels[1])
gen_trig_funs('cos',ax0)

ax0 = fig.add_subplot(bottom_3_panels[2])
gen_trig_funs('tan',ax0)

# plt.savefig('example.pdf',format='pdf')
