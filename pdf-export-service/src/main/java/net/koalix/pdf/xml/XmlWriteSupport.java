package net.koalix.pdf.xml;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

/** Small shortcuts to keep XmlBuilder implementations readable. */
public final class XmlWriteSupport {

    private XmlWriteSupport() {}

    public static void writeText(XMLStreamWriter writer, String name, Object value)
            throws XMLStreamException {
        if (value == null) {
            return;
        }
        writer.writeStartElement(name);
        writer.writeCharacters(String.valueOf(value));
        writer.writeEndElement();
    }

    public static void writeAttribute(XMLStreamWriter writer, String name, Object value)
            throws XMLStreamException {
        if (value == null) {
            return;
        }
        writer.writeAttribute(name, String.valueOf(value));
    }
}
