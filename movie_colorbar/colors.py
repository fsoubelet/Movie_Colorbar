"""
Colors
------

Module with functions to handle color calculations and conversions.
"""

from colorsys import hls_to_rgb as _hls_to_rgb
from colorsys import hsv_to_rgb as _hsv_to_rgb
from colorsys import rgb_to_hls as _rgb_to_hls
from colorsys import rgb_to_hsv as _rgb_to_hsv
from colorsys import rgb_to_yiq as _rgb_to_yiq
from colorsys import yiq_to_rgb as _yiq_to_rgb

from movie_colorbar.jit import maybe_jit

# We re-export the colorsys functions with a
# potential JIT-compilation by numba
cs_rgb_to_yiq = maybe_jit(_rgb_to_yiq)
cs_yiq_to_rgb = maybe_jit(_yiq_to_rgb)
cs_rgb_to_hls = maybe_jit(_rgb_to_hls)
cs_hls_to_rgb = maybe_jit(_hls_to_rgb)
cs_rgb_to_hsv = maybe_jit(_rgb_to_hsv)
cs_hsv_to_rgb = maybe_jit(_hsv_to_rgb)


@maybe_jit
def convert_rgb_to_xyz(R: float, G: float, B: float) -> tuple[float, float, float]:
    """
    Converts a color from the sRGB to the CIE XYZ 1931 colorspace.
    The colorsys module does not provide an implementation for this
    conversion so I wrote a custom one.

    Optimized for Numba JIT compilation.

    Parameters
    ----------
    R : float
        The red component of the color (0-255).
    G : float
        The green component of the color (0-255).
    B : float
        The blue component of the color (0-255).

    Returns
    -------
    tuple[float, float, float]
        A tuple with the X, Y, Z values of the color.
    """

    # Normalize and gamma correct each color channel
    def normalize_and_correct_gamma(value: float) -> float:
        value = value / 255.0  # To make sure we are in the [0, 1] range
        if value > 0.04045:
            return ((value + 0.055) / 1.055) ** 2.4
        return value / 12.92

    r = normalize_and_correct_gamma(R)
    g = normalize_and_correct_gamma(G)
    b = normalize_and_correct_gamma(B)

    # Compute XYZ using the transformation matrix (D65 illuminant)
    # and also scale to be in the [0, 100] range
    X = 100 * (r * 0.4124 + g * 0.3576 + b * 0.1805)
    Y = 100 * (r * 0.2126 + g * 0.7152 + b * 0.0722)
    Z = 100 * (r * 0.0193 + g * 0.1192 + b * 0.9505)
    return X, Y, Z


@maybe_jit
def convert_xyz_to_rgb(X: float, Y: float, Z: float) -> tuple[float, float, float]:
    """
    Converts a color from CIE XYZ 1931 to the sRGB colorspace.
    The colorsys module does not provide an implementation for this
    conversion so I wrote a custom one.

    Optimized for Numba JIT compilation.

    Parameters
    ----------
    X : float
        The X value of the color (0-100).
    Y : float
        The Y value of the color (0-100).
    Z : float
        The Z value of the color (0-100).

    Returns
    -------
    tuple[float, float, float]
        A tuple with the R, G, and B components of the color.
    """

    # To make sure we are in the [0, 1] range
    x = X / 100
    y = Y / 100
    z = Z / 100

    # Apply the inverse transformation matrix (D65 illuminant)
    # to compute the linear RGB components
    rl = x * 3.2406 + y * -1.5372 + z * -0.4986
    gl = x * -0.9689 + y * 1.8758 + z * 0.0415
    bl = x * 0.0557 + y * -0.2040 + z * 1.0570

    #  Apply gamma correction to each color channel
    def correct_gamma(value: float) -> float:
        if value > 0.0031308:
            return 1.055 * (value ** (1 / 2.4)) - 0.055
        return 12.92 * value

    # Apply Gamma correction
    r = correct_gamma(rl)
    g = correct_gamma(gl)
    b = correct_gamma(bl)

    # Clamp values to the [0, 1] range and scale to [0, 255]
    R = max(0, min(1, r)) * 255
    G = max(0, min(1, g)) * 255
    B = max(0, min(1, b)) * 255
    return R, G, B


@maybe_jit
def convert_xyz_to_lab(X: float, Y: float, Z: float) -> tuple[float, float, float]:
    """
    Converts a color from the CIE XYZ 1931 to the LAB colorspace.
    The colorsys module does not provide an implementation for this
    conversion so I wrote a custom one.

    Optimized for Numba JIT compilation.

    Parameters
    ----------
    X : float
        The X value of the color (0-100).
    Y : float
        The Y value of the color (0-100).
    Z : float
        The Z value of the color (0-100).

    Returns
    -------
    tuple[float, float, float]
        A tuple with the Lightness (L), A channel and B channel values.
    """
    # Normalize XYZ by reference white (D65 illuminant)
    x = X / 95.047
    y = Y / 100.0
    z = Z / 108.883

    # Nonlinear transformation to align with human perception
    def nonlinear_transform(value: float) -> float:
        if value > 0.008856:
            return value ** (1 / 3)
        return 7.787 * value + 16.0 / 116.0

    xf = nonlinear_transform(x)
    yf = nonlinear_transform(y)
    zf = nonlinear_transform(z)

    # Compute the LAB components
    L = 116 * yf - 16
    A = 500 * (xf - yf)
    B = 200 * (yf - zf)
    return L, A, B


@maybe_jit
def convert_lab_to_xyz(L: float, A: float, B: float) -> tuple[float, float, float]:
    """
    Converts a color from the LAB to the CIE XYZ 1931 colorspace.
    The colorsys module does not provide an implementation for this
    conversion so I wrote a custom one.

    Optimized for Numba JIT compilation.

    Parameters
    ----------
    L : float
        The lightness value of the color.
    A : float
        The A channel value of the color.
    B : float
        The B channel value of the color.

    Returns
    -------
    tuple[float, float, float]
        A tuple with the X, Y, Z values of the color.
    """
    # Calculate the intermediate XYZ values
    yf = (L + 16) / 116
    xf = A / 500 + yf
    zf = yf - B / 200

    # Reverse the nonlinear transformation for XYZ components
    def reverse_nonlinear_transform(value: float) -> float:
        if value**3 > 0.008856:
            return value**3
        return (value - 16.0 / 116.0) / 7.787

    # These are the normalized XYZ by reference white (D65 illuminant)
    x = reverse_nonlinear_transform(xf)
    y = reverse_nonlinear_transform(yf)
    z = reverse_nonlinear_transform(zf)

    # Scale back by the reference white (D65 illuminant)
    X = x * 95.047
    Y = y * 100.0
    Z = z * 108.883
    return X, Y, Z
