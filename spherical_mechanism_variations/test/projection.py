import numpy as np

h = 100

# az, q1, q2, x, y, z
data = [[30, 30, 30, 88.14, 23.62, 40.91],
        [30, 30, 45, 93.33, 17.96, 31.11],
        [30, 30, 60, 96.81, 12.52, 21.69],
        [30, 45, 30, 89.8, 31.11, 31.11],
        [30, 45, 45, 93.51, 25.06, 25.06],
        [30, 45, 45, 93.51, 25.06, 25.06],
        [30, 45, 60, 96.49, 18.57, 18.57],
        [30, 60, 30, 90.10, 37.56, 21.69],
        [30, 60, 45, 92.85, 32.16, 18.57],
        [30, 60, 60, 95.53, 25.6, 14.78],
        [45, 30, 30, 77.01, 31.90, 55.25],
        [45, 30, 45, 86.51, 25.08, 43.44],
        [45, 30, 60, 93.43, 17.82, 30.87],
        [45, 45, 30, 78.91, 43.44, 43.44],
        [45, 45, 45, 86.29, 35.74, 35.74],
        [45, 45, 60, 92.53, 26.82, 26.82],
        [45, 60, 30, 78.67, 53.46, 30.87],
        [45, 60, 45, 84.39, 46.46, 26.82],
        [45, 60, 60, 90.21, 37.37, 21.57],
        [60, 30, 30, 65.47, 37.80, 65.47],
        [60, 30, 45, 79, 30.65, 53.09],
        [60, 30, 60, 89.63, 22.18, 38.41],
        [60, 45, 30, 66.05, 53.09, 53.09],
        [60, 45, 45, 77.46, 44.72, 44.72],
        [60, 45, 60, 87.67, 34.02, 34.02],
        [60, 60, 30, 64.02, 66.53, 38.41],
        [60, 60, 45, 73.29, 58.92, 34.02],
        [60, 60, 60, 83.21, 48.04, 27.74],
        ]


if __name__ == '__main__':
    import numpy as np
    import sympy as sp
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    from boon_sp_gen import boon_sp

    data = np.array(data)
    P0E_sld = data[:,3:]
    az = data[:, 0]
    q1 = data[:, 1]
    q2 = data[:, 2]
    q3 = np.zeros(q1.shape)
    q4 = 100*np.ones(q1.shape)

    q = np.dstack((q1,q2,q3,q4)).reshape(len(q1),4)

    q_1, q_2, q_3, q_4 = sp.symbols('q_1 q_2 q_3 q_4')
    P0E = []
    for num, angles in enumerate(q): # should vectorize this but i don't know how :(
        T0S, T0E = boon_sp(num)
        T0E = sp.lambdify([q_1, q_2, q_3, q_4], T0E, 'numpy')
        P0E.append(T0E(*angles)[0:3, 3])

    P0E = np.array(P0E)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Model vs Solidworks')

    ax.scatter(P0E[:, 0], P0E[:, 1], P0E[:, 2], c='r', label = 'Calculated')
    ax.scatter(P0E_sld[:, 0], P0E_sld[:, 1], P0E_sld[:, 2], c='b', label = 'Solidworks')

    for line in np.array(list(zip(P0E, P0E_sld))):
        ax.plot(line[:, 0], line[:, 1], line[:, 2], c='g')

    ax.legend()
    ax.set_xlabel('X', fontsize=20)
    ax.set_ylabel('Y', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)

    plt.show()
