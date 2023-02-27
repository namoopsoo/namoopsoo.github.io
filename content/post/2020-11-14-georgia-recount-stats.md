

#### Binomial Distribution
Plot Binomial distribution for `p`, and a sample of `n`
```python

from scipy.stats import binom
import numpy as np
import matplotlib.pyplot as plt
import pylab
workdir = '_posts/2020-11-14-georgia-recount-stats_files'       

fig, ax = plt.subplots(1, 1)
n, p = 5, 0.4
mean, var, skew, kurt = binom.stats(n, p, moments='mvsk')

x = np.arange(binom.ppf(0.01, n, p),

              binom.ppf(0.99, n, p))

ax.plot(x, binom.pmf(x, n, p), 'bo', ms=8, label='binom pmf')

ax.vlines(x, 0, binom.pmf(x, n, p), colors='b', lw=5, alpha=0.5)

out_loc = f'{workdir}/foo.png'
pylab.savefig(out_loc)
pylab.close()
```
