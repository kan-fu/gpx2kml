import xml.etree.ElementTree as ET
from pathlib import Path
from textwrap import dedent, indent
from typing import Iterator

from gpx2kml.gpx import GPX


class KML:
    kml_template = dedent(
        """\
        <?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2">
        </kml>"""
    )

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

    def _add_placemark_to_document(self, gpx_path: Path):
        self.get_document_ele().append(KML.new_placemark(gpx_path))

    def add_gpx_files_to_document(self, gpx_paths: Iterator[Path]):
        for gpx_path in gpx_paths:
            self._add_placemark_to_document(gpx_path)

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
        kml_folder = f"""\
            <Folder>
                <name>{name}</name>
            </Folder>"""
        return ET.fromstring(kml_folder)

    @staticmethod
    def new_document(name: str):
        kml_document = f"""\
            <Document>
                <name>{name}</name>
            </Document>"""
        return ET.fromstring(kml_document)

    @staticmethod
    def new_style(style_id: str, color: str, width: int):
        kml_style = f"""\
            <Style id="{style_id}">
                <LineStyle>
                    <color>{color}</color>
                    <width>{width}</width>
                </LineStyle>
            </Style>"""
        return ET.fromstring(kml_style)

    @staticmethod
    def new_placemark(gpx_path: Path) -> ET.Element:
        gpx = GPX(gpx_path)

        description = "\n" + indent(gpx.get_desc(), "\t\t\t")
        kml_placemark = f"""\
            <Placemark>
                <name>{gpx.get_name()}</name>
                <description>{description}</description>
                <styleUrl>#{gpx.get_type()}</styleUrl>
                <MultiGeometry></MultiGeometry>
            </Placemark>"""
        placemark_ele: ET.Element = ET.fromstring(kml_placemark)

        for seg_coords in gpx.extract_latlon():
            placemark_ele.find("MultiGeometry").append(KML.new_line_string(seg_coords))  # type: ignore
        return placemark_ele

    @staticmethod
    def new_line_string(seg_coords: list[tuple[str, str]]) -> ET.Element:
        kml_line_string = f"""\
            <LineString>
                <coordinates>{" ".join([f"{lon},{lat},0" for lat, lon in seg_coords])}</coordinates>
            </LineString>"""

        return ET.fromstring(kml_line_string)
