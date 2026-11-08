import math
import struct

def create_annular_cylinder_stl(r_inner, r_outer, height, z_offset=0.0, num_segments=72):
    """
    Generates triangles for a thick washer / annular ring shell.
    r_inner: inside radius (mm)
    r_outer: outside radius (mm)
    height: cylinder wall height (mm)
    z_offset: bottom z-coordinate
    """
    triangles = []
    z_bot = z_offset
    z_top = z_offset + height

    for i in range(num_segments):
        theta1 = 2.0 * math.pi * i / num_segments
        theta2 = 2.0 * math.pi * (i + 1) / num_segments

        # Points on circle
        x_out1 = r_outer * math.cos(theta1)
        y_out1 = r_outer * math.sin(theta1)
        x_out2 = r_outer * math.cos(theta2)
        y_out2 = r_outer * math.sin(theta2)

        x_in1 = r_inner * math.cos(theta1)
        y_in1 = r_inner * math.sin(theta1)
        x_in2 = r_inner * math.cos(theta2)
        y_in2 = r_inner * math.sin(theta2)

        # 1. Top face (annular ring surface)
        triangles.append(((x_in1, y_in1, z_top), (x_out1, y_out1, z_top), (x_out2, y_out2, z_top)))
        triangles.append(((x_in1, y_in1, z_top), (x_out2, y_out2, z_top), (x_in2, y_in2, z_top)))

        # 2. Bottom face
        triangles.append(((x_in1, y_in1, z_bot), (x_out2, y_out2, z_bot), (x_out1, y_out1, z_bot)))
        triangles.append(((x_in1, y_in1, z_bot), (x_in2, y_in2, z_bot), (x_out2, y_out2, z_bot)))

        # 3. Outer wall
        triangles.append(((x_out1, y_out1, z_bot), (x_out2, y_out2, z_bot), (x_out2, y_out2, z_top)))
        triangles.append(((x_out1, y_out1, z_bot), (x_out2, y_out2, z_top), (x_out1, y_out1, z_top)))

        # 4. Inner wall (facing inward)
        triangles.append(((x_in1, y_in1, z_bot), (x_in1, y_in1, z_top), (x_in2, y_in2, z_top)))
        triangles.append(((x_in1, y_in1, z_bot), (x_in2, y_in2, z_top), (x_in2, y_in2, z_bot)))

    return triangles

def create_disc_cover_stl(r_inner, r_outer, thickness, z_offset=0.0, num_segments=72):
    return create_annular_cylinder_stl(r_inner, r_outer, thickness, z_offset, num_segments)

def create_diffuser_ring_stl(r_inner, r_outer, height, z_offset=0.0, num_segments=72):
    return create_annular_cylinder_stl(r_inner, r_outer, height, z_offset, num_segments)

def calc_normal(p1, p2, p3):
    u = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    nx = u[1] * v[2] - u[2] * v[1]
    ny = u[2] * v[0] - u[0] * v[2]
    nz = u[0] * v[1] - u[1] * v[0]
    l = math.sqrt(nx*nx + ny*ny + nz*nz)
    if l < 1e-9:
        return (0.0, 0.0, 1.0)
    return (nx/l, ny/l, nz/l)

def write_binary_stl(filepath, triangles):
    header = b'Identity Disc Vault - Physical Case Shell 3D Model'.ljust(80, b' ')[:80]
    count = len(triangles)
    with open(filepath, 'wb') as f:
        f.write(header)
        f.write(struct.pack('<I', count))
        for t in triangles:
            n = calc_normal(t[0], t[1], t[2])
            f.write(struct.pack('<3f', n[0], n[1], n[2]))
            f.write(struct.pack('<3f', t[0][0], t[0][1], t[0][2]))
            f.write(struct.pack('<3f', t[1][0], t[1][1], t[1][2]))
            f.write(struct.pack('<3f', t[2][0], t[2][1], t[2][2]))
            f.write(struct.pack('<H', 0))

def write_obj(filepath, triangles, obj_name="IdentityDisc"):
    vertices = []
    v_map = {}
    faces = []

    def get_v_idx(pt):
        # Round to 4 decimals to weld close vertices
        key = (round(pt[0], 4), round(pt[1], 4), round(pt[2], 4))
        if key not in v_map:
            v_map[key] = len(vertices) + 1
            vertices.append(key)
        return v_map[key]

    for t in triangles:
        i1 = get_v_idx(t[0])
        i2 = get_v_idx(t[1])
        i3 = get_v_idx(t[2])
        faces.append((i1, i2, i3))

    with open(filepath, 'w') as f:
        f.write(f"# Identity Disc Vault CAD Model: {obj_name}\n")
        f.write(f"o {obj_name}\n")
        for v in vertices:
            f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
        f.write("s 1\n")
        for f_idx in faces:
            f.write(f"f {f_idx[0]} {f_idx[1]} {f_idx[2]}\n")

def main():
    # Model Specs:
    # Outer disc radius: 37.5 mm (OD 75mm)
    # Inner hole radius: 12.5 mm (ID 25mm)
    # Total thickness: 11.0 mm
    
    # 1. Base Housing (Bottom tray):
    # Outer radius 37.5mm, Wall 2.0mm, Floor 1.8mm, Lip height 8.0mm
    tray_floor = create_annular_cylinder_stl(12.5, 37.5, 1.8, z_offset=0.0)
    outer_wall = create_annular_cylinder_stl(35.5, 37.5, 6.2, z_offset=1.8)
    inner_wall = create_annular_cylinder_stl(12.5, 14.5, 6.2, z_offset=1.8)
    base_chassis = tray_floor + outer_wall + inner_wall
    
    write_binary_stl("hardware/cad/identity_disc_base.stl", base_chassis)
    write_obj("hardware/cad/identity_disc_base.obj", base_chassis, "BaseChassis")

    # 2. Top Bezel / Cover with touch window & LED light ring lip
    top_lid = create_annular_cylinder_stl(12.5, 37.5, 2.0, z_offset=8.0)
    bezel_rim = create_annular_cylinder_stl(33.5, 37.5, 1.5, z_offset=6.5)
    inner_bezel_rim = create_annular_cylinder_stl(12.5, 16.5, 1.5, z_offset=6.5)
    top_cover = top_lid + bezel_rim + inner_bezel_rim
    
    write_binary_stl("hardware/cad/identity_disc_top_cover.stl", top_cover)
    write_obj("hardware/cad/identity_disc_top_cover.obj", top_cover, "TopCover")

    # 3. Translucent Diffuser Ring (Sandwiched between base and top for Tron neon glow)
    # r_inner: 30.5mm, r_outer: 34.5mm, height: 4.0mm
    diffuser = create_diffuser_ring_stl(30.0, 35.0, 4.0, z_offset=3.0)
    write_binary_stl("hardware/cad/identity_disc_light_ring.stl", diffuser)
    write_obj("hardware/cad/identity_disc_light_ring.obj", diffuser, "NeonLightRingDiffuser")

    # 4. Full Complete Assembly (Base + Diffuser + Top)
    assembly = base_chassis + diffuser + top_cover
    write_binary_stl("hardware/cad/identity_disc_assembly.stl", assembly)
    write_obj("hardware/cad/identity_disc_assembly.obj", assembly, "CompleteIdentityDiscAssembly")

    print(f"Generated 3D CAD files:")
    print(f" - Base: {len(base_chassis)} tris")
    print(f" - Top Cover: {len(top_cover)} tris")
    print(f" - Neon Light Ring Diffuser: {len(diffuser)} tris")
    print(f" - Complete Assembly: {len(assembly)} tris")

if __name__ == '__main__':
    main()
