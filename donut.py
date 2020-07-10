# Esteban Garcia-Gurtubay Jan 2014

import math


def render_frame(A, B):

    # Precompute sines and cosines of A and B
    cosA = math.cos(A)
    sinA = math.sin(A)
    cosB = math.cos(B)
    sinB = math.sin(B)

    char_output = []
    zbuffer = []

    for i in range(screen_height + 1):
        char_output.append([' '] * (screen_width + 0))
        zbuffer.append([0] * (screen_width + 0))

    # theta goes around the cross-sectional circle of a torus
    theta = 0
    while (theta < 2* math.pi):
        theta += theta_spacing

        # Precompute sines and cosines of theta
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # phi goes around the center of revolution of a torus
        phi = 0
        while (phi < 2*math.pi):
            phi += phi_spacing

            # Precompute sines and cosines of phi
            cosphi = math.cos(phi)
            sinphi = math.sin(phi)

            # the x,y coordinate of the circle,
            # before revolving (factored out of the above equations)
            circlex = R2 + R1*costheta
            circley = R1*sintheta

            # final 3D (x,y,z) coordinate after rotations, directly from our math above
            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = K2 + cosA*circlex*sinphi + circley*sinA
            ooz = 1/z

            # x and y projection. y is negated here, because y goes up in
            # 3D space but down on 2D displays.
            xp = int(screen_width/2 + K1*ooz*x)
            yp = int(screen_height/2 - K1*ooz*y)

            # Calculate luminance
            L = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + cosB*(cosA*sintheta - costheta*sinA*sinphi)

            # L ranges from -sqrt(2) to +sqrt(2).  If it's < 0, the surface is
            # pointing away from us, so we won't bother trying to plot it.
            if L > 0:
                # Test against the z-buffer. Larger 1/z means the pixel is closer to
                # the viewer than what's already plotted.
                if ooz > zbuffer[xp][yp]:
                    zbuffer[xp][yp] = ooz
                    luminance_index = L*8   # this brings L into the range 0..11 (8*sqrt(2) = 11.3)

                    # Now we lookup the character corresponding
                    # to the luminance and plot it in our output
                    char_output[xp][yp] = '.,-~:;=!*#$@'[int(luminance_index)]

    # Now, dump char_output to the screen.
    # Bring cursor to "home" location, in just about any currently-used terminal emulation mode
    print('\x1b[H')
    for i in range(screen_height):
        for j in range(screen_width):
            print(char_output[i][j], end='')
        print()


theta_spacing = 0.07
phi_spacing = 0.02

R1 = 1
R2 = 2
K2 = 5

# Calculate K1 based on screen size: the maximum x-distance occurs roughly at
# the edge of the torus, which is at x=R1+R2, z=0.  we want that to be
# displaced 3/8ths of the width of the screen, which is 3/4th of the way from
# the center to the side of the screen.
# screen_width*3/8 = K1*(R1+R2)/(K2+0)
# screen_width*K2*3/(8*(R1+R2)) = K1

screen_width = 35
screen_height = 35

K1 = screen_width*K2*3/(8*(R1+R2))

print('\x1b[2J')
A = 1.0
B = 1.0

for i in range(250):
    render_frame(A, B)
    A += 0.08
    B += 0.03
