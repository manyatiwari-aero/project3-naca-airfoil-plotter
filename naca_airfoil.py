import numpy as np
import matplotlib.pyplot as plt

def naca4(number, n_points=100):
    """
    Generate NACA 4-digit airfoil coordinates.
    number: string like '2412' or '0012'
    n_points: number of points on each surface
    """
    # Extract the four digits
    m = int(number[0]) / 100      # max camber
    p = int(number[1]) / 10       # camber position
    t = int(number[2:]) / 100     # max thickness

    # x coordinates from 0 to 1 (chord length = 1)
    # use cosine spacing for better resolution near leading edge
    beta = np.linspace(0, np.pi, n_points)
    x = (1 - np.cos(beta)) / 2

    # thickness distribution
    yt = 5 * t * (0.2969*np.sqrt(x)
                - 0.1260*x
                - 0.3516*x**2
                + 0.2843*x**3
                - 0.1015*x**4)

    # camber line and gradient
   # handle symmetric airfoil (m=0 or p=0) separately
    if m == 0 or p == 0:
        yc = np.zeros_like(x)
        dyc = np.zeros_like(x)
    else:
        yc = np.where(x < p,
                      m/p**2 * (2*p*x - x**2),
                      m/(1-p)**2 * (1 - 2*p + 2*p*x - x**2))
        dyc = np.where(x < p,
                       2*m/p**2 * (p - x),
                       2*m/(1-p)**2 * (p - x))

    # angle of camber line
    theta = np.arctan(dyc)

    # upper and lower surface coordinates
    xu = x  - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x  + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    return xu, yu, xl, yl, x, yc

def plot_airfoil(number):
    xu, yu, xl, yl, x, yc = naca4(number)

    # extract info for labels
    m = int(number[0])
    p = int(number[1])
    t = int(number[2:])

    plt.figure(figsize=(10, 4))

    # plot upper surface
    plt.plot(xu, yu, 'b-', linewidth=2, label='Upper surface')

    # plot lower surface
    plt.plot(xl, yl, 'r-', linewidth=2, label='Lower surface')

    # plot camber line
    plt.plot(x, yc, 'g--', linewidth=1.5, label='Camber line')

    # plot chord line
    plt.axhline(y=0, color='k', linewidth=0.8,
                linestyle=':', label='Chord line')

    plt.xlabel('x/c (chord fraction)')
    plt.ylabel('y/c (chord fraction)')
    plt.title(f'NACA {number} Airfoil Profile')
    plt.legend()
    plt.axis('equal')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'naca_{number}.png', dpi=150,
                bbox_inches='tight')
    plt.show()

    # print key properties
    print(f"NACA {number} properties:")
    print(f"  Max camber:     {m}% of chord")
    print(f"  Camber position:{p*10}% of chord")
    print(f"  Max thickness:  {t}% of chord")
    if m == 0:
        print(f"  Type: Symmetric airfoil")
    else:
        print(f"  Type: Cambered airfoil")

# ── Run for multiple airfoils ──────────────────────
airfoils = ['0012', '2412', '4412']

for naca_num in airfoils:
    plot_airfoil(naca_num)
    print()