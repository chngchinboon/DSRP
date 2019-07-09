import sympy as sp
import numpy as np

def set_axes_radius(ax, origin, radius):
    # https://stackoverflow.com/a/50664367
    ax.set_xlim3d([origin[0] - radius, origin[0] + radius])
    ax.set_ylim3d([origin[1] - radius, origin[1] + radius])
    ax.set_zlim3d([origin[2] - radius, origin[2] + radius])


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.
    https://stackoverflow.com/a/50664367

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    limits = np.array([
        ax.get_xlim3d(),
        ax.get_ylim3d(),
        ax.get_zlim3d(),
    ])

    origin = np.mean(limits, axis=1)
    radius = 0.5 * np.max(np.abs(limits[:, 1] - limits[:, 0]))
    set_axes_radius(ax, origin, radius)
    return radius


class FrameTransform:
    def __init__(self):
        self.T = np.matrix(np.eye(4))

    def rotx(self, angle):
        if isinstance(angle, sp.symbol.Symbol):
            theta = angle
            T = sp.Matrix([[1, 0, 0, 0],
                           [0, sp.cos(theta), -1 * sp.sin(theta), 0],
                           [0, sp.sin(theta), sp.cos(theta), 0],
                           [0, 0, 0, 1]])
        else:
            theta = np.deg2rad(angle)
            T = np.matrix([[1, 0, 0, 0],
                           [0, np.cos(theta), -1 * np.sin(theta), 0],
                           [0, np.sin(theta), np.cos(theta), 0],
                           [0, 0, 0, 1]])
            T[np.abs(T) < np.finfo(float).eps] = 0
        return T

    def roty(self, angle):
        if isinstance(angle, sp.symbol.Symbol):
            theta = angle
            T = sp.Matrix([[sp.cos(theta), 0, sp.sin(theta), 0],
                           [0, 1, 0, 0],
                           [-1 * sp.sin(theta), 0, sp.cos(theta), 0],
                           [0, 0, 0, 1]])
        else:
            theta = np.deg2rad(angle)
            T = np.matrix([[np.cos(theta), 0, np.sin(theta), 0],
                           [0, 1, 0, 0],
                           [-1 * np.sin(theta), 0, np.cos(theta), 0],
                           [0, 0, 0, 1]])
            T[np.abs(T) < np.finfo(float).eps] = 0
        return T

    def rotz(self, angle):
        if isinstance(angle, sp.symbol.Symbol):
            theta = angle
            T = sp.Matrix([[sp.cos(theta), -1 * sp.sin(theta), 0, 0],
                           [sp.sin(theta), sp.cos(theta), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        else:
            theta = np.deg2rad(angle)
            T = np.matrix([[np.cos(theta), -1 * np.sin(theta), 0, 0],
                           [np.sin(theta), np.cos(theta), 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
            T[np.abs(T) < np.finfo(float).eps] = 0
        return T

    def translate(self, in_mat, op_mat):
        T = in_mat
        if isinstance(op_mat, list) or isinstance(op_mat, tuple) or isinstance(op_mat, np.ndarray):
            op = np.array(op_mat)
            arrayshape = op.shape
            if (arrayshape == (3, 1)) | (arrayshape == (3,)) | (arrayshape == (1, 3)):  # position only
                T[0:3, 3] += op.reshape(3, 1)
            else:
                raise TypeError(f'Error: Unknown shape of input array {arrayshape}')
        return T

    def transform(self, *args):
        # function to transform coord sys with input matrix
        Targs = np.zeros((len(args), 4, 4))

        # sanitize inputs to np.arrays.
        for idx, arg in enumerate(args):
            if isinstance(arg, list) or isinstance(arg, tuple) or isinstance(arg, np.ndarray):
                input_array = np.array(arg)
                arrayshape = input_array.shape
                Targ = np.eye(4)
                if arrayshape == (4, 4):  # full 4x4 homogenous matrix
                    Targ = input_array
                elif (arrayshape == (3, 1)) | (arrayshape == (3,)) | (arrayshape == (1, 3)):  # position only
                    Targ[0:3, 3:4] = input_array.reshape(3, 1)
                elif arrayshape == (3, 3):  # orientation only
                    Targ[0:3, 0:3] = input_array
                else:
                    raise TypeError(f'Error: Unknown shape of input array {arrayshape}')
            else:
                raise TypeError(f'Error: arg {arg} is not a numpy array')

            Targs[idx, :, :] = Targ

        output = self.cumprodmat(Targs)

        return output[-1]

    def cumprodmat(self, matlist):
        cumprodout = np.zeros((len(matlist), 4, 4))
        for idx, mat in enumerate(matlist):
            if idx == 0:
                cumprodout[0, :, :] = mat
            else:
                cumprodout[idx, :, :] = np.dot(cumprodout[idx - 1, :, :], mat)
        return cumprodout

    def reset(self):
        self.T = np.matrix(np.eye(4))


class coordsys:
    def __init__(self, *args):

        self.T = np.eye(4)
        self.name = None

        if args:
            # if len(args) > 1:
            #     raise TypeError(f'Args > 1. Use only one numpy.ndarray')

            for arg in args:
                if isinstance(arg, np.ndarray):
                    arrayshape = arg.shape
                    if arrayshape == (4, 4):  # full 4x4 homogenous matrix
                        self.T = arg
                    elif (arrayshape == (3, 1)) | (arrayshape == (3,)) | (arrayshape == (1, 3)):  # position only
                        self.T[0:3, 3] = arg.reshape(3, 1)
                    elif arrayshape == (3, 3):  # orientation only
                        self.T[0:3, 0:3] = arg
                    else:
                        raise TypeError(f'Error: Unknown shape of input array {arrayshape}')
                if isinstance(arg, str):
                    self.name = arg

        self.visible = True
        self.axhdl = None
        self.xhdl = None
        self.yhdl = None
        self.zhdl = None
        self.syslabelhdl = None
        self.length = 0.1
        self.linewidths = 2
        self.nameoffset = 0.1

    def plot(self, ax, **kwargs):
        # function to plot coord sys given ax
        # self.T needs to be a 4x4 numpy array!
        # following solidworks axis colors: x = red, y = green, z = blue
        if 'colorspec' in kwargs:
            colorspec = kwargs['colorspec']
        else:
            colorspec = ['r', 'g', 'b']

        if 'length' in kwargs:
            self.length = kwargs['length']

        if 'nameoffset' in kwargs:
            self.nameoffset = kwargs['nameoffset']

        if 'linewidths' in kwargs:
            self.linewidths = kwargs['linewidths']

        self.axhdl = ax

        [xu, yu, zu, px], [xv, yv, zv, py], [xw, yw, zw, pz] = self.T[0:3, :]

        self.xhdl = self.axhdl.quiver(px, py, pz, xu, xv, xw, color=colorspec[0], length=self.length,
                                      linewidths=self.linewidths, normalize=True)
        self.yhdl = self.axhdl.quiver(px, py, pz, yu, yv, yw, color=colorspec[1], length=self.length,
                                      linewidths=self.linewidths, normalize=True)
        self.zhdl = self.axhdl.quiver(px, py, pz, zu, zv, zw, color=colorspec[2], length=self.length,
                                      linewidths=self.linewidths, normalize=True)

        if self.name:
            self.syslabelhdl = self.axhdl.text(*(self.T[0:3, 3] - self.nameoffset), self.name)

    def set_label(self, text):
        self.name = text
        self.syslabelhdl.set_text(self.name)

    def P(self):
        return self.T[0:3, 3]

    def R(self):
        return self.T[0:3, 0:3]

    def xhat(self):
        return self.T[0:3, 0]

    def yhat(self):
        return self.T[0:3, 1]

    def zhat(self):
        return self.T[0:3, 2]

    def update(self, arg, refresh=False):
        if isinstance(arg, list) or isinstance(arg, tuple) or isinstance(arg, np.ndarray):
            arg = np.array(arg)
        if isinstance(arg, np.ndarray):
            arrayshape = arg.shape
            if arrayshape == (4, 4):  # full 4x4 homogenous matrix
                self.T = arg
            elif (arrayshape == (3, 1)) | (arrayshape == (3,)) | (arrayshape == (1, 3)):  # position only
                self.T[0:3, 3] = arg.reshape(3, 1)
            elif arrayshape == (3, 3):  # orientation only
                self.T[0:3, 0:3] = arg
            else:
                raise TypeError(f'Error: Unknown shape of input array {arrayshape}')

            if refresh:
                self.refresh()

        else:
            raise TypeError('Error: input is not a numpy array')

    def refresh(self):  # update plot
        self.remove()
        self.plot(self.axhdl)
        if self.name:
            print(f'Refreshing {self.name}')
        else:
            print(f'Refreshing {self.axhdl}')

    def remove(self):
        self.xhdl.remove()
        self.yhdl.remove()
        self.zhdl.remove()
        self.syslabelhdl.remove()


class DRSP:
    def __init__(self):
        self.q_1, self.q_2, self.q_3, self.q_4, self.azimuth = sp.symbols('q_1 q_2 q_3 q_4 az')
        # self.azimuth = azimuth
        self.rotx90 = sp.Matrix([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
        self.roty90 = sp.Matrix([[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, 0], [0, 0, 0, 1]])
        self.ft = FrameTransform()
        self.ft.q_1 = self.q_1
        self.ft.q_2 = self.q_2

    def get_xhat(self):
        self.xhat = sp.Matrix([1, 0, 0])  # unit vector of x-axis
        self.xhat_M = sp.eye(4) * self.roty90

    def get_azmod(self):
        self.azmod = sp.Matrix(
            [[sp.cos(self.azimuth), -sp.sin(self.azimuth), 0], [sp.sin(self.azimuth), sp.cos(self.azimuth), 0],
             [0, 0, 1]])
        self.azmod_M = sp.eye(4)
        self.azmod_M[0:3, 0:3] = self.azmod

    def get_yhat(self):
        self.default_yhat = sp.Matrix([0, 1, 0])  # unit vector of y-axis
        self.default_yhat_M = sp.eye(4) * self.roty90
        self.yhat = self.azmod * self.xhat
        self.yhat_M = self.azmod_M * self.default_yhat_M
        # self.yhat = (self.xhat.T*self.azmod).T

    def get_y_plane(self):
        # vector projection of joystick onto YZ plane. starts from positive y-axis and goes anti clockwise
        self.jyz = sp.Matrix([0, sp.cos(self.q_1), sp.sin(self.q_1)])
        # jxz = [sin(q2),0,cos(q2)] # vector projection of joystick onto XZ plane.
        self.XOE = self.xhat.cross(self.jyz)  # normal vector used to define plane XOE
        self.XOE_M = self.xhat_M * self.ft.rotz(self.q_1)

    def get_x_plane(self):
        # vector projection of joystick onto XZ plane. starts from negative x-axis and goes anticlockwise
        self.jxz = sp.Matrix([-sp.cos(self.q_2), 0, sp.sin(self.q_2)])
        # jxz = [cos(q2),0,sin(q2)] # vector projection of joystick onto XZ plane. starts from positive x-axis and goes clockwise
        self.YOE = self.yhat.cross(self.jxz)  # normal vector used to define plane YOE
        self.YOE_M = self.yhat_M * self.ft.rotz(self.q_2)

    def get_interserction(self):
        self.jz = self.XOE.cross(self.YOE)  # intersection of both planes, i.e. z-axis of joystick
        # normjz = simple((sum(jz.^2))^0.5) #(s1^2*s2^2 - s1^2 + 1)^(1/2)= (1-c1^2*s2^2)^(1/2)
        # normjz = (1-cos(q1)^2*sin(q2)^2)^0.5 # even more simplifed form #sala? should be (1 - cos(q1)^2*cos(q2)^2)^(1/2)
        self.normjz = self.jz.norm()
        self.normjz_simplified = sp.sqrt(1 - sp.cos(self.q_1) ** 2 * sp.cos(self.q_2) ** 2)
        self.jzhat = self.jz / self.normjz_simplified  # unit vector z-axis of joystick

    def get_M(self):
        self.jz_M = self.XOE_M[0:3, 0].cross(self.YOE_M[0:3, 0])  # intersection of both planes, i.e. z-axis of joystick
        # self.normjz_M = self.jz_M.norm()
        self.normjz_M = (self.jz_M.T * self.jz_M) ** 0.5
        self.jzhat_M = self.jz_M / self.normjz_M

        self.jyhat_M = self.YOE_M[0:3, 0]

        self.jx_M = self.jyhat_M.cross(self.jzhat_M)
        # self.normjx_M = self.jx_M.norm()
        self.normjx_M = (self.jx_M.T*self.jx_M) ** 0.5
        self.jxhat_M = self.jx_M / self.normjx_M

    def get_rotation_matrix(self):
        self.jyhat = -self.XOE  # make x-axis of joystick to be on XOE plane. Since x & z-axis used to make xoe plane and y-axis has to perpendicular to both,
        # y-axis is thus perpendicular to XOE, i.e. the norm of XOE.
        # make x-axis to be on xoe plane, and hence to find y axis, cross(jyz,xhat) or y=z X x. therefore jyhat=-(XOE), !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.jxhat = self.jyhat.cross(
            self.jzhat)  # already unit vector, since jzhat and jyhat are perpendicular and are unit vectors.

        self.R0S = sp.BlockMatrix([[self.jxhat, self.jyhat, self.jzhat]]).as_explicit()
        self.R0S_M = sp.BlockMatrix([[self.jxhat_M, self.jyhat_M, self.jzhat_M]]).as_explicit()  # todo: check

    def get_tf_sp(self):
        self.T0S = sp.BlockMatrix([[self.R0S, sp.zeros(3, 1)],
                                   [sp.zeros(1, 3),
                                    sp.eye(1)]]).as_explicit()  # Transformation function for parallel system.
        self.T0S_M = sp.BlockMatrix([[self.R0S_M, sp.zeros(3, 1)],
                                     [sp.zeros(1, 3),
                                      sp.eye(1)]]).as_explicit()  # Transformation function for parallel system.

    def get_tf_end(self):
        self.TSE = sp.Matrix([[sp.cos(self.q_3), -sp.sin(self.q_3), 0, 0], [sp.sin(self.q_3), sp.cos(self.q_3), 0, 0],
                              [0, 0, 1, self.q_4],
                              [0, 0, 0, 1]])  # knob/yaw angle with height of joystick

        self.T0E = self.T0S * self.TSE  # Forward kinematics
        self.T0E_M = self.T0S_M * self.TSE  # Forward kinematics

    def get_aJ(self):
        self.T0E_M

    def populate(self):
        self.get_xhat()
        self.get_azmod()
        self.get_yhat()
        self.get_y_plane()
        self.get_x_plane()
        self.get_interserction()
        self.get_M()
        self.get_rotation_matrix()
        self.get_tf_sp()
        self.get_tf_end()
        self.func_T0E = sp.lambdify([self.q_1, self.q_2, self.q_3, self.q_4, self.azimuth], self.T0E, 'numpy')
        self.func_T0E_M = sp.lambdify([self.q_1, self.q_2, self.q_3, self.q_4, self.azimuth], self.T0E_M, 'numpy')
        self.func_T0S_M = sp.lambdify([self.q_1, self.q_2, self.q_3, self.q_4, self.azimuth], self.T0S_M, 'numpy')
        self.func_XOE_M = sp.lambdify([self.q_1, self.q_2, self.q_3, self.q_4, self.azimuth], self.XOE_M, 'numpy')
        self.func_YOE_M = sp.lambdify([self.q_1, self.q_2, self.q_3, self.q_4, self.azimuth], self.YOE_M, 'numpy')


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D, art3d

    # from test.projection import data

    x_arc_radius = 100
    y_arc_radius = 110
    motor_x = [100, 0, 0]
    motor_y = [0, 100, 0]
    tool_tip = 100

    numpoints = 5
    adiff = 85
    mina = 90 - adiff
    maxa = 90 + adiff

    stepsize = (maxa - mina) / numpoints

    anglevectd = np.linspace(mina, maxa, numpoints)
    anglevectrad = np.deg2rad(anglevectd)
    meshx, meshy = np.meshgrid(anglevectrad, anglevectrad)
    q3 = np.zeros(meshx.shape)
    q4 = tool_tip * np.ones(meshx.shape)

    q = np.dstack((meshx, meshy, q3, q4)).reshape(np.multiply(*meshx.shape), 4)

    # T0S, T0E = boon_sp(np.pi / 4)
    #
    # q_1, q_2, q_3, q_4 = sp.symbols('q_1 q_2 q_3 q_4')
    # T0E = sp.lambdify([q_1, q_2, q_3, q_4], T0E, 'numpy')
    # T0E = np.array([T0E(*joint_pos)[0:3, 3] for joint_pos in q])
    azimuth = np.pi / 2
    # mechanism = DRSP(azimuth)
    mechanism = DRSP()
    mechanism.populate()
    # func_T0E = mechanism.func_T0E
    # pos = 6
    pos = 6
    # q_1, q_2, q_3, q_4 = q[pos:pos+1][0]
    q_1 = np.deg2rad(47.5)
    q_2 = np.deg2rad(47.5 + 90 * 3 / 4)
    q_3 = 0
    q_4 = 120

    q_point = [q_1, q_2, q_3, q_4, azimuth]

    # vector
    # T0E = np.array([mechanism.func_T0E(*joint_pos) for joint_pos in q[pos:pos+1]])
    T0E = np.array([mechanism.func_T0E(*q_point)])
    P0E = T0E[0][0:3, 3]
    R0E = T0E[0][0:3, 0:3]

    # matrix
    T0E_M = np.array([mechanism.func_T0E_M(*q_point)])
    P0E_M = T0E_M[0][0:3, 3]
    R0E_M = T0E_M[0][0:3, 0:3]

    T0S_M = np.array([mechanism.func_T0S_M(*q_point)])
    X0E_M = np.array([mechanism.func_XOE_M(*q_point)])
    Y0E_M = np.array([mechanism.func_YOE_M(*q_point)])

    # spherical visualization setup
    fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    ax.set_title('Workspace')
    ax.set_aspect('equal')
    ax.view_init(elev=16, azim=45)

    ax.set_xlabel('X', fontsize=20)
    ax.set_ylabel('Y', fontsize=20)
    ax.set_zlabel('Z', fontsize=20)
    # data_extent = set_axes_equal(ax)
    data_extent = 150
    set_axes_radius(ax, np.zeros(3, ), data_extent)

    # plot origin
    origin = coordsys('{O}')
    origin.plot(ax, length=data_extent / 5, nameoffset=np.array([10, 20, 20]))

    tfmat = FrameTransform() # for quick coordinate transformation use

    # plotting coordinate rotation after q1
    xrot = coordsys('{$\^X_m$}')
    xrot.plot(ax, length=data_extent / 5, nameoffset=np.array([0, -10, 25]))
    xrot.update(tfmat.translate(tfmat.roty(90), [y_arc_radius, 0, 0])) #shifted y_arc_radius along x
    xrot.refresh()
    ax.plot(*zip(np.zeros(3, ), xrot.T[0:3, 3]), label='X-motor', color='pink') #x-axis line

    # arc points
    arc_pts = np.array([[0, np.cos(theta - np.pi / 2), np.sin(theta - np.pi / 2)] \
                        for theta in np.linspace(0, np.pi, 10)])
    planepts = np.array([[0, 0, 0, 0],
                         [0, 1, 1, 0],
                         [-1, -1, 1, 1]])

    # x_arc plot
    arc_xpts = x_arc_radius * arc_pts
    arc_xpts2 = np.dot(Y0E_M[0][0:3, 0:3], arc_xpts.T).T #apply to rotation of q1

    # plotting arc and plane
    ax.plot3D(arc_xpts2[:, 0], arc_xpts2[:, 1], arc_xpts2[:, 2], label='Y-arc', color='violet', linewidth=5)
    ax.text(*arc_xpts2[int(len(arc_xpts2) / 2)] - np.array([0, 100, -5]), '$\^YOE$')

    yoe_pts = np.dot(Y0E_M[0][0:3, 0:3], planepts*x_arc_radius).T
    yoe = art3d.Poly3DCollection([yoe_pts], alpha=0.5)
    yoe.set_facecolor('pink')
    ax.add_collection3d(yoe)

    # plotting coordinate rotation after q2
    yrot = coordsys(r'{$\^Y_m$}')
    yrot.plot(ax, length=data_extent / 5, nameoffset=np.array([0, -10, 25]))
    yrot.update(np.matrix(tfmat.transform(np.array(mechanism.azmod.subs('az', azimuth)))) * tfmat.translate(tfmat.roty(90),[x_arc_radius, 0, 0]))
    yrot.refresh()
    ax.plot(*zip(np.zeros(3, ), yrot.T[0:3, 3]), label='Y-motor', color='cyan') # y-axis line

    # y_arc plot
    arc_ypts = y_arc_radius * arc_pts
    arc_ypts2 = np.dot(X0E_M[0][0:3, 0:3], arc_ypts.T).T
    ax.plot3D(arc_ypts2[:, 0], arc_ypts2[:, 1], arc_ypts2[:, 2], label='X-arc', color='turquoise',linewidth=5)
    ax.text(*arc_ypts2[int(len(arc_ypts2) / 2)] - np.array([100, 0, -10]), '$\^XOE$')

    xoe_pts = np.dot(X0E_M[0][0:3, 0:3], planepts*y_arc_radius).T
    xoe = art3d.Poly3DCollection([xoe_pts], alpha=0.5)
    xoe.set_facecolor('lightblue')
    ax.add_collection3d(xoe)

    # plot endeffector positions
    endeff_M = coordsys(f'{{E}},($q_3$={q_3}$^\circ$, $q_4$={q_4})')
    endeff_M.update(T0E_M[0])
    endeff_M.plot(ax, length=data_extent / 5, nameoffset=np.array([-50, 0, -35]))
    endeff_M.refresh()

    # spherical_M = coordsys('T0S')
    # spherical_M.update(T0S_M[0])
    # spherical_M.plot(ax, length=data_extent / 5)
    # spherical_M.refresh()

    Xplane_M = coordsys(f'{{$\^X$}},($q_1$={np.rad2deg(q_1)}$^\circ$)')
    X0E_M[0][0:3, 3] = [150, 0, 0]
    Xplane_M.update(X0E_M[0])
    Xplane_M.plot(ax, length=data_extent / 5, nameoffset=np.array([-60, 0, -35]))
    Xplane_M.refresh()

    Yplane_M = coordsys(f'{{$\^Y$}},($q_2$={np.rad2deg(q_2)}$^\circ$)')
    Y0E_M[0][0:3, 3] = Y0E_M[0][0:3, 2] * 150
    Yplane_M.update(Y0E_M[0])
    Yplane_M.plot(ax, length=data_extent / 5, nameoffset=np.array([10, 0, -25]))
    Yplane_M.refresh()

    ax.plot3D(*zip(np.zeros(3, ), P0E_M), label='tool', color='indigo')

    print(f'q1: {np.rad2deg(q_1)}, q2: {np.rad2deg(q_2)}, q3: {np.rad2deg(q_3)}, q4: {q_4}')

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.set_title('Boon')
    ax2.set_aspect('equal')

    ax2.set_xlabel('X', fontsize=20)
    ax2.set_ylabel('Y', fontsize=20)
    ax2.set_zlabel('Z', fontsize=20)
    # data_extent = set_axes_equal(ax)
    data_extent2 = 150
    set_axes_radius(ax2, np.zeros(3, ), data_extent2)

    # data mesh
    # numpoints = 20
    # adiff = 85
    # mina = 90 - adiff
    # maxa = 90 + adiff
    #
    # stepsize = (maxa - mina) / numpoints
    #
    # anglevectd = np.linspace(mina, maxa, numpoints)
    # anglevectrad = np.deg2rad(anglevectd)
    # meshx, meshy = np.meshgrid(anglevectrad, anglevectrad)
    # q3 = np.zeros(meshx.shape)
    # q4 = tool_tip * np.ones(meshx.shape)
    # az = azimuth * np.ones(meshx.shape)
    #
    # q = np.dstack((meshx, meshy, q3, q4, az)).reshape(np.multiply(*meshx.shape), 5)
    # data_M = np.array([mechanism.func_T0E_M(*joint_pos) for joint_pos in q])
    # datahdl = ax2.scatter(data_M[:, 0], data_M[:, 1], data_M[:, 2], c='b')

    plt.show()
