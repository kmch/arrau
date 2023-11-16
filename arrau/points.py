
class Points:
  def __init__(self, points):
    self.all = points
class Points3d(Points):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for pt in self.all: # checking if it's really (x,y,z)
        assert np.array(pt).shape == (3,) 
  def slice(self, slice_at='y', **kwargs):
    if slice_at == 'x':
      i1, i2 = 1, 2
    elif slice_at == 'y':
      i1, i2 = 0, 2
    elif slice_at == 'z':
      i1, i2 = 0, 1
    else:
      raise ValueError('Wrong slice coord: %s' % slice_at)
    self.sliced = []
    for i, elem in enumerate(self.all):
      #assert len(val) == 3 # IT CAN HAVE METADATA
      self.sliced.append(np.array([elem[i1], elem[i2]]))
    return self.sliced
  def plot_slice(self, ax=None, **kwargs):
    """
    """
    annotate = kw('annotate', False, kwargs)
    annoffset = kw('annoffset', 0, kwargs)
    alpha = kw('alpha', 0.7, kwargs)
    marker = kw('marker', '.', kwargs)
    markersize = kw('markersize', 5, kwargs)
    markeredgecolor = kw('markeredgecolor', 'k', kwargs)
    markerfacecolor = kw('markerfacecolor', 'none', kwargs) # EMPTY MARKERS
    if ax is None:
      ax = plt.gca()

    self.slice(**kwargs)

    if annotate: 
      for key, val in self.items():
        ax.annotate(key, (val[0]+annoffset, val[1]+annoffset), clip_on=True) # clip_on IS REQUIRED

    ax.plot([i[0] for i in self.sliced], [i[1] for i in self.sliced], 
        '.',
        alpha=alpha, 
        marker=marker, 
        markersize=markersize, 
        markeredgecolor=markeredgecolor,
        markerfacecolor=markerfacecolor,
         )
  def plot_3slices(self, fig, **kwargs): # LEGACY
    d = self.read(**dict(kwargs, unit='node'))
    s3 = kwargs.get('slice', 'y') #FIXME: THIS MUST BE MERGED WITH arr3d
    s1, s2 = [i for i in ['x', 'y', 'z'] if i != s3]
    s = [s1, s2, s3]

    for i in range(3):
      self.plot_slice(s[i], fig.axes[i])
  def plot(self, *args, **kwargs):
    self.plot_slice(*args, **kwargs)