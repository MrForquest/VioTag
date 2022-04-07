import numpy as np
from sklearn.decomposition import NMF

V = np.array([[0, 1, 0, 1, 2, 2],
              [2, 3, 1, 1, 2, 2],
              [1, 1, 1, 0, 1, 1],
              [0, 2, 3, 4, 1, 1],
              [0, 0, 0, 0, 1, 0]])
model = NMF(n_components=3, init='nndsvd', random_state=0)
W = model.fit_transform(V)
H = model.components_
narr = np.round(np.dot(W, H), 2)
# narr = np.interp(narr, (narr.min(), narr.max()), (0, +1))
for a in narr:
    for i in np.interp(a, (a.min(), a.max()), (0, +1)):
        print('{:.2f}'.format(i), end=" ")
    print()
print()
for a in narr:
    for i in a:
        print('{:.2f}'.format(i), end=" ")
    print()
