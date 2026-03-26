import xml.etree.ElementTree as ET
from pathlib import Path
from textwrap import dedent, indent
from typing import Iterator

from gpx2kml.gpx import GPX


class KML:
    kml_template = dedent("""\
        <?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
        </kml>""")

    __ns = {"ns": "http://www.opengis.net/kml/2.2"}

    def __init__(self, kml_path: Path, mode: str):
        self.kml_path = kml_path

        if mode == "new":
            self.root = ET.fromstring(KML.kml_template)
        elif mode == "read":
            assert kml_path.exists()
            self.root = ET.parse(kml_path).getroot()
        else:
            raise ValueError("mode is unknown")

    def get_document_ele(self):
        return self.root.find("ns:Document", KML.__ns) or self.root.find("Document")

    def get_folder_ele(self):
        return self.root.find("ns:Folder", KML.__ns) or self.root.find("Folder")

    def get_sub_folder_ele(self):
        return self.root.findall("Folder/Folder")[-1]

    def add_style_to_document(self, style_id: str, color: str, width: int):
        self.get_document_ele().append(KML.new_style(style_id, color, width))

    def _add_placemark_to_document(self, gpx: GPX):
        self.get_document_ele().append(KML.new_placemark(gpx))

    def add_gpx_files_to_document(self, gpx_paths: Iterator[Path]):
        for gpx_path in gpx_paths:
            self._add_placemark_to_document(GPX(gpx_path))

    def add_gpx_file_to_document(self, gpx_path: Path):
        self.add_gpx_to_document(GPX(gpx_path))

    def add_gpx_to_document(self, gpx: GPX):
        self._add_placemark_to_document(gpx)

    def _add_sub_folder_to_folder(self, sub_folder):
        self.get_folder_ele().append(sub_folder)

    def add_sub_folder(self, year: str, kml_sublist: Iterator[Path]):
        sub_folder = KML.new_folder(year)
        for kml_path in kml_sublist:
            kml = KML(kml_path, mode="read")
            sub_folder.append(kml.get_document_ele())
        self._add_sub_folder_to_folder(sub_folder)

    def add_document(self):
        self.root.append(KML.new_document(self.kml_path.stem))

    def add_folder(self):
        self.root.append(KML.new_folder(self.kml_path.stem))

    def export(self) -> None:
        ET.register_namespace("", KML.__ns["ns"])
        ET.indent(ET.ElementTree(self.root), space="\t")
        ET.ElementTree(self.root).write(
            self.kml_path,
            xml_declaration=True,
            encoding="UTF-8",
        )

    @staticmethod
    def new_folder(name: str):
        folder = ET.Element("Folder")
        name_ele = ET.SubElement(folder, "name")
        name_ele.text = name
        return folder

    @staticmethod
    def new_document(name: str):
        document = ET.Element("Document")
        name_ele = ET.SubElement(document, "name")
        name_ele.text = name
        return document

    @staticmethod
    def new_style(style_id: str, color: str, width: int):
        style = ET.Element("Style", attrib={"id": style_id})
        line_style = ET.SubElement(style, "LineStyle")
        color_ele = ET.SubElement(line_style, "color")
        color_ele.text = color
        width_ele = ET.SubElement(line_style, "width")
        width_ele.text = str(width)
        return style

    @staticmethod
    def new_placemark(gpx: GPX) -> ET.Element:
        placemark = ET.Element("Placemark")

        name_ele = ET.SubElement(placemark, "name")
        name_ele.text = gpx.get_name()

        description_ele = ET.SubElement(placemark, "description")
        description_ele.text = "\n" + indent(gpx.get_desc(), "\t\t\t")

        style_url_ele = ET.SubElement(placemark, "styleUrl")
        style_url_ele.text = f"#{gpx.get_type()}"

        multi_geometry = ET.SubElement(placemark, "MultiGeometry")
        for seg_coords in gpx.extract_latlon():
            multi_geometry.append(KML.new_line_string(seg_coords))
        return placemark

    @staticmethod
    def new_line_string(seg_coords: list[tuple[str, str]]) -> ET.Element:
        line_string = ET.Element("LineString")
        coordinates = ET.SubElement(line_string, "coordinates")
        coordinates.text = " ".join(f"{lon},{lat},0" for lat, lon in seg_coords)
        return line_string
