package net.koalix.pdf.template;

import java.nio.file.Path;

/**
 * Local filesystem paths to the template assets needed by FOP for one render.
 * Caller is responsible for cleaning these up once rendering is done.
 */
public record TemplateAssets(Path xslFile, Path fopConfigFile, Path logoFile) {
}
