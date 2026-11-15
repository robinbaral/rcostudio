# Swap the pink accent in a CrissCross screenshot for the yellow one, keeping antialiasing:
# each pixel is read as a mix of pink and grey (pixel = a*pink + c*grey) and rebuilt with yellow.
import sys, numpy as np
from PIL import Image
src, out = sys.argv[1], sys.argv[2]
P = np.array([255, 194, 209.]); Y = np.array([249, 200, 12.]); G = np.array([1, 1, 1.])
im = np.asarray(Image.open(src).convert("RGB")).astype(float)
A = np.stack([P, G], 1)                      # 3x2
coef, *_ = np.linalg.lstsq(A, im.reshape(-1, 3).T, rcond=None)
a = np.clip(coef[0], 0, None); c = coef[1]
recon = (A @ np.stack([a, c])).T
err = np.abs(recon - im.reshape(-1, 3)).max(1)
mask = (a > 0.02) & (err < 18)
new = im.reshape(-1, 3).copy()
new[mask] = (np.outer(a[mask], Y) + np.outer(c[mask], G))
Image.fromarray(np.clip(new, 0, 255).astype(np.uint8).reshape(im.shape)).save(out)
print(mask.sum())
