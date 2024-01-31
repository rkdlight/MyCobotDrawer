from svg.path import *
from xml.dom import minidom
import BaseClasses

def parse_svg(filepath):
    # read the SVG file
    doc = minidom.parse(filepath)
    path_strings = [path.getAttribute('d') for path in doc.getElementsByTagName('path')]
    doc.unlink()

    image_objects = []
    for path_string in path_strings:
        path = parse_path(path_string)
        path_objects = []
        for element in path:
            if isinstance(element, Move):

                path_objects.append(
                    BaseClasses.Move(element.start.real, element.start.imag)
                )
            elif isinstance(element, Line):
                path_objects.append(
                    BaseClasses.Line(element.start.real, element.start.imag, element.end.real, element.end.imag)
                )
            elif isinstance(element, CubicBezier):
                path_objects.append(
                    BaseClasses.CubicCurve(element.start.real, element.start.imag,
                                           element.control1.real, element.control1.imag,
                                           element.control2.real, element.control2.imag,
                                           element.end.real, element.end.imag
                                           )
                )
            elif isinstance(element, QuadraticBezier):
                path_objects.append(
                    BaseClasses.QuadraticCurve(element.start.real, element.start.imag,
                                           element.control.real, element.control.imag,
                                           element.end.real, element.end.imag)
                )
            elif isinstance(element, Arc):
                path_objects.append(
                    BaseClasses.ArcCurve(element.start.real, element.start.imag, element.radius.real, element.radius.imag,
                                         element.rotation, element.arc, element.sweep, element.end.real, element.end.imag)
                )

        image_objects.append(path_objects)

    return image_objects

if __name__ == '__main__':
    objects = parse_svg("C:/Users/konop/Downloads/25344740_4900_5_06.svg")