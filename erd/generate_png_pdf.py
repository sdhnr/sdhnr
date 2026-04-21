"""Generate PNG and PDF ERD visuals without external dependencies.

This is a fallback artifact generator for constrained environments where
Graphviz/eralchemy cannot run.
"""

from __future__ import annotations

from pathlib import Path
import struct
import zlib

OUT = Path("erd/output")

CURRENT_NODES = [
    "CUSTOMER", "ORDER", "PRODUCT", "CATEGORY", "ORDERDETAILS",
    "SUPPLIER", "INVENTORY", "WAREHOUSE", "PAYMENT", "EMPLOYEE",
]
CURRENT_EDGES = [
    ("ORDER", "ORDERDETAILS"),
    ("PRODUCT", "ORDERDETAILS"),
    ("PRODUCT", "INVENTORY"),
    ("ORDER", "PAYMENT"),
    ("CATEGORY", "CATEGORY"),
]

IMPROVED_NODES = [
    "CUSTOMER", "CUSTOMERADDRESS", "ORDER", "ORDERITEM", "CATEGORY",
    "PRODUCT", "SUPPLIER", "PRODUCTSUPPLIER", "WAREHOUSE", "INVENTORY",
    "PAYMENT", "EMPLOYEE",
]
IMPROVED_EDGES = [
    ("CUSTOMER", "CUSTOMERADDRESS"),
    ("CUSTOMER", "ORDER"),
    ("ORDER", "ORDERITEM"),
    ("PRODUCT", "ORDERITEM"),
    ("CATEGORY", "PRODUCT"),
    ("PRODUCT", "PRODUCTSUPPLIER"),
    ("SUPPLIER", "PRODUCTSUPPLIER"),
    ("PRODUCT", "INVENTORY"),
    ("WAREHOUSE", "INVENTORY"),
    ("ORDER", "PAYMENT"),
    ("EMPLOYEE", "PAYMENT"),
]

FONT = {
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "B": ["11110","10001","10001","11110","10001","10001","11110"],
    "C": ["01111","10000","10000","10000","10000","10000","01111"],
    "D": ["11110","10001","10001","10001","10001","10001","11110"],
    "E": ["11111","10000","10000","11110","10000","10000","11111"],
    "F": ["11111","10000","10000","11110","10000","10000","10000"],
    "G": ["01111","10000","10000","10111","10001","10001","01110"],
    "H": ["10001","10001","10001","11111","10001","10001","10001"],
    "I": ["11111","00100","00100","00100","00100","00100","11111"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    "M": ["10001","11011","10101","10001","10001","10001","10001"],
    "N": ["10001","11001","10101","10011","10001","10001","10001"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "P": ["11110","10001","10001","11110","10000","10000","10000"],
    "R": ["11110","10001","10001","11110","10100","10010","10001"],
    "S": ["01111","10000","10000","01110","00001","00001","11110"],
    "T": ["11111","00100","00100","00100","00100","00100","00100"],
    "U": ["10001","10001","10001","10001","10001","10001","01110"],
    "V": ["10001","10001","10001","10001","10001","01010","00100"],
    "W": ["10001","10001","10001","10001","10101","11011","10001"],
    "Y": ["10001","10001","01010","00100","00100","00100","00100"],
    "_": ["00000","00000","00000","00000","00000","00000","11111"],
}


def layout(nodes: list[str], cols: int = 4):
    pos = {}
    for i, n in enumerate(nodes):
        r, c = divmod(i, cols)
        pos[n] = (40 + c * 220, 40 + r * 140)
    return pos


def draw_diagram_png(path: Path, title: str, nodes: list[str], edges: list[tuple[str, str]]):
    w, h = 980, 620
    pix = bytearray([255, 255, 255] * w * h)

    def set_px(x, y, rgb=(0, 0, 0)):
        if 0 <= x < w and 0 <= y < h:
            i = (y * w + x) * 3
            pix[i:i+3] = bytes(rgb)

    def line(x1, y1, x2, y2):
        dx = abs(x2 - x1); sx = 1 if x1 < x2 else -1
        dy = -abs(y2 - y1); sy = 1 if y1 < y2 else -1
        err = dx + dy
        while True:
            set_px(x1, y1)
            if x1 == x2 and y1 == y2: break
            e2 = 2 * err
            if e2 >= dy: err += dy; x1 += sx
            if e2 <= dx: err += dx; y1 += sy

    def rect(x, y, rw, rh):
        for i in range(x, x + rw):
            set_px(i, y); set_px(i, y + rh)
        for j in range(y, y + rh):
            set_px(x, j); set_px(x + rw, j)

    def text(x, y, s):
        for ch in s:
            glyph = FONT.get(ch, FONT.get("_"))
            for gy, row in enumerate(glyph):
                for gx, bit in enumerate(row):
                    if bit == "1":
                        set_px(x + gx, y + gy)
            x += 7

    positions = layout(nodes)
    text(20, 10, title.upper().replace(" ", "_"))

    for a, b in edges:
        ax, ay = positions[a]; bx, by = positions[b]
        line(ax + 80, ay + 60, bx + 80, by)

    for n, (x, y) in positions.items():
        rect(x, y, 160, 60)
        text(x + 10, y + 24, n)

    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(pix[y*w*3:(y+1)*w*3])

    def chunk(t, d):
        return struct.pack("!I", len(d)) + t + d + struct.pack("!I", zlib.crc32(t + d) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b'IHDR', struct.pack("!2I5B", w, h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    path.write_bytes(png)


def draw_diagram_pdf(path: Path, title: str, nodes: list[str], edges: list[tuple[str, str]]):
    positions = layout(nodes)
    cmds = ["0 0 0 RG 1 w", "BT /F1 14 Tf 40 800 Td ({}) Tj ET".format(title)]

    for a, b in edges:
        ax, ay = positions[a]; bx, by = positions[b]
        y1 = 842 - (ay + 60)
        y2 = 842 - by
        cmds.append(f"{ax+80} {y1} m {bx+80} {y2} l S")

    for n, (x, y) in positions.items():
        yy = 842 - y - 60
        cmds.append(f"{x} {yy} 160 60 re S")
        cmds.append(f"BT /F1 10 Tf {x+10} {yy+30} Td ({n}) Tj ET")

    stream = "\n".join(cmds).encode()

    objects = []
    def add(obj: bytes):
        objects.append(obj)

    add(b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n")
    add(b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n")
    add(b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 1000 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>endobj\n")
    add(b"4 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n")
    add(f"5 0 obj<< /Length {len(stream)} >>stream\n".encode() + stream + b"\nendstream endobj\n")

    pdf = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for off in offsets[1:]:
        pdf.extend(f"{off:010d} 00000 n \n".encode())
    pdf.extend(f"trailer<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
    path.write_bytes(pdf)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    draw_diagram_png(OUT / "current_erd.png", "Current ERD", CURRENT_NODES, CURRENT_EDGES)
    draw_diagram_pdf(OUT / "current_erd.pdf", "Current ERD", CURRENT_NODES, CURRENT_EDGES)
    draw_diagram_png(OUT / "improved_erd.png", "Improved ERD", IMPROVED_NODES, IMPROVED_EDGES)
    draw_diagram_pdf(OUT / "improved_erd.pdf", "Improved ERD", IMPROVED_NODES, IMPROVED_EDGES)
    print("Generated PNG/PDF artifacts in erd/output")


if __name__ == "__main__":
    main()
