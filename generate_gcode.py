#!/usr/bin/env python3
"""
G-code Generator for CFRP Drone Parts
Machine : LUNYEE 3020 Nova CNC Router (GRBL controller)
Sender  : Universal Gcode Sender (UGS)
Material: CFRP (Carbon Fiber Reinforced Polymer)

WARNING: CFRP dust is hazardous (carcinogenic).
  - Use dust extraction at all times
  - Wear N95/P100 respirator mask
  - Consider wet cutting or vacuum enclosure
"""

import struct
import math
from collections import defaultdict

# ─────────────────────────────────────────
# CUTTING PARAMETERS  (adjust to your setup)
# ─────────────────────────────────────────
TOOL_DIAMETER = 3.0     # mm  – carbide 2-flute flat end mill
TOOL_RADIUS   = TOOL_DIAMETER / 2.0

SPINDLE_RPM = 15000     # RPM  – high RPM helps CFRP cut cleanly
FEED_XY     = 600       # mm/min – lateral feed (conservative for CFRP)
FEED_Z      = 120       # mm/min – plunge feed
STEP_DOWN   = 0.5       # mm  – depth per Z pass (shallow = cleaner CFRP cuts)
SAFE_Z      = 10.0      # mm  – rapid clearance height above workpiece


# ─────────────────────────────────────────
# STL READER
# ─────────────────────────────────────────

def read_stl(path):
    tris = []
    with open(path, 'rb') as f:
        f.read(80)
        n = struct.unpack('<I', f.read(4))[0]
        for _ in range(n):
            f.read(12)
            v0 = struct.unpack('<3f', f.read(12))
            v1 = struct.unpack('<3f', f.read(12))
            v2 = struct.unpack('<3f', f.read(12))
            f.read(2)
            tris.append((v0, v1, v2))
    return tris


def stl_bounds(tris):
    xs = [v[0] for t in tris for v in t]
    ys = [v[1] for t in tris for v in t]
    zs = [v[2] for t in tris for v in t]
    return min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)


# ─────────────────────────────────────────
# SLICER  – intersect STL with Z plane
# ─────────────────────────────────────────

def slice_at_z(tris, z, eps=1e-4):
    """Return list of 2D line segments at height z."""
    segs = []
    for v0, v1, v2 in tris:
        pts = []
        for a, b in [(v0, v1), (v1, v2), (v2, v0)]:
            za, zb = a[2], b[2]
            if abs(za - zb) < eps:
                continue
            t = (z - za) / (zb - za)
            if 0.0 <= t <= 1.0:
                x = a[0] + t * (b[0] - a[0])
                y = a[1] + t * (b[1] - a[1])
                pts.append((round(x, 3), round(y, 3)))
        if len(pts) == 2 and pts[0] != pts[1]:
            segs.append((pts[0], pts[1]))
    return segs


def chain_segments(segs):
    """Chain 2D segments into closed polygons."""
    adj = defaultdict(list)
    for i, (p1, p2) in enumerate(segs):
        adj[p1].append((i, p2))
        adj[p2].append((i, p1))

    used  = set()
    loops = []

    for i, (p1, _) in enumerate(segs):
        if i in used:
            continue
        used.add(i)
        loop = [p1, segs[i][1]]
        cur  = segs[i][1]

        while True:
            ch = [(j, q) for j, q in adj[cur] if j not in used]
            if not ch:
                break
            j, q = ch[0]
            used.add(j)
            if q == loop[0]:
                loop.append(q)
                loops.append(loop)
                break
            loop.append(q)
            cur = q

    return loops


def signed_area(pts):
    """Shoelace formula – positive = CCW, negative = CW."""
    n = len(pts)
    a = 0.0
    for i in range(n):
        j = (i + 1) % n
        a += pts[i][0] * pts[j][1] - pts[j][0] * pts[i][1]
    return a / 2.0


def centroid(pts):
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    return cx, cy


# ─────────────────────────────────────────
# POLYGON OFFSET  (miter join)
# ─────────────────────────────────────────

def offset_poly(pts, d):
    """
    Offset a CCW polygon by distance d.
      d > 0  →  expand outward  (outer profile)
      d < 0  →  shrink inward   (hole inner path)
    Uses miter joins, capped to 5× d to avoid extreme spikes.
    """
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    n = len(pts)
    result = []

    for i in range(n):
        a  = pts[(i - 1) % n]
        b  = pts[i]
        c  = pts[(i + 1) % n]

        e1 = (b[0] - a[0], b[1] - a[1])
        e2 = (c[0] - b[0], c[1] - b[1])
        l1 = math.hypot(*e1)
        l2 = math.hypot(*e2)

        if l1 < 1e-9 or l2 < 1e-9:
            result.append(b)
            continue

        # outward unit normals for CCW polygon (right-hand rule)
        n1 = ( e1[1] / l1, -e1[0] / l1)
        n2 = ( e2[1] / l2, -e2[0] / l2)

        bx, by = n1[0] + n2[0], n1[1] + n2[1]
        bl_sq  = bx * bx + by * by

        if bl_sq < 1e-9:
            result.append((b[0] + n1[0] * d, b[1] + n1[1] * d))
            continue

        # miter offset: 2d / |bisector|²  ×  bisector
        scale = 2.0 * d / bl_sq
        # cap extreme miters
        max_s = 5.0 * abs(d) / math.sqrt(bl_sq) if bl_sq > 0 else abs(d)
        if abs(scale) > max_s:
            scale = math.copysign(max_s, scale)

        result.append((b[0] + bx * scale, b[1] + by * scale))

    return result


# ─────────────────────────────────────────
# G-CODE HELPERS
# ─────────────────────────────────────────

def fmt(v):
    return f"{v:.4f}"


def gcode_header(part_name, thickness):
    return [
        f"; ════════════════════════════════════",
        f"; Part    : {part_name}",
        f"; Thickness: {thickness:.2f} mm",
        f"; Tool    : {TOOL_DIAMETER} mm carbide 2-flute end mill",
        f"; Spindle : {SPINDLE_RPM} RPM",
        f"; Feed XY : {FEED_XY} mm/min",
        f"; Feed Z  : {FEED_Z} mm/min",
        f"; Step-down: {STEP_DOWN} mm/pass",
        f"; Z=0 = top surface of material",
        f"; ════════════════════════════════════",
        f"; !! CFRP DUST WARNING !!",
        f"; Use dust extraction + N95 respirator",
        f"; ════════════════════════════════════",
        "",
        "G21       ; mm units",
        "G90       ; absolute positioning",
        "G17       ; XY plane",
        f"G0 Z{fmt(SAFE_Z)}  ; safe height",
        "G0 X0 Y0",
        f"M3 S{SPINDLE_RPM}  ; spindle on (CW)",
        "G4 P3     ; wait 3 s for spindle to spin up",
        "",
    ]


def gcode_footer():
    return [
        "",
        f"G0 Z{fmt(SAFE_Z)}  ; retract",
        "G0 X0 Y0  ; return to origin",
        "M5        ; spindle off",
        "M30       ; end of program",
    ]


def cut_profile(pts, z_passes, label):
    """Generate G-code to cut a closed polygon with multiple Z passes."""
    lines = [f"; {label}"]
    sx, sy = pts[0]
    lines.append(f"G0 Z{fmt(SAFE_Z)}")
    lines.append(f"G0 X{fmt(sx)} Y{fmt(sy)}")

    for z in z_passes:
        lines.append(f"G1 Z{fmt(z)} F{FEED_Z}")
        for px, py in pts[1:]:
            lines.append(f"G1 X{fmt(px)} Y{fmt(py)} F{FEED_XY}")
        lines.append(f"G1 X{fmt(pts[0][0])} Y{fmt(pts[0][1])} F{FEED_XY}")

    lines.append(f"G0 Z{fmt(SAFE_Z)}")
    lines.append("")
    return lines


# ─────────────────────────────────────────
# MAIN GENERATOR
# ─────────────────────────────────────────

def generate_gcode(part_name, stl_path, output_path):
    tris = read_stl(stl_path)
    x0, x1, y0, y1, z_bot, z_top = stl_bounds(tris)
    thickness = round(z_top - z_bot, 4)

    print(f"\n{'='*50}")
    print(f"{part_name}")
    print(f"  Size      : {x1-x0:.2f} x {y1-y0:.2f} mm")
    print(f"  Thickness : {thickness:.2f} mm")

    # Slice at mid-height to get clean 2D profile
    mid_z = (z_bot + z_top) / 2.0
    segs  = slice_at_z(tris, mid_z)
    loops = chain_segments(segs)
    print(f"  Loops found: {len(loops)}")

    # Classify loops by area
    classified = []
    for loop in loops:
        pts  = loop[:-1]
        area = signed_area(pts)
        classified.append((abs(area), area, pts))

    classified.sort(key=lambda x: x[0], reverse=True)

    # Largest = outer profile; rest = holes
    outer_profile = None
    holes         = []
    for i, (abs_a, signed_a, pts) in enumerate(classified):
        if i == 0:
            outer_profile = (abs_a, signed_a, pts)
        else:
            holes.append((abs_a, signed_a, pts))

    # Z passes: from -STEP_DOWN down through material, plus small overcut
    z_passes = []
    z = -STEP_DOWN
    while z > -(thickness + STEP_DOWN):
        z_passes.append(round(z, 4))
        z -= STEP_DOWN
    # Final overcut pass to ensure clean cut-through
    z_passes[-1] = round(-(thickness + 0.2), 4)

    print(f"  Z passes  : {len(z_passes)} × {STEP_DOWN} mm  → {z_passes}")

    lines = gcode_header(part_name, thickness)

    # ── Outer profile ──────────────────────────────
    abs_a, signed_a, pts = outer_profile
    print(f"  Outer area: {abs_a:.1f} mm²  (~{math.sqrt(abs_a/math.pi)*2:.1f} mm eff. dia)")

    # Ensure CCW (positive area) for outward offset
    if signed_a < 0:
        pts = pts[::-1]

    offset_pts = offset_poly(pts, TOOL_RADIUS)  # tool outside the part
    lines += cut_profile(offset_pts, z_passes, f"Outer profile (tool offset +{TOOL_RADIUS}mm)")

    # ── Holes ───────────────────────────────────────
    cuttable_holes  = []
    drill_holes     = []

    for abs_a, signed_a, pts in holes:
        # Estimate equivalent radius
        eq_r = math.sqrt(abs_a / math.pi)
        cx, cy = centroid(pts)

        if eq_r > TOOL_RADIUS + 0.3:  # hole larger than tool – can mill
            cuttable_holes.append((abs_a, signed_a, pts, eq_r, cx, cy))
        else:  # hole too small – must drill
            drill_holes.append((abs_a, eq_r, cx, cy))

    print(f"  Millable holes : {len(cuttable_holes)}")
    print(f"  Drill holes    : {len(drill_holes)}")

    for abs_a, signed_a, pts, eq_r, cx, cy in cuttable_holes:
        # Make CCW then shrink inward by tool radius
        if signed_a < 0:
            pts = pts[::-1]
        inner_pts = offset_poly(pts, -TOOL_RADIUS)
        lines += cut_profile(
            inner_pts, z_passes,
            f"Hole (r≈{eq_r:.2f}mm, center≈{cx:.2f},{cy:.2f})")

    if drill_holes:
        lines.append("; ── DRILL MANUALLY (holes too small for current tool) ──")
        for abs_a, eq_r, cx, cy in drill_holes:
            dia = eq_r * 2
            lines.append(f"; Hole d≈{dia:.2f}mm at X={cx:.3f} Y={cy:.3f}  → use {dia:.1f}mm drill bit")
        lines.append("; ──────────────────────────────────────────────────────")
        lines.append("")

    lines += gcode_footer()

    gcode_text = "\n".join(lines)
    with open(output_path, 'w') as f:
        f.write(gcode_text)

    line_count = len(lines)
    print(f"  Written   : {output_path}  ({line_count} lines)")
    return gcode_text


# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────

if __name__ == "__main__":
    import os
    base = os.path.dirname(os.path.abspath(__file__))

    generate_gcode(
        part_name  = "CENTER_PLATE",
        stl_path   = os.path.join(base, "CENTER_PLATE_fixed.stl"),
        output_path= os.path.join(base, "CENTER_PLATE.nc"),
    )

    generate_gcode(
        part_name  = "6INCH_ARM",
        stl_path   = os.path.join(base, "6INCH_ARM_fixed.stl"),
        output_path= os.path.join(base, "6INCH_ARM.nc"),
    )
