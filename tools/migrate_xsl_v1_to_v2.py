#!/usr/bin/env python3
"""Mechanical rewrite of pre-v2.0.0 XSL templates to the v2.0 XML shape.

Covers the XPath-string rewrite rules (1-4, 6, 8, 10-12, 14-16) from
docs/migration-v1.14.0-to-v2.0.0.md. The structural rewrites (rules 5,
7, 9, 13) are left for a follow-up pass — search markers
`MIGRATION_TODO:` are inserted where human/agent review is needed.

Usage:
    python tools/migrate_xsl_v1_to_v2.py FILE...
    python tools/migrate_xsl_v1_to_v2.py --all
"""
from __future__ import annotations

import argparse
import difflib
import os
import re
import sys
from pathlib import Path

REPO = Path("/app/koalixcrm")

# The v1 templates live outside the repo (the tree that held them also held
# customer data). Set KOALIXCRM_LEGACY_TEMPLATE_DIR to include them in --all;
# without it, only the in-repo default templates are rewritten.
_legacy = os.environ.get("KOALIXCRM_LEGACY_TEMPLATE_DIR")
DEFAULT_ROOTS = [
    *([Path(_legacy)] if _legacy else []),
    REPO / "projectsettings/static/default_templates/de",
    REPO / "projectsettings/static/default_templates/en",
]

# Each rule: (compiled regex, replacement, human-readable name).
RULES: list[tuple[re.Pattern, str, str]] = []


def _add(pattern: str, repl: str, name: str) -> None:
    RULES.append((re.compile(pattern), repl, name))


# Rule 1 - root template match.
_add(
    r'''(<xsl:template\s+match=")django-objects(")''',
    r'''\1koalixcrm-export\2''',
    "root-match",
)

# Rule 2/3 - salesdocument and subtype-specific fields flattened.
#   object[@model='crm.salesdocument']/field[@name='X']  ->  commercial_document/X
#   object[@model='crm.invoice']/field[@name='X']        ->  commercial_document/X
#   object[@model='crm.quote']/field[@name='X']          ->  commercial_document/X
#   object[@model='crm.quotation']/field[@name='X']      ->  commercial_document/X
#   object[@model='crm.creditnote']/field[@name='X']     ->  commercial_document/X
#   object[@model='crm.paymentreminder']/field[@name='X']->  commercial_document/X
#   object[@model='crm.despatchadvice']/field[@name='X'] ->  commercial_document/X
#   object[@model='crm.purchaseorder']/field[@name='X']  ->  commercial_document/X
_add(
    r"""object\[@model=['"]crm\.(?:salesdocument|invoice|quote|quotation|creditnote|paymentreminder|despatchadvice|purchaseorder)['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""commercial_document/\1""",
    "document-field",
)
# Same, bare @pk -> @id
_add(
    r"""object\[@model=['"]crm\.(?:salesdocument|invoice|quote|quotation|creditnote|paymentreminder|despatchadvice|purchaseorder)['"]\]/@pk""",
    r"""commercial_document/@id""",
    "document-pk",
)
# Bare document element (no trailing /field or /@pk): object[@model='crm.salesdocument']
_add(
    r"""object\[@model=['"]crm\.(?:salesdocument|invoice|quote|quotation|creditnote|paymentreminder|despatchadvice|purchaseorder)['"]\]""",
    r"""commercial_document""",
    "document-element",
)

# Rule 4 - currency.
_add(
    r"""object\[@model=['"]crm\.currency['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""commercial_document/currency/\1""",
    "currency-field",
)
_add(
    r"""object\[@model=['"]crm\.currency['"]\]/@pk""",
    r"""commercial_document/currency/@id""",
    "currency-pk",
)
_add(
    r"""object\[@model=['"]crm\.currency['"]\]""",
    r"""commercial_document/currency""",
    "currency-element",
)

# Rule 5 (partial) - contact -> party. Structural choose-block left for agent.
#   object[@model='crm.contact']/@pk -> commercial_document/party/@id
#   object[@model='crm.contact']/field[@name='name'] -> commercial_document/party/display_name
_add(
    r"""object\[@model=['"]crm\.contact['"]\]/@pk""",
    r"""commercial_document/party/@id""",
    "contact-pk",
)
_add(
    r"""object\[@model=['"]crm\.contact['"]\]/field\[@name=['"]name['"]\]""",
    r"""commercial_document/party/display_name""",
    "contact-name",
)
_add(
    r"""object\[@model=['"]crm\.contact['"]\]""",
    r"""commercial_document/party""",
    "contact-element",
)

# Rule 6 - postal address: we default to billing, first match.
# object[@model='crm.postaladdress']/field[@name='pre_name' or 'name']  ->  needs manual review
# (rule 5 structural rewrite); we tag it.
_add(
    r"""object\[@model=['"]crm\.postaladdress['"]\]/field\[@name=['"](pre_name|name)['"]\]""",
    r"""commercial_document/party/_MIGRATION_TODO_addressee_\1""",
    "postal-addressee-todo",
)
# Generic postal fields -> party/postal_address[@purpose='billing'][1]/FIELD
_add(
    r"""object\[@model=['"]crm\.postaladdress['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""commercial_document/party/postal_address[@purpose='billing' or @is_primary='true'][1]/\1""",
    "postal-field",
)
_add(
    r"""object\[@model=['"]crm\.postaladdressforcontact['"]\]/field\[@name=['"]purpose['"]\]""",
    r"""commercial_document/party/postal_address/@purpose""",
    "postal-purpose",
)

# Rule 6/7 - phone and email. The legacy template often used these for BOTH
# party and user-extension contexts; disambiguating is structural so we
# prefer the party-side translation and tag the other cases.
_add(
    r"""object\[@model=['"]crm\.phoneaddress['"]\]/field\[@name=['"]phone['"]\]""",
    r"""commercial_document/party/phone_number[1]""",
    "phone",
)
_add(
    r"""object\[@model=['"]crm\.emailaddress['"]\]/field\[@name=['"]email['"]\]""",
    r"""commercial_document/party/email_address[1]""",
    "email",
)

# Rule 7 - user / user-extension.
_add(
    r"""object\[@model=['"]auth\.user['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""user_extension/user/\1""",
    "user-field",
)
_add(
    r"""object\[@model=['"]auth\.user['"]\]/@pk""",
    r"""user_extension/user/@id""",
    "user-pk",
)
# Issuing-org / filebrowser-driven fields -> MIGRATION_TODO (not in XML).
_add(
    r"""object\[@model=['"]djangoUserExtension\.documenttemplate['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""_MIGRATION_TODO_documenttemplate_\1""",
    "documenttemplate-todo",
)
_add(
    r"""object\[@model=['"]djangoUserExtension\.templateset['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""_MIGRATION_TODO_templateset_\1""",
    "templateset-todo",
)
_add(
    r"""object\[@model=['"]djangoUserExtension\.userextension['"]\]/field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""user_extension/\1""",
    "userextension-field",
)
# Filebrowser dir variable (was a top-level sibling in django-objects).
_add(
    r"""\bfilebrowser_directory\b""",
    r"""_MIGRATION_TODO_filebrowser_directory""",
    "filebrowser-todo",
)

# Rule 8 - positions.
_add(
    r"""object\[@model=['"]crm\.position['"]\]""",
    r"""commercial_document/items/position""",
    "position-element",
)
# Position sort key typo: select="field[@name=position_number]" (unquoted) -> position_number
_add(
    r'<xsl:sort\s+select="field\[@name=position_number\]"',
    r'<xsl:sort select="position_number"',
    "position-sort-fix",
)
# Generic `field[@name='X']` inside a position loop -> plain element.
# This is safe-ish because inside `for-each ... position`, field[@name='X']
# referred to a position field. But it's also used inside other contexts in
# some templates; the rewrite is still locally correct for those because the
# new XML uses bare element names. We translate UNQUALIFIED field[...]
# (no object[...] prefix) everywhere.
_add(
    r"""field\[@name=['"]([a-z_0-9]+)['"]\]""",
    r"""\1""",
    "bare-field",
)

# Rule 9 - product dereference.
# Drop patterns like: ../object[@model='crm.product' and @pk=$x]/field[@name='Y']
# -> product_type/Y  (after rule "bare-field" these are already elementified).
_add(
    r"""\.\./object\[@model=['"]crm\.product['"]\s+and\s+@pk=\$[a-zA-Z_0-9]+\]/""",
    r"""product_type/""",
    "product-lookup",
)
# Rule 10 - unit dereference.
_add(
    r"""\.\./object\[@model=['"]crm\.unit['"]\s+and\s+@pk=\$[a-zA-Z_0-9]+\]/""",
    r"""unit/""",
    "unit-lookup",
)

# Rule 11 - currency relative-from-position reference.
_add(
    r"""\.\./object\[@model=['"]crm\.currency['"]\]/""",
    r"""../../currency/""",
    "currency-relative",
)

# Rule 12 - None tests.
# Matches <xsl:when test="X/None"> or select="X/None" — we only neutralise the
# predicate. The XSL pattern `field[...]/None` is almost always used inside a
# test=""; rewriting it to `not(X) or string(X)=''` would change the XSL
# grammar in places that are hard to detect, so we minimally rewrite the
# appended /None to `=''` to keep the test compiling. The downstream agent can
# tighten it per case if needed.
_add(
    r"""/None(?=['"\]\s])""",
    r"""[string(.)='']""",
    "none-test",
)

# Rule 13 - text paragraphs. Tag every remaining occurrence.
_add(
    r"""object\[@model=['"]crm\.textparagraphinsalesdocument['"]\]""",
    r"""_MIGRATION_TODO_textparagraph""",
    "textparagraph-todo",
)


def rewrite(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for pattern, repl, name in RULES:
        new_text, n = pattern.subn(repl, text)
        if n:
            counts[name] = counts.get(name, 0) + n
        text = new_text
    return text, counts


def process_file(path: Path, write: bool) -> dict[str, int]:
    original = path.read_text(encoding="utf-8")
    new, counts = rewrite(original)
    if not counts:
        return counts
    if write:
        path.write_text(new, encoding="utf-8")
    else:
        diff = difflib.unified_diff(
            original.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=str(path),
            tofile=str(path) + " (migrated)",
            n=1,
        )
        sys.stdout.writelines(diff)
    return counts


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="process every XSL under the known roots")
    ap.add_argument("--dry-run", action="store_true", help="print a diff instead of writing")
    ap.add_argument("files", nargs="*", type=Path)
    args = ap.parse_args(argv)

    files: list[Path] = list(args.files)
    if args.all:
        for root in DEFAULT_ROOTS:
            files.extend(sorted(root.glob("*.xsl")))
    if not files:
        ap.error("pass --all or one or more .xsl files")

    totals: dict[str, int] = {}
    for f in files:
        if not f.exists():
            print(f"skip (missing): {f}", file=sys.stderr)
            continue
        counts = process_file(f, write=not args.dry_run)
        label = f.relative_to(REPO) if f.is_absolute() and REPO in f.parents else f
        summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "no changes"
        print(f"{label}: {summary}")
        for k, v in counts.items():
            totals[k] = totals.get(k, 0) + v

    print("\nTOTALS:")
    for k, v in sorted(totals.items()):
        print(f"  {k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
