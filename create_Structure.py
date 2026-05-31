#!/usr/bin/env python3
"""
Parametric CFRP parts – exact translation of structure_example.py into cadquery.

create_plate()      → CENTER_PLATE_param.step / .nc
create_arm_motor()  → 6INCH_ARM_param.step   / .nc

Blender boolean logic faithfully replicated:
  - create_plate: base cylinder + 8 boss rings (4 large diagonal, 4 small axis-aligned)
  - create_arm_motor: motor-mount square + arm beam + boss rings + corner cuts
    (no 45° rotation – optimal orientation for CNC bed)
"""

import cadquery as cq
import math
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────────────────────────────────
# PARAMETERS  (identical to structure_example.py)
# ─────────────────────────────────────────────────────────
M3 = 3.2
M5 = 5.2
FC_PITCH    = 30.5 / 2          # 15.25 mm
MOTOR_PITCH = 19.0 / 2          # 9.5 mm

PROP_INCH      = 6 * 25.4       # 152.4 mm
ARM_length     = PROP_INCH / 2 * 1.47   # 112.4 mm
ARM_width      = 12.0
ARM_THICKNESS  = 6.0
PLATE_THICKNESS = 3.0

# ─────────────────────────────────────────────────────────
# CUTTING PARAMETERS
# ─────────────────────────────────────────────────────────
TOOL_D    = 3.0
TOOL_R    = TOOL_D / 2
SPINDLE   = 15000
FEED_XY   = 600
FEED_Z    = 120
STEP_DOWN = 0.5
SAFE_Z    = 10.0


# ─────────────────────────────────────────────────────────
# create_plate()  ←  structure_example.py 忠実再現
# ─────────────────────────────────────────────────────────
def create_plate() -> cq.Workplane:
    """
    Blender logic:
      1. base_cylinder(r=24.5)
      2. 4×add_ring(outer=M3*2, inner=M3/2) at FC_HOLES  ← body at 0°
      3. body.rotation = 45°
      4. 4×add_ring(outer=M3*1.25, inner=M3/2) at same FC_HOLES world pos
         → in body-local space these land at axis-aligned positions
      5. cut_cylinder(r=M5/2)  center hole

    Result in world space (body still at 45° on export):
      large bosses (r=6.4mm) at 0°/90°/180°/270°   r=21.567mm BCD
      small bosses (r=4.0mm) at 45°/135°/225°/315° r=21.567mm BCD
    """
    R_BASE  = 24.5
    R_LARGE = M3 * 2.0    # 6.4 mm
    R_SMALL = M3 * 1.25   # 4.0 mm
    BCD     = math.sqrt(2) * FC_PITCH   # 21.567 mm

    # FC_HOLES (±15.25, ±15.25) – diagonal positions
    FC_HOLES = [
        ( FC_PITCH,  FC_PITCH),
        ( FC_PITCH, -FC_PITCH),
        (-FC_PITCH,  FC_PITCH),
        (-FC_PITCH, -FC_PITCH),
    ]
    # After body rotated 45°, the same world positions map to axis-aligned local
    # → second set of rings ends up at 0°/90°/180°/270° in world
    AXIS_HOLES = [(BCD, 0), (-BCD, 0), (0, BCD), (0, -BCD)]

    plate = cq.Workplane("XY").circle(R_BASE).extrude(PLATE_THICKNESS)

    # Step 2: large bosses at diagonal (45°/135°/225°/315°)
    for x, y in FC_HOLES:
        plate = plate.union(
            cq.Workplane("XY").transformed(offset=(x, y, 0))
            .circle(R_LARGE).extrude(PLATE_THICKNESS)
        )

    # Step 4: small bosses at axis-aligned (0°/90°/180°/270°)
    for x, y in AXIS_HOLES:
        plate = plate.union(
            cq.Workplane("XY").transformed(offset=(x, y, 0))
            .circle(R_SMALL).extrude(PLATE_THICKNESS)
        )

    # M3 through-holes at all 8 boss centers
    for x, y in FC_HOLES + AXIS_HOLES:
        plate = plate.cut(
            cq.Workplane("XY").transformed(offset=(x, y, 0))
            .circle(M3 / 2).extrude(PLATE_THICKNESS)
        )

    # M5 center hole
    plate = plate.cut(
        cq.Workplane("XY").circle(M5 / 2).extrude(PLATE_THICKNESS)
    )

    return plate


# ─────────────────────────────────────────────────────────
# create_arm_motor()  ←  structure_example.py 忠実再現
# ─────────────────────────────────────────────────────────
def create_arm_motor() -> cq.Workplane:
    """
    Blender logic (rotation stripped for CNC – arm along Y axis):
      1. motor-mount square (MOTOR_PITCH*2.08 × MOTOR_PITCH*2.08)
      2. add arm beam (ARM_width × ARM_length) from mount to tip at +Y
      3. 4×add_ring(outer=M3*1.5, inner=M3/2) at (±MOTOR_PITCH, 0) and (0, ±MOTOR_PITCH)
      4. cut M5 at arm tip (0, ARM_length)
      5. cut M3 body-attach hole at (FC_PITCH, -FC_PITCH)
      6. corner relief cuts

    Origin: motor-mount center at (0,0).  Arm tip at (0, ARM_length).
    """
    MOUNT_W = MOTOR_PITCH * 2.08   # 19.76 mm

    # Motor mount base
    arm = cq.Workplane("XY").rect(MOUNT_W, MOUNT_W).extrude(ARM_THICKNESS)

    # Arm beam extending from mount center toward +Y
    arm = arm.union(
        cq.Workplane("XY")
        .transformed(offset=(0, ARM_length / 2, 0))
        .rect(ARM_width, ARM_length)
        .extrude(ARM_THICKNESS)
    )

    # 4 motor boss rings — holes at 45° (× pattern), 19 mm pitch
    D = MOTOR_PITCH / math.sqrt(2)   # 9.5 / √2 ≈ 6.718 mm
    motor_hole_pos = [
        ( D,  D),
        (-D,  D),
        (-D, -D),
        ( D, -D),
    ]
    R_BOSS = M3 * 1.5   # 4.8 mm boss radius
    for x, y in motor_hole_pos:
        arm = arm.union(
            cq.Workplane("XY").transformed(offset=(x, y, 0))
            .circle(R_BOSS).extrude(ARM_THICKNESS)
        )
        arm = arm.cut(
            cq.Workplane("XY").transformed(offset=(x, y, 0))
            .circle(M3 / 2).extrude(ARM_THICKNESS)
        )

    # M5 hole at arm tip (body/center-plate attachment end)
    arm = arm.cut(
        cq.Workplane("XY").transformed(offset=(0, ARM_length, 0))
        .circle(M5 / 2).extrude(ARM_THICKNESS)
    )

    # 45° corner cuts at body-attachment end (y = ARM_length)
    # Prevents arm-to-arm overlap at center when 4 arms are assembled
    CUT = ARM_width / 2   # 6 mm
    for sx in [1, -1]:
        tip_cut = (
            cq.Workplane("XY")
            .polyline([
                (sx * ARM_width/2,              ARM_length - CUT),
                (sx * ARM_width/2,              ARM_length),
                (sx * ARM_width/2 - sx * CUT,   ARM_length),
            ])
            .close()
            .extrude(ARM_THICKNESS)
        )
        arm = arm.cut(tip_cut)

    return arm


# ─────────────────────────────────────────────────────────
# G-CODE GENERATOR  (true arcs from cadquery BREP edges)
# ─────────────────────────────────────────────────────────

def fmt(v: float) -> str:
    return f"{v:.4f}"


def extract_loops(shape: cq.Workplane):
    """
    Extract edge loops from top face as G-code primitives.
    Chains wire edges into connected order (wire.Edges() has arbitrary order).
    Returns list of loops; each loop is a list of:
      ("LINE", (x1,y1), (x2,y2))
      ("G2"|"G3", (x1,y1), (x2,y2), cx, cy, r)
    """
    wires = shape.faces(">Z").wires().vals()
    loops = []

    for wire in wires:
        edges = wire.Edges()
        if not edges:
            continue

        # ── chain edges in connected order ───────────────────────────────
        def get_pts(e):
            sp = e.startPoint();  ep_ = e.endPoint()
            return (round(sp.x, 4), round(sp.y, 4)), (round(ep_.x, 4), round(ep_.y, 4))

        def close(a, b, eps=0.005):
            return abs(a[0] - b[0]) < eps and abs(a[1] - b[1]) < eps

        ordered = [(edges[0], False)]   # (edge, needs_reverse)
        remaining = list(edges[1:])

        while remaining:
            last_edge, last_rev = ordered[-1]
            s_pt, e_pt = get_pts(last_edge)
            cur_end = e_pt if not last_rev else s_pt

            found = False
            for i, ed in enumerate(remaining):
                es, ee = get_pts(ed)
                if close(es, cur_end):
                    ordered.append((ed, False)); remaining.pop(i); found = True; break
                elif close(ee, cur_end):
                    ordered.append((ed, True));  remaining.pop(i); found = True; break
            if not found:
                break   # disconnected wire (shouldn't happen in valid BREP)

        # ── convert each (edge, reversed) to G-code primitive ────────────
        segs = []
        for edge, rev in ordered:
            gt = edge.geomType()
            s_pt, e_pt = get_pts(edge)
            if rev:
                s_pt, e_pt = e_pt, s_pt
            x1, y1 = s_pt
            x2, y2 = e_pt

            if gt == "LINE":
                segs.append(("LINE", (x1, y1), (x2, y2)))

            elif gt in ("CIRCLE", "ARC"):
                ac = edge.arcCenter()
                r  = round(edge.radius(), 4)
                cx = round(ac.x, 4)
                cy = round(ac.y, 4)
                # Arc direction from cross product at actual start point.
                # Works correctly for both forward and reversed traversal.
                mid = edge.positionAt(0.5)
                sx_, sy_ = x1 - cx, y1 - cy
                mx, my   = round(mid.x, 4) - cx, round(mid.y, 4) - cy
                cross    = sx_ * my - sy_ * mx
                cmd      = "G3" if cross > 0 else "G2"
                segs.append((cmd, (x1, y1), (x2, y2), cx, cy, r))

            else:
                # Spline / other: sample into short lines
                pts = [edge.positionAt(t / 20) for t in range(21)]
                if rev:
                    pts = pts[::-1]
                prev = (round(pts[0].x, 4), round(pts[0].y, 4))
                for pt in pts[1:]:
                    nxt = (round(pt.x, 4), round(pt.y, 4))
                    segs.append(("LINE", prev, nxt))
                    prev = nxt

        if segs:
            loops.append(segs)

    return loops


def loop_signed_area(segs):
    """Signed area. Handles full-circle (1 arc, start==end) correctly."""
    if len(segs) == 1 and segs[0][0] in ("G2", "G3"):
        cmd, (x1, y1), (x2, y2), cx, cy, r = segs[0]
        if abs(x1 - x2) < 0.01 and abs(y1 - y2) < 0.01:
            area = math.pi * r * r
            return -area if cmd == "G2" else area
    pts = [s[1] for s in segs]
    n, a = len(pts), 0.0
    for i in range(n):
        j = (i + 1) % n
        a += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return a / 2.0


def generate_gcode(part_name: str, shape: cq.Workplane,
                   thickness: float, output_path: str):
    lines = [
        f"; ═══════════════════════════════════════════",
        f"; Part      : {part_name}",
        f"; Thickness : {thickness:.1f} mm (CFRP)",
        f"; Tool      : {TOOL_D} mm carbide 2-flute end mill",
        f"; Spindle   : {SPINDLE} RPM | Feed XY: {FEED_XY} mm/min | Z: {FEED_Z} mm/min",
        f"; Step-down : {STEP_DOWN} mm/pass  ← true arc G2/G3 code",
        f"; Z=0 = top surface of material",
        f"; !! CFRP DUST HAZARD – dust extraction + N95 respirator required !!",
        f"; ═══════════════════════════════════════════",
        "",
        "G21  ; mm units",
        "G90  ; absolute coordinates",
        "G17  ; XY plane",
        f"G0 Z{fmt(SAFE_Z)}",
        "G0 X0 Y0",
        f"M3 S{SPINDLE}  ; spindle on",
        "G4 P3          ; wait 3 s",
        "",
    ]

    loops = extract_loops(shape)

    # Z pass depths
    z_passes = []
    z = -STEP_DOWN
    while z > -(thickness + STEP_DOWN):
        z_passes.append(round(z, 4))
        z -= STEP_DOWN
    z_passes[-1] = round(-(thickness + 0.2), 4)

    # Sort loops: largest abs area first = outer profile
    loops.sort(key=lambda s: abs(loop_signed_area(s)), reverse=True)

    drill_notes = []

    for li, segs in enumerate(loops):
        abs_a = abs(loop_signed_area(segs))
        is_outer = (li == 0)

        # Holes smaller than tool: flag for manual drilling
        if not is_outer and abs_a < math.pi * (TOOL_R + 0.2) ** 2:
            eq_r  = math.sqrt(abs_a / math.pi)
            # Full-circle holes are single G2/G3 arcs; use arc center, not start point
            if len(segs) == 1 and segs[0][0] in ("G2", "G3"):
                _, (hx1, hy1), (hx2, hy2), cx, cy, _ = segs[0]
            else:
                cx, cy = segs[0][1]
            drill_notes.append(
                f"; DRILL MANUALLY  d≈{eq_r*2:.2f}mm  "
                f"X≈{cx:.3f} Y≈{cy:.3f}  → use {eq_r*2:.1f}mm drill"
            )
            continue

        label = "outer profile" if is_outer else f"hole ({abs_a:.0f} mm²)"
        sx, sy = segs[0][1]

        lines.append(f"; {label}")
        lines.append(f"G0 Z{fmt(SAFE_Z)}")
        lines.append(f"G0 X{fmt(sx)} Y{fmt(sy)}")

        for z_cut in z_passes:
            lines.append(f"G1 Z{fmt(z_cut)} F{FEED_Z}")
            for seg in segs:
                if seg[0] == "LINE":
                    _, _, (x2, y2) = seg
                    lines.append(f"G1 X{fmt(x2)} Y{fmt(y2)} F{FEED_XY}")
                else:
                    cmd, (x1, y1), (x2, y2), acx, acy, r = seg
                    i_val = round(acx - x1, 4)
                    j_val = round(acy - y1, 4)
                    lines.append(
                        f"{cmd} X{fmt(x2)} Y{fmt(y2)} I{fmt(i_val)} J{fmt(j_val)} F{FEED_XY}"
                    )
            lines.append(f"G1 X{fmt(sx)} Y{fmt(sy)} F{FEED_XY}")

        lines.append(f"G0 Z{fmt(SAFE_Z)}")
        lines.append("")

    if drill_notes:
        lines.append("; ── DRILL MANUALLY ─────────────────────────────")
        lines += drill_notes
        lines.append("; ────────────────────────────────────────────────")
        lines.append("")

    lines += [
        f"G0 Z{fmt(SAFE_Z)}",
        "G0 X0 Y0",
        "M5   ; spindle off",
        "M30  ; end of program",
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    arc_count  = sum(1 for l in lines if l.startswith(("G2 ", "G3 ")))
    g1_count   = sum(1 for l in lines if l.startswith("G1 "))
    print(f"  → {output_path}")
    print(f"     lines: {len(lines)}   G1: {g1_count}   arcs(G2/G3): {arc_count}")


# ─────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────

print("Building CENTER_PLATE (create_plate) …")
plate = create_plate()
plate.val().exportStep(os.path.join(BASE, "CENTER_PLATE_param.step"))
print("  STEP: CENTER_PLATE_param.step")
generate_gcode("CENTER_PLATE", plate, PLATE_THICKNESS,
               os.path.join(BASE, "CENTER_PLATE_param.nc"))

print()
print("Building 6INCH_ARM (create_arm_motor) …")
arm = create_arm_motor()
arm.val().exportStep(os.path.join(BASE, "6INCH_ARM_param.step"))
print("  STEP: 6INCH_ARM_param.step")
generate_gcode("6INCH_ARM", arm, ARM_THICKNESS,
               os.path.join(BASE, "6INCH_ARM_param.nc"))

print("\nComplete.")
