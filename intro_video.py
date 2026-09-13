import cv2
import numpy as np
import random
import math


# =========================================================
# CẤU HÌNH VIDEO
# =========================================================

WIDTH = 1920
HEIGHT = 1080

FPS = 30
DURATION = 8

OUTPUT_FILE = "intro_video.mp4"


# =========================================================
# CẤU HÌNH CỤM CHÍNH
# =========================================================

NUM_POINTS = 72

POINTS_PER_CLUSTER = 3
NUM_CLUSTERS = NUM_POINTS // POINTS_PER_CLUSTER

POINT_RADIUS = 7
OUTER_POINT_RADIUS = 5

LINE_WIDTH = 2


# =========================================================
# PHÂN BỐ CỤM CHÍNH
# =========================================================

CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

DISTRIBUTION_X = 620
DISTRIBUTION_Y = 340

MIN_CLUSTER_DISTANCE = 125

MAX_ATTEMPTS = 50000


# =========================================================
# KẾT NỐI CỤM CHÍNH
# =========================================================

MAX_CONNECTION_DISTANCE = 430

MIN_EXTRA_CONNECTIONS = 0
MAX_EXTRA_CONNECTIONS = 1

EXTRA_CONNECTION_PROBABILITY = 0.35


# =========================================================
# TAM GIÁC NGOÀI
# =========================================================

MIN_OUTER_TRIANGLES = 10
MAX_OUTER_TRIANGLES = 12


# =========================================================
# VÙNG PHÂN BỐ TAM GIÁC NGOÀI
# =========================================================

OUTER_MIN_RADIUS_X = 650
OUTER_MIN_RADIUS_Y = 350

OUTER_MAX_RADIUS_X = 900
OUTER_MAX_RADIUS_Y = 480


# =========================================================
# KHOẢNG CÁCH
# =========================================================

MIN_OUTER_DISTANCE = 110


# =========================================================
# KÍCH THƯỚC TAM GIÁC NGOÀI
# =========================================================

OUTER_TRIANGLE_MIN_RADIUS = 32
OUTER_TRIANGLE_MAX_RADIUS = 58


# =========================================================
# TỶ LỆ KÉO DÀI
# =========================================================

OUTER_SCALE_MIN_X = 1.05
OUTER_SCALE_MAX_X = 1.35

OUTER_SCALE_MIN_Y = 0.90
OUTER_SCALE_MAX_Y = 1.10


# =========================================================
# FILL
# =========================================================

OUTER_FILL_PROBABILITY = 0.40


# =========================================================
# CHUYỂN ĐỘNG TAM GIÁC NGOÀI
# =========================================================

OUTER_MIN_SPEED = 0.25
OUTER_MAX_SPEED = 0.75

OUTER_WAVE_MIN = 0.015
OUTER_WAVE_MAX = 0.045

OUTER_ROTATION_MIN = -0.006
OUTER_ROTATION_MAX = 0.006

OUTER_SWAY_MIN = 3.0
OUTER_SWAY_MAX = 9.0


# =========================================================
# CHUYỂN ĐỘNG RIÊNG CỦA 3 ĐIỂM
# =========================================================

OUTER_POINT_MIN_SPEED = 0.45
OUTER_POINT_MAX_SPEED = 1.5

OUTER_POINT_MAX_RADIUS_MIN = 35
OUTER_POINT_MAX_RADIUS_MAX = 65

OUTER_POINT_WANDER_FORCE = 0.018
OUTER_POINT_RETURN_FORCE = 0.20


# =========================================================
# MÀU
# =========================================================

COLOR = (
    255,
    140,
    0
)

CONNECTION_COLOR = COLOR

BG_COLOR = (
    255,
    255,
    255
)


# =========================================================
# MÀU FILL
# =========================================================

FILL_COLOR = (
    255,
    220,
    170
)

FILL_ALPHA = 0.58


# =========================================================
# FILL CỤM CHÍNH
# =========================================================

MIN_FILLED_CLUSTERS = 15
MAX_FILLED_CLUSTERS = 18


# =========================================================
# CHUYỂN ĐỘNG CỤM CHÍNH
# =========================================================

MIN_SPEED = 0.45
MAX_SPEED = 2.0

CLUSTER_MAX_RADIUS_MIN = 38
CLUSTER_MAX_RADIUS_MAX = 62


# =========================================================
# TẠO TÂM CỤM CHÍNH
# =========================================================

def create_cluster_centers():

    centers = []

    attempts = 0

    margin = 110

    while (
        len(centers) < NUM_CLUSTERS
        and attempts < MAX_ATTEMPTS
    ):

        attempts += 1

        x = random.gauss(
            CENTER_X,
            DISTRIBUTION_X / 2.4
        )

        y = random.gauss(
            CENTER_Y,
            DISTRIBUTION_Y / 2.4
        )

        if x < margin:
            continue

        if x > WIDTH - margin:
            continue

        if y < margin:
            continue

        if y > HEIGHT - margin:
            continue

        valid = True

        for cx, cy in centers:

            distance = math.hypot(
                x - cx,
                y - cy
            )

            if distance < MIN_CLUSTER_DISTANCE:

                valid = False
                break

        if valid:

            centers.append(
                (
                    x,
                    y
                )
            )

    # =====================================================
    # FALLBACK
    # =====================================================

    if len(centers) < NUM_CLUSTERS:

        attempts = 0

        while (
            len(centers) < NUM_CLUSTERS
            and attempts < MAX_ATTEMPTS
        ):

            attempts += 1

            x = random.uniform(
                150,
                WIDTH - 150
            )

            y = random.uniform(
                120,
                HEIGHT - 120
            )

            valid = True

            for cx, cy in centers:

                distance = math.hypot(
                    x - cx,
                    y - cy
                )

                if distance < 105:

                    valid = False
                    break

            if valid:

                centers.append(
                    (
                        x,
                        y
                    )
                )

    if len(centers) != NUM_CLUSTERS:

        raise RuntimeError(
            "Không thể tạo đủ cụm chính."
        )

    return centers


# =========================================================
# TẠO CỤM CHÍNH
# =========================================================

def create_clusters():

    clusters = []

    centers = create_cluster_centers()

    number_filled = random.randint(
        MIN_FILLED_CLUSTERS,
        MAX_FILLED_CLUSTERS
    )

    filled_ids = set(
        random.sample(
            range(NUM_CLUSTERS),
            number_filled
        )
    )

    for cluster_id in range(NUM_CLUSTERS):

        center_x = centers[cluster_id][0]
        center_y = centers[cluster_id][1]

        points = []

        base_rotation = random.uniform(
            0,
            math.pi * 2
        )

        for i in range(POINTS_PER_CLUSTER):

            angle = (
                base_rotation
                + i * 2 * math.pi / 3
            )

            angle += random.uniform(
                -0.20,
                0.20
            )

            radius = random.uniform(
                24,
                42
            )

            x = (
                center_x
                + math.cos(angle)
                * radius
            )

            y = (
                center_y
                + math.sin(angle)
                * radius
            )

            # -------------------------------------------------
            # VẬN TỐC
            # -------------------------------------------------

            speed = random.uniform(
                MIN_SPEED,
                MAX_SPEED
            )

            direction = random.uniform(
                0,
                math.pi * 2
            )

            vx = (
                math.cos(direction)
                * speed
            )

            vy = (
                math.sin(direction)
                * speed
            )

            # -------------------------------------------------
            # DAO ĐỘNG
            # -------------------------------------------------

            phase = random.uniform(
                0,
                math.pi * 2
            )

            phase_speed = random.uniform(
                0.008,
                0.018
            )

            points.append({

                "x": x,
                "y": y,

                "center_x": center_x,
                "center_y": center_y,

                "vx": vx,
                "vy": vy,

                "phase": phase,
                "phase_speed": phase_speed,

                "max_radius": random.uniform(
                    CLUSTER_MAX_RADIUS_MIN,
                    CLUSTER_MAX_RADIUS_MAX
                )
            })

        clusters.append({

            "points": points,

            "center_x": center_x,
            "center_y": center_y,

            "filled": (
                cluster_id in filled_ids
            )
        })

    return clusters


# =========================================================
# KHOẢNG CÁCH 2 CỤM
# =========================================================

def cluster_distance(
    clusters,
    a,
    b
):

    dx = (
        clusters[a]["center_x"]
        - clusters[b]["center_x"]
    )

    dy = (
        clusters[a]["center_y"]
        - clusters[b]["center_y"]
    )

    return math.hypot(
        dx,
        dy
    )


# =========================================================
# KIỂM TRA CONNECTION
# =========================================================

def connection_exists(
    connections,
    a,
    b
):

    for connection in connections:

        ca = connection["cluster_a"]
        cb = connection["cluster_b"]

        if (
            ca == a and cb == b
        ) or (
            ca == b and cb == a
        ):

            return True

    return False


# =========================================================
# THÊM CONNECTION
# =========================================================

def add_connection(
    connections,
    cluster_a,
    cluster_b
):

    if cluster_a == cluster_b:
        return

    if connection_exists(
        connections,
        cluster_a,
        cluster_b
    ):
        return

    number_of_points = random.choice(
        [
            1,
            2
        ]
    )

    points_a = random.sample(
        range(POINTS_PER_CLUSTER),
        number_of_points
    )

    points_b = random.sample(
        range(POINTS_PER_CLUSTER),
        number_of_points
    )

    for i in range(number_of_points):

        connections.append({

            "cluster_a": cluster_a,
            "point_a": points_a[i],

            "cluster_b": cluster_b,
            "point_b": points_b[i]
        })


# =========================================================
# TẠO MẠNG CHÍNH LIÊN THÔNG
# =========================================================

def create_connections(clusters):

    connections = []

    connected = {0}

    remaining = set(
        range(
            1,
            NUM_CLUSTERS
        )
    )

    while remaining:

        best_pair = None
        best_distance = float("inf")

        for a in connected:

            for b in remaining:

                distance = cluster_distance(
                    clusters,
                    a,
                    b
                )

                if distance < best_distance:

                    best_distance = distance

                    best_pair = (
                        a,
                        b
                    )

        if best_pair is None:
            break

        a, b = best_pair

        add_connection(
            connections,
            a,
            b
        )

        connected.add(b)
        remaining.remove(b)

    if len(connected) != NUM_CLUSTERS:

        raise RuntimeError(
            "Mạng chính không liên thông."
        )

    # =====================================================
    # CONNECTION PHỤ
    # =====================================================

    for cluster_a in range(NUM_CLUSTERS):

        if (
            random.random()
            > EXTRA_CONNECTION_PROBABILITY
        ):
            continue

        candidates = []

        for cluster_b in range(NUM_CLUSTERS):

            if cluster_a == cluster_b:
                continue

            if connection_exists(
                connections,
                cluster_a,
                cluster_b
            ):
                continue

            distance = cluster_distance(
                clusters,
                cluster_a,
                cluster_b
            )

            if distance <= MAX_CONNECTION_DISTANCE:

                candidates.append(
                    (
                        cluster_b,
                        distance
                    )
                )

        if not candidates:
            continue

        random.shuffle(candidates)

        candidates.sort(
            key=lambda item:
                item[1]
                * random.uniform(
                    0.85,
                    1.15
                )
        )

        number_extra = random.randint(
            MIN_EXTRA_CONNECTIONS,
            MAX_EXTRA_CONNECTIONS
        )

        for cluster_b, distance in candidates[
            :number_extra
        ]:

            add_connection(
                connections,
                cluster_a,
                cluster_b
            )

    return connections


# =========================================================
# XOAY ĐIỂM
# =========================================================

def rotate_point(
    x,
    y,
    angle
):

    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    return (
        x * cos_a - y * sin_a,
        x * sin_a + y * cos_a
    )


# =========================================================
# TẠO TAM GIÁC NGOÀI
#
# QUAN TRỌNG:
#
# Mỗi triangle CHỈ có đúng 3 points.
#
# Mỗi point đều có:
#
# x
# y
# local_x
# local_y
# vx
# vy
# phase
# phase_speed
# max_radius
#
# =========================================================

def create_outer_triangles(clusters):

    outer_triangles = []

    target_count = random.randint(
        MIN_OUTER_TRIANGLES,
        MAX_OUTER_TRIANGLES
    )

    attempts = 0
    max_attempts = 50000

    while (
        len(outer_triangles) < target_count
        and attempts < max_attempts
    ):

        attempts += 1

        # =================================================
        # VỊ TRÍ TÂM
        # =================================================

        angle = random.uniform(
            0,
            math.pi * 2
        )

        radius_x = random.uniform(
            OUTER_MIN_RADIUS_X,
            OUTER_MAX_RADIUS_X
        )

        radius_y = random.uniform(
            OUTER_MIN_RADIUS_Y,
            OUTER_MAX_RADIUS_Y
        )

        center_x = (
            CENTER_X
            + math.cos(angle)
            * radius_x
        )

        center_y = (
            CENTER_Y
            + math.sin(angle)
            * radius_y
        )

        # =================================================
        # MARGIN
        # =================================================

        margin = 90

        if center_x < margin:
            continue

        if center_x > WIDTH - margin:
            continue

        if center_y < margin:
            continue

        if center_y > HEIGHT - margin:
            continue

        # =================================================
        # KHÔNG QUÁ GẦN CỤM CHÍNH
        # =================================================

        too_close_to_main = False

        for cluster in clusters:

            distance = math.hypot(
                center_x - cluster["center_x"],
                center_y - cluster["center_y"]
            )

            if distance < 130:

                too_close_to_main = True
                break

        if too_close_to_main:
            continue

        # =================================================
        # KHÔNG QUÁ GẦN TAM GIÁC NGOÀI KHÁC
        # =================================================

        too_close_to_outer = False

        for outer in outer_triangles:

            distance = math.hypot(
                center_x - outer["center_x"],
                center_y - outer["center_y"]
            )

            if distance < MIN_OUTER_DISTANCE:

                too_close_to_outer = True
                break

        if too_close_to_outer:
            continue

        # =================================================
        # KÍCH THƯỚC
        # =================================================

        radius = random.uniform(
            OUTER_TRIANGLE_MIN_RADIUS,
            OUTER_TRIANGLE_MAX_RADIUS
        )

        scale_x = random.uniform(
            OUTER_SCALE_MIN_X,
            OUTER_SCALE_MAX_X
        )

        scale_y = random.uniform(
            OUTER_SCALE_MIN_Y,
            OUTER_SCALE_MAX_Y
        )

        rotation = random.uniform(
            0,
            math.pi * 2
        )

        # =================================================
        # TẠO ĐÚNG 3 ĐIỂM
        # =================================================

        points = []

        for i in range(3):

            base_angle = (
                i
                * 2
                * math.pi
                / 3
            )

            angle_offset = random.uniform(
                -0.10,
                0.10
            )

            local_angle = (
                base_angle
                + angle_offset
            )

            point_radius = random.uniform(
                0.92,
                1.08
            )

            local_x = (
                math.cos(local_angle)
                * radius
                * point_radius
                * scale_x
            )

            local_y = (
                math.sin(local_angle)
                * radius
                * point_radius
                * scale_y
            )

            rotated_x, rotated_y = rotate_point(
                local_x,
                local_y,
                rotation
            )

            px = center_x + rotated_x
            py = center_y + rotated_y

            # =================================================
            # VẬN TỐC RIÊNG CHO POINT
            # =================================================

            point_speed = random.uniform(
                OUTER_POINT_MIN_SPEED,
                OUTER_POINT_MAX_SPEED
            )

            point_direction = random.uniform(
                0,
                math.pi * 2
            )

            point_vx = (
                math.cos(point_direction)
                * point_speed
            )

            point_vy = (
                math.sin(point_direction)
                * point_speed
            )

            # =================================================
            # DAO ĐỘNG RIÊNG
            # =================================================

            point_phase = random.uniform(
                0,
                math.pi * 2
            )

            point_phase_speed = random.uniform(
                0.008,
                0.018
            )

            # =================================================
            # BÁN KÍNH TỐI ĐA
            # =================================================

            point_max_radius = random.uniform(
                OUTER_POINT_MAX_RADIUS_MIN,
                OUTER_POINT_MAX_RADIUS_MAX
            )

            # =================================================
            # LƯU POINT
            #
            # TẤT CẢ 3 POINT ĐỀU CÓ vx/vy
            # =================================================

            points.append({

                "x": px,
                "y": py,

                "local_x": local_x,
                "local_y": local_y,

                "vx": point_vx,
                "vy": point_vy,

                "phase": point_phase,
                "phase_speed": point_phase_speed,

                "max_radius": point_max_radius
            })

        # =================================================
        # VẬN TỐC TÂM TAM GIÁC
        # =================================================

        direction = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            OUTER_MIN_SPEED,
            OUTER_MAX_SPEED
        )

        vx = (
            math.cos(direction)
            * speed
        )

        vy = (
            math.sin(direction)
            * speed
        )

        # =================================================
        # DAO ĐỘNG TÂM
        # =================================================

        phase = random.uniform(
            0,
            math.pi * 2
        )

        phase_speed = random.uniform(
            OUTER_WAVE_MIN,
            OUTER_WAVE_MAX
        )

        sway_amount = random.uniform(
            OUTER_SWAY_MIN,
            OUTER_SWAY_MAX
        )

        sway_direction = random.uniform(
            0,
            math.pi * 2
        )

        # =================================================
        # XOAY
        # =================================================

        rotation_speed = random.uniform(
            OUTER_ROTATION_MIN,
            OUTER_ROTATION_MAX
        )

        # =================================================
        # FILL
        # =================================================

        filled = (
            random.random()
            < OUTER_FILL_PROBABILITY
        )

        # =================================================
        # LƯU TAM GIÁC
        # =================================================

        outer_triangles.append({

            "center_x": center_x,
            "center_y": center_y,

            "vx": vx,
            "vy": vy,

            "radius": radius,

            "scale_x": scale_x,
            "scale_y": scale_y,

            "rotation": rotation,
            "rotation_speed": rotation_speed,

            "phase": phase,
            "phase_speed": phase_speed,

            "sway_amount": sway_amount,
            "sway_direction": sway_direction,

            "points": points,

            "filled": filled
        })

    # =====================================================
    # KIỂM TRA
    # =====================================================

    if len(outer_triangles) < MIN_OUTER_TRIANGLES:

        raise RuntimeError(
            "Không thể tạo đủ tam giác ngoài."
        )

    # =====================================================
    # KIỂM TRA MỖI TAM GIÁC PHẢI CÓ ĐÚNG 3 POINT
    # =====================================================

    for index, triangle in enumerate(
        outer_triangles
    ):

        if len(triangle["points"]) != 3:

            raise RuntimeError(
                f"Tam giác ngoài #{index} "
                f"không có đúng 3 điểm."
            )

        for point_index, point in enumerate(
            triangle["points"]
        ):

            required_keys = (
                "x",
                "y",
                "local_x",
                "local_y",
                "vx",
                "vy",
                "phase",
                "phase_speed",
                "max_radius"
            )

            for key in required_keys:

                if key not in point:

                    raise RuntimeError(
                        f"Tam giác #{index}, "
                        f"point #{point_index} "
                        f"thiếu key '{key}'."
                    )

    return outer_triangles


# =========================================================
# UPDATE CỤM CHÍNH
# =========================================================

def update_cluster(
    cluster,
    frame_number
):

    for p in cluster["points"]:

        # =================================================
        # DI CHUYỂN
        # =================================================

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        # =================================================
        # DAO ĐỘNG
        # =================================================

        p["phase"] += (
            p["phase_speed"]
        )

        p["vx"] += (
            math.sin(
                p["phase"]
            )
            * 0.018
        )

        p["vy"] += (
            math.cos(
                p["phase"]
            )
            * 0.018
        )

        # =================================================
        # GIỚI HẠN TỐC ĐỘ
        # =================================================

        speed = math.hypot(
            p["vx"],
            p["vy"]
        )

        if speed > MAX_SPEED:

            p["vx"] = (
                p["vx"]
                / speed
                * MAX_SPEED
            )

            p["vy"] = (
                p["vy"]
                / speed
                * MAX_SPEED
            )

        elif speed < MIN_SPEED:

            if speed == 0:

                direction = random.uniform(
                    0,
                    math.pi * 2
                )

                p["vx"] = math.cos(
                    direction
                )

                p["vy"] = math.sin(
                    direction
                )

            else:

                p["vx"] = (
                    p["vx"]
                    / speed
                    * MIN_SPEED
                )

                p["vy"] = (
                    p["vy"]
                    / speed
                    * MIN_SPEED
                )

        # =================================================
        # KÉO VỀ TÂM
        # =================================================

        dx = (
            p["x"]
            - p["center_x"]
        )

        dy = (
            p["y"]
            - p["center_y"]
        )

        distance = math.hypot(
            dx,
            dy
        )

        if distance > p["max_radius"]:

            if distance > 0:

                nx = dx / distance
                ny = dy / distance

                force = 0.20

                p["vx"] -= (
                    nx * force
                )

                p["vy"] -= (
                    ny * force
                )


# =========================================================
# UPDATE TAM GIÁC NGOÀI
# =========================================================

def update_outer_triangle(
    triangle
):

    # =====================================================
    # PHASE
    # =====================================================

    triangle["phase"] += (
        triangle["phase_speed"]
    )

    # =====================================================
    # DI CHUYỂN TÂM
    # =====================================================

    triangle["center_x"] += (
        triangle["vx"]
    )

    triangle["center_y"] += (
        triangle["vy"]
    )

    # =====================================================
    # DAO ĐỘNG TÂM
    # =====================================================

    sway = (
        math.sin(
            triangle["phase"]
        )
        * triangle["sway_amount"]
    )

    sway_x = (
        math.cos(
            triangle["sway_direction"]
        )
        * sway
    )

    sway_y = (
        math.sin(
            triangle["sway_direction"]
        )
        * sway
    )

    triangle["center_x"] += (
        sway_x * 0.12
    )

    triangle["center_y"] += (
        sway_y * 0.12
    )

    # =====================================================
    # XOAY
    # =====================================================

    triangle["rotation"] += (
        triangle["rotation_speed"]
    )

    # =====================================================
    # GIỚI HẠN TÂM
    # =====================================================

    margin = 110

    if triangle["center_x"] < margin:

        triangle["center_x"] = margin

        triangle["vx"] = abs(
            triangle["vx"]
        )

    elif triangle["center_x"] > WIDTH - margin:

        triangle["center_x"] = (
            WIDTH - margin
        )

        triangle["vx"] = -abs(
            triangle["vx"]
        )

    if triangle["center_y"] < margin:

        triangle["center_y"] = margin

        triangle["vy"] = abs(
            triangle["vy"]
        )

    elif triangle["center_y"] > HEIGHT - margin:

        triangle["center_y"] = (
            HEIGHT - margin
        )

        triangle["vy"] = -abs(
            triangle["vy"]
        )

    # =====================================================
    # UPDATE 3 POINT RIÊNG
    # =====================================================

    for p in triangle["points"]:

        # =================================================
        # DI CHUYỂN
        # =================================================

        p["x"] += p["vx"]
        p["y"] += p["vy"]

        # =================================================
        # DAO ĐỘNG
        # =================================================

        p["phase"] += (
            p["phase_speed"]
        )

        p["vx"] += (
            math.sin(
                p["phase"]
            )
            * OUTER_POINT_WANDER_FORCE
        )

        p["vy"] += (
            math.cos(
                p["phase"]
            )
            * OUTER_POINT_WANDER_FORCE
        )

        # =================================================
        # GIỚI HẠN TỐC ĐỘ
        # =================================================

        speed = math.hypot(
            p["vx"],
            p["vy"]
        )

        if speed > OUTER_POINT_MAX_SPEED:

            p["vx"] = (
                p["vx"]
                / speed
                * OUTER_POINT_MAX_SPEED
            )

            p["vy"] = (
                p["vy"]
                / speed
                * OUTER_POINT_MAX_SPEED
            )

        elif speed < OUTER_POINT_MIN_SPEED:

            if speed == 0:

                direction = random.uniform(
                    0,
                    math.pi * 2
                )

                p["vx"] = (
                    math.cos(direction)
                    * OUTER_POINT_MIN_SPEED
                )

                p["vy"] = (
                    math.sin(direction)
                    * OUTER_POINT_MIN_SPEED
                )

            else:

                p["vx"] = (
                    p["vx"]
                    / speed
                    * OUTER_POINT_MIN_SPEED
                )

                p["vy"] = (
                    p["vy"]
                    / speed
                    * OUTER_POINT_MIN_SPEED
                )

        # =================================================
        # KHOẢNG CÁCH TỚI TÂM
        # =================================================

        dx = (
            p["x"]
            - triangle["center_x"]
        )

        dy = (
            p["y"]
            - triangle["center_y"]
        )

        distance = math.hypot(
            dx,
            dy
        )

        # =================================================
        # KÉO VỀ TÂM
        # =================================================

        if distance > p["max_radius"]:

            if distance > 0:

                nx = dx / distance
                ny = dy / distance

                force = OUTER_POINT_RETURN_FORCE

                p["vx"] -= (
                    nx * force
                )

                p["vy"] -= (
                    ny * force
                )


# =========================================================
# VẼ CONNECTION
# =========================================================

def draw_connections(
    frame,
    clusters,
    connections
):

    for connection in connections:

        cluster_a = connection[
            "cluster_a"
        ]

        point_a = connection[
            "point_a"
        ]

        cluster_b = connection[
            "cluster_b"
        ]

        point_b = connection[
            "point_b"
        ]

        p1 = clusters[
            cluster_a
        ]["points"][
            point_a
        ]

        p2 = clusters[
            cluster_b
        ]["points"][
            point_b
        ]

        pt1 = (
            int(p1["x"]),
            int(p1["y"])
        )

        pt2 = (
            int(p2["x"]),
            int(p2["y"])
        )

        cv2.line(
            frame,
            pt1,
            pt2,
            CONNECTION_COLOR,
            LINE_WIDTH,
            cv2.LINE_AA
        )


# =========================================================
# VẼ CỤM CHÍNH
# =========================================================

def draw_cluster(
    frame,
    cluster
):

    points = cluster["points"]

    pt1 = (
        int(points[0]["x"]),
        int(points[0]["y"])
    )

    pt2 = (
        int(points[1]["x"]),
        int(points[1]["y"])
    )

    pt3 = (
        int(points[2]["x"]),
        int(points[2]["y"])
    )

    triangle = np.array(
        [
            pt1,
            pt2,
            pt3
        ],
        dtype=np.int32
    )

    # =====================================================
    # FILL
    # =====================================================

    if cluster["filled"]:

        overlay = frame.copy()

        cv2.fillPoly(
            overlay,
            [triangle],
            FILL_COLOR
        )

        cv2.addWeighted(
            overlay,
            FILL_ALPHA,
            frame,
            1 - FILL_ALPHA,
            0,
            frame
        )

    # =====================================================
    # 3 CẠNH
    # =====================================================

    cv2.line(
        frame,
        pt1,
        pt2,
        COLOR,
        LINE_WIDTH,
        cv2.LINE_AA
    )

    cv2.line(
        frame,
        pt2,
        pt3,
        COLOR,
        LINE_WIDTH,
        cv2.LINE_AA
    )

    cv2.line(
        frame,
        pt3,
        pt1,
        COLOR,
        LINE_WIDTH,
        cv2.LINE_AA
    )

    # =====================================================
    # 3 ĐIỂM
    # =====================================================

    for p in points:

        center = (
            int(p["x"]),
            int(p["y"])
        )

        cv2.circle(
            frame,
            center,
            POINT_RADIUS,
            COLOR,
            -1,
            cv2.LINE_AA
        )


# =========================================================
# VẼ TAM GIÁC NGOÀI
# =========================================================

def draw_outer_triangle(
    frame,
    triangle
):

    points = triangle["points"]

    # =====================================================
    # LUÔN ĐÚNG 3 ĐIỂM
    # =====================================================

    if len(points) != 3:
        return

    pt1 = (
        int(points[0]["x"]),
        int(points[0]["y"])
    )

    pt2 = (
        int(points[1]["x"]),
        int(points[1]["y"])
    )

    pt3 = (
        int(points[2]["x"]),
        int(points[2]["y"])
    )

    polygon = np.array(
        [
            pt1,
            pt2,
            pt3
        ],
        dtype=np.int32
    )

    # =====================================================
    # FILL
    # =====================================================

    if triangle["filled"]:

        overlay = frame.copy()

        cv2.fillPoly(
            overlay,
            [polygon],
            FILL_COLOR
        )

        cv2.addWeighted(
            overlay,
            0.30,
            frame,
            0.70,
            0,
            frame
        )

    # =====================================================
    # 3 CẠNH
    # =====================================================

    cv2.line(
        frame,
        pt1,
        pt2,
        COLOR,
        LINE_WIDTH,
        cv2.LINE_AA
    )

    cv2.line(
        frame,
        pt2,
        pt3,
        COLOR,
        LINE_WIDTH,
        cv2.LINE_AA
    )

    cv2.line(
        frame,
        pt3,
        pt1,
        COLOR,
        LINE_WIDTH,
        cv2.LINE_AA
    )

    # =====================================================
    # 3 ĐIỂM
    # =====================================================

    for p in points:

        center = (
            int(p["x"]),
            int(p["y"])
        )

        cv2.circle(
            frame,
            center,
            OUTER_POINT_RADIUS,
            COLOR,
            -1,
            cv2.LINE_AA
        )


# =========================================================
# MAIN
# =========================================================

def main():

    # =====================================================
    # TẠO CỤM CHÍNH
    # =====================================================

    clusters = create_clusters()

    # =====================================================
    # TẠO MẠNG CHÍNH
    # =====================================================

    connections = create_connections(
        clusters
    )

    # =====================================================
    # TẠO TAM GIÁC NGOÀI
    # =====================================================

    # outer_triangles = create_outer_triangles(
    #     clusters
    # )
    # Không tạo tam giác ngoài
    outer_triangles = []

    # =====================================================
    # THỐNG KÊ
    # =====================================================

    filled_count = sum(
        1
        for cluster in clusters
        if cluster["filled"]
    )

    outer_filled_count = sum(
        1
        for triangle in outer_triangles
        if triangle["filled"]
    )

    total_outer_points = sum(
        len(triangle["points"])
        for triangle in outer_triangles
    )

    print(
        "=============================================="
    )

    print(
        "ĐANG TẠO VIDEO"
    )

    print(
        "=============================================="
    )

    print(
        f"Kích thước          : "
        f"{WIDTH} x {HEIGHT}"
    )

    print(
        f"FPS                 : "
        f"{FPS}"
    )

    print(
        f"Thời lượng          : "
        f"{DURATION} giây"
    )

    print(
        f"Điểm chính          : "
        f"{NUM_POINTS}"
    )

    print(
        f"Cụm chính           : "
        f"{NUM_CLUSTERS}"
    )

    print(
        f"Connection chính    : "
        f"{len(connections)}"
    )

    print(
        f"Tam giác chính fill : "
        f"{filled_count}"
    )

    print(
        f"Tam giác ngoài      : "
        f"{len(outer_triangles)}"
    )

    print(
        f"Điểm tam giác ngoài : "
        f"{total_outer_points}"
    )

    print(
        f"Tam giác ngoài fill : "
        f"{outer_filled_count}"
    )

    print(
        "Mạng chính          : LIÊN THÔNG"
    )

    print(
        "Tam giác ngoài      : 3 ĐIỂM / TAM GIÁC"
    )

    print(
        "Chuyển động ngoài   : MẠNH + XOAY + DAO ĐỘNG"
    )

    print(
        "Kích thước ngoài    : LỚN + KÉO DÀI"
    )

    print(
        "=============================================="
    )

    print()

    # =====================================================
    # VIDEO WRITER
    # =====================================================

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    out = cv2.VideoWriter(
        OUTPUT_FILE,
        fourcc,
        FPS,
        (
            WIDTH,
            HEIGHT
        )
    )

    if not out.isOpened():

        print(
            "LỖI: Không thể tạo video!"
        )

        return

    # =====================================================
    # RENDER
    # =====================================================

    total_frames = (
        FPS * DURATION
    )

    for frame_number in range(
        total_frames
    ):

        # =================================================
        # NỀN
        # =================================================

        frame = np.full(
            (
                HEIGHT,
                WIDTH,
                3
            ),
            BG_COLOR,
            dtype=np.uint8
        )

        # =================================================
        # UPDATE CỤM CHÍNH
        # =================================================

        for cluster in clusters:

            update_cluster(
                cluster,
                frame_number
            )

        # =================================================
        # UPDATE TAM GIÁC NGOÀI
        # =================================================

        for triangle in outer_triangles:

            update_outer_triangle(
                triangle
            )

        # =================================================
        # VẼ TAM GIÁC NGOÀI TRƯỚC
        # =================================================

        for triangle in outer_triangles:

            draw_outer_triangle(
                frame,
                triangle
            )

        # =================================================
        # VẼ CONNECTION
        # =================================================

        draw_connections(
            frame,
            clusters,
            connections
        )

        # =================================================
        # VẼ CỤM CHÍNH
        # =================================================

        for cluster in clusters:

            draw_cluster(
                frame,
                cluster
            )

        # =================================================
        # GHI VIDEO
        # =================================================

        out.write(
            frame
        )

        # =================================================
        # PROGRESS
        # =================================================

        if frame_number % FPS == 0:

            second = (
                frame_number // FPS
            )

            print(
                f"Đang render: "
                f"{second}/{DURATION} giây"
            )

    # =====================================================
    # RELEASE
    # =====================================================

    out.release()

    print()

    print(
        "=============================================="
    )

    print(
        "HOÀN THÀNH!"
    )

    print(
        "=============================================="
    )

    print(
        f"File: {OUTPUT_FILE}"
    )


# =========================================================
# CHẠY
# =========================================================

if __name__ == "__main__":

    main()
