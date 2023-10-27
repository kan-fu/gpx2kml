import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterator


class GPX:
    __ns = {"ns": "http://www.topografix.com/GPX/1/1"}

    def __init__(self, path: str | Path):
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()

        ET.register_namespace("", GPX.__ns["ns"])
        # assert ET.tostring(self.root, encoding="unicode").count("trkseg") % 2 == 0

    def get_type(self) -> str:
        type_ele = self.root.find("*//ns:type", GPX.__ns)
        if type_ele is not None and type_ele.text is not None:
            return type_ele.text
        else:
            return ""

    def get_name(self) -> str:
        name_ele = self.root.find("*//ns:name", GPX.__ns)
        if name_ele is not None and name_ele.text is not None:
            return name_ele.text
        else:
            return ""

    def get_desc(self) -> str:
        desc_ele = self.root.find("*//ns:desc", GPX.__ns)
        if desc_ele is not None and desc_ele.text is not None:
            return desc_ele.text
        else:
            return ""

    def add_meta(self, meta_info: dict[str, str]):
        """
        Add the desc and type tag under trk tag. Works only when the gpx does not have desc and type tag.
        """
        desc_tag = ET.Element("desc")
        desc_tag.text = meta_info["desc"]
        desc_tag.tail = "\n  "
        type_tag = ET.Element("type")
        type_tag.text = meta_info["type"]
        type_tag.tail = "\n  "
        trk = self.root.find("ns:trk", GPX.__ns)
        assert trk is not None
        trk.insert(1, desc_tag)
        trk.insert(1, type_tag)

    def extract_latlon(self) -> Iterator[list[tuple[str, str]]]:
        for trkseg in self.root[0].findall("ns:trkseg", GPX.__ns):
            seg_coords = []
            for trkpt in trkseg.findall("ns:trkpt", GPX.__ns):
                seg_coords.append((trkpt.attrib["lat"], trkpt.attrib["lon"]))
            yield seg_coords

    def export(self, output_file: Path):
        self.tree.write(output_file, xml_declaration=True, encoding="UTF-8")
