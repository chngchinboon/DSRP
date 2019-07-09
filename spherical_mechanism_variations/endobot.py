import sympy as sp

def endobot_fk():
    '''
    Based on endobot thesis by Hyosig Kang.
    :return: (H_steps, H_final)
    where
        H_steps is the homogenous transformation matrix based on the working steps
        H_final is the homogenous transformation matrix based on written matrix in thesis
    '''


    # q_i be the angle of rotation or linear displacement
    q_1, q_2, q_3, q_4 = sp.symbols('q_1 q_2 q_3 q_4')
    c_1 = sp.cos(q_1)
    c_2 = sp.cos(q_2)
    c_3 = sp.cos(q_3)
    s_1 = sp.sin(q_1)
    s_2 = sp.sin(q_2)
    s_3 = sp.sin(q_3)

    # Let h_i be a unit vector, which specifies the direction of rotation or translation
    h_1 = sp.Matrix([1, 0, 0])
    h_2 = sp.Matrix([0, 1, 0])
    h_3 = sp.Matrix([0, 0, 1])
    h_4 = sp.Matrix([0, 0, 1])

    # p_i,i+1 be the position vector between ith and (i + 1)th
    p_01 = sp.Matrix([0, 0, 0])
    p_12 = sp.Matrix([0, 0, 0])
    p_23 = sp.Matrix([0, 0, 0])

    p_34 = sp.Matrix([0, 0, q_4])
    p_4E = sp.Matrix([0, 0, 0])

    # exponentials are given by
    e_h1q1 = sp.Matrix([[1, 0, 0],
                        [0, c_1, -s_1],
                        [0, s_1, c_1]])

    e_h2q2 = sp.Matrix([[c_2, 0, s_2],
                        [0, 1, 0],
                        [-s_2, 0, c_2]])

    e_h3q3 = sp.Matrix([[c_3, -s_3, 0],
                        [s_3, c_3, 0],
                        [0, 0, 1]])

    e_h4q4 = sp.eye(3)

    # The product of exponentials formula gives the forward kinematics map:
    # R0 = R_04 = R_12*R_01*R_23*R_34 = e_h2q2*e_h1q1*e_h3q3*e_h4q4
    # p_0T = p_04 = p_01 + R_01*p_12 + R_12*R_01*p_23 + R_12*R_01*R_23*p_34 = e_h2q2*e_h1q1*e_h3q3*p_34

    R_12 = e_h2q2
    R_01 = e_h1q1
    R_23 = e_h3q3
    R_34 = e_h4q4

    R_04_steps = R_12*R_01*R_23*R_34
    p_0T_steps = e_h2q2*e_h1q1*e_h3q3*p_34
    H_steps = sp.BlockMatrix([[R_04_steps, p_0T_steps],[sp.zeros(1,3), sp.eye(1)]]).as_explicit()

    R_04_final = R_01*R_12*R_23*R_34
    p_0T_final = e_h1q1*e_h2q2*e_h3q3*p_34
    H_final = sp.BlockMatrix([[R_04_final, p_0T_final], [sp.zeros(1, 3), sp.eye(1)]]).as_explicit()

    return H_steps, H_final


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    numpoints = 25
    adiff = 90
    mina = 90 - adiff
    maxa = 90 + adiff

    stepsize = (maxa - mina)/ numpoints

    anglevectd = np.linspace(mina,maxa,numpoints)
    anglevectrad = np.deg2rad(anglevectd)
    meshx, meshy = np.meshgrid(anglevectrad,anglevectrad)
    q3 = np.zeros(meshx.shape)
    q4 = 100*np.ones(meshx.shape)

    q = np.dstack((meshx,meshy,q3,q4)).reshape(np.multiply(*meshx.shape),4)

    T0S, T0E = endobot_fk()

    q_1, q_2, q_3, q_4 = sp.symbols('q_1 q_2 q_3 q_4')
    T0E = sp.lambdify([q_1, q_2, q_3, q_4], T0E, 'numpy')
    T0E = np.array([T0E(*joint_pos)[0:3, 3] for joint_pos in q])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Boon')
    ax.scatter(T0E[:, 0], T0E[:, 1], T0E[:, 2], c='b')

    ax.set_xlabel('X', fontsize=20)
    ax.set_ylabel('Y', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)

    plt.show()
