"""
Colors
------

Helper functions to handle color calculations and conversions.
"""
from new.jit import maybe_jit


@maybe_jit
def convert_rgb_to_xyz(r: float, g: float, b: float) -> tuple[float, float, float]:
    """
    Converts a color from the sRGB to the CIE XYZ 1931 colorspace.
    The colorsys module does not provide an implementation for this
    conversion so I wrote a custom one.

    Optimized for Numba JIT compilation.

    Parameters
    ----------
    r : float
        The red value of the color (0-255).
    g : float
        The green value of the color (0-255).
    b : float
        The blue value of the color (0-255).

    Returns
    -------
    tuple[float, float, float]
        A tuple with the X, Y, Z values of the color.
    """
    # Normalize and gamma correct each color channel
    def normalize_and_correct_gamma(value: float) -> float:
        value /= 255.0  # normalize to [0, 1] range
        if value > 0.04045:
            return ((value + 0.055) / 1.055) ** 2.4
        return value / 12.92

    r = normalize_and_correct_gamma(r)
    g = normalize_and_correct_gamma(g)
    b = normalize_and_correct_gamma(b)

    # Compute XYZ using the transformation matrix (D65 illuminant)
    # and also scale to be in the [0, 100] range
    x = 100 * (r * 0.4124 + g * 0.3576 + b * 0.1805)
    y = 100 * (r * 0.2126 + g * 0.7152 + b * 0.0722)
    z = 100 * (r * 0.0193 + g * 0.1192 + b * 0.9505)
    return x, y, z


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
        A tuple with the R, G, B values of the color.
    """
    # Normalize XYZ to the [0, 1] range
    x = X / 100.0
    y = Y / 100.0
    z = Z / 100.0

    # Apply the inverse transformation matrix (D65 illuminant)
    # to compute the linear RGB components
    rl = x * 3.2406 + y * -1.5372 + z * -0.4986
    gl = x * -0.9689 + y  * 1.8758 + z * 0.0415
    bl = x * 0.0557 + y * -0.2040 + z * 1.0570

    #  Apply gamma correction to each color channel and
    # clamp to [0, 1] range then scale to [0, 255]
    def correct_gamma(value: float) -> float:
        if value > 0.0031308:
            return 1.055 * (value ** (1 / 2.4)) - 0.055
        return 12.92 * value

    # Apply Gamma correction
    r = correct_gamma(rl)
    g = correct_gamma(gl)
    b = correct_gamma(bl)

    # Clamp values to the [0, 1] range and scale to [0, 255]
    r = max(0, min(1, r)) * 255
    g = max(0, min(1, g)) * 255
    b = max(0, min(1, b)) * 255
    return r, g, b
