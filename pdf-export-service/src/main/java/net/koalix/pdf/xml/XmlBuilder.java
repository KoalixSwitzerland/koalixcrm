package net.koalix.pdf.xml;

import javax.xml.stream.XMLStreamException;
import javax.xml.stream.XMLStreamWriter;

/**
 * One StAX-based XML writer per DTO type.
 *
 * <p>Implementations MUST write a single XML element representing {@code dto}
 * (including its subtree). Element name and attributes are chosen to be
 * compatible with the existing XSL-FO stylesheets — any change to an
 * implementation is a coordinated release with the templates bucket.
 */
public interface XmlBuilder<T> {

    void write(XMLStreamWriter writer, T dto) throws XMLStreamException;
}
