
# coding: utf-8

# In[4]:
from __future__ import print_function
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage.filters import gaussian_filter

import os


# In[5]:

lampList = {
    "lamp1" : {
        "file" : "lamp1.dat",
        "name" : "He"
    },
    "lamp2" : {
        "file" : "lamp2.dat",
        "name" : "Ar"
    }
}

directory = "arcplots"

sides = ["red","blue"]

gratings = {
    "150/7500": {
        "dispersion": 3,
        "range":12288
    },
    "300/500": {
        "dispersion": 1.59,
        "range":6525
    },
    "400/8500": {
        "dispersion": 1.16,
        "range": 4762
    },
    "600/7500": {
        "dispersion": 0.80,
        "range": 3275
    },
    "600/5000": {
        "dispersion": 0.80,
        "range": 3275
    },
    "600/1000": {
        "dispersion": 0.80,
        "range":3275
    },
    "831/8200": {
        "dispersion": 0.58,
        "range": 2375
    }
}


for key in lampList.keys():
    file = os.path.join(directory,lampList[key]["file"])
    df = pd.read_csv(file,delim_whitespace=True)
    df.columns=['lambda','intensity']
    lampList[key]["lines"] = df

    


# In[17]:

from bokeh.plotting import figure, output_file, show, curdoc
from bokeh.models import Range1d, HoverTool

from bokeh.layouts import widgetbox, layout
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider




# In[6]:

output_file("line.html")
hover = HoverTool(tooltips=[
    ("lambda", "$x{00000.0}"),
])

p = figure(plot_width=600, plot_height=400)
p.add_tools(hover)


# In[7]:

x1=lampList['lamp1']['lines']['lambda']
y1=gaussian_filter(lampList['lamp1']['lines']['intensity'],sigma=4)
x2=lampList['lamp2']['lines']['lambda']
y2=gaussian_filter(lampList['lamp2']['lines']['intensity'],sigma=4)


# In[8]:

p.line(x1,y1, color='firebrick', legend=lampList['lamp1']['name'])
p.line(x2,y2,color='navy', legend=lampList['lamp2']['name'])
central_wavelength=7500
range = gratings["600/1000"]["range"]
xlim_low = central_wavelength-range/2
xlim_high = central_wavelength+range/2
p.x_range=Range1d(xlim_low, xlim_high)


# In[9]:

p.title.text = "LRIS Arcplot"
p.title.align = "right"
p.title.text_color = "orange"
p.title.text_font_size = "25px"


# In[10]:

p.background_fill_color = "beige"
p.background_fill_alpha = 0.5


# In[11]:

p.xaxis.axis_label = "Wavelength"
p.yaxis.axis_label = "Intensity"


# In[12]:

p.legend.click_policy="hide"


# In[15]:

#slider = Slider(start=0, end=10, value=1, step=.1, title="Slider")
#button_group = RadioButtonGroup(labels=["Option 1", "Option 2", "Option 3"], active=0)
#select = Select(title="Option:", value="foo", options=["foo", "bar", "baz", "quux"])
#button_1 = Button(label="Button 1")
#button_2 = Button(label="Button 2")

show(p)


# In[18]:

#l = layout([
#  [button_group],
#  [select],
#  [p],
#], sizing_mode='stretch_both')


# In[20]:

curdoc().add_root(p)


# In[ ]:

#show(widgetbox(p,button_1, slider, button_group, select, button_2, width=300))


# In[19]:




