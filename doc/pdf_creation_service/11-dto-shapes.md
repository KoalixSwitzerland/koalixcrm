# DTO Shapes — stage 1 sketch

Sketches of the JSON the Java worker expects from Django. **These are
anchors, not final.** Stage 1 (nested serializers) will refine field names
and pagination exactly; each `XmlBuilder<T>` in stage 3 consumes the final
shape verbatim.

Conventions:

- All DTOs are JSON objects, no XML anywhere.
- Nested objects are embedded inline (the worker should not need follow-up
  round trips for rendering).
- Foreign-key fields that are **not** needed for rendering stay as bare IDs.
- Dates: ISO-8601 (`YYYY-MM-DD`). Datetimes: RFC 3339 UTC.
- Money: decimal strings (`"123.45"`), not floats. Currency is a sibling
  field (`"CHF"`).

## `PdfExportProcessDto`

Used for `GET /api/pdf-export-processes/{id}/` and
`PATCH /api/pdf-export-processes/{id}/`.

```json
{
  "id": 42,
  "source_model": "Invoice",
  "source_id": 17,
  "template_set": 3,
  "triggered_by": 5,
  "status": "processing",
  "result_url": "",
  "error_message": "",
  "created_at": "2026-04-16T12:34:56Z",
  "updated_at": "2026-04-16T12:35:10Z"
}
```

Writable via PATCH: `status`, `result_url`, `error_message` only.

## `DocumentTemplateDto`

Used for `GET /api/document-templates/{id}/`. Asset URLs are sub-resources,
not embedded, because they need to be short-lived presigned URLs.

```json
{
  "id": 3,
  "title": "Default Invoice Template",
  "xsl_href": "/api/document-templates/3/xsl/",
  "fop_config_href": "/api/document-templates/3/fop-config/",
  "logo_href": "/api/document-templates/3/logo/"
}
```

`GET {xsl_href}` → `302 Location: <presigned S3 URL>` (short TTL, e.g. 5 min).
Same for `fop_config_href` and `logo_href`. If the optional field
(`fop_config`, `logo`) is absent, the endpoint returns `404`.

## `CommercialDocumentMediaDto`

Created by the worker with `POST /api/commercial-document-media/`. Returned
by GET.

```json
{
  "id": 101,
  "commercial_document": 17,
  "pdf_export_process": 42,
  "s3_url": "https://koalixcrm-pdf-exports.s3.eu-west-3.amazonaws.com/pdf-exports/Invoice_17_42.pdf",
  "s3_key": "pdf-exports/Invoice_17_42.pdf",
  "status": "completed",
  "media_type": "application/pdf",
  "created_by": 5,
  "created_at": "2026-04-16T12:35:09Z"
}
```

## `UserDto` (minimal)

Referenced from `triggered_by`, `created_by` and the user-extension aggregate.

```json
{
  "id": 5,
  "username": "a.riedener",
  "first_name": "Aaron",
  "last_name": "Riedener",
  "email": "a.riedener@example.com"
}
```

## `UserExtensionDto`

Referenced by the worker while assembling the XSL-FO document. Shape
reflects whatever the current Django `UserExtension.serialize_to_xml()`
produces (to be confirmed in stage 1 by reading the existing serializer /
model; stub here).

```json
{
  "id": 7,
  "user": { "…UserDto fields…" },
  "default_template_set": 3,
  "defaultCurrency": "CHF",
  "defaultCustomer": 42,
  "defaultDistributor": 5,
  "defaultSupplier": 9,
  "company": {
    "id": 1,
    "name": "Koalix Switzerland AG",
    "postal_address": { "…PostalAddressDto…" },
    "default_currency": "CHF"
  }
}
```

## `InvoiceDto` (deeply nested — the worker's main input)

The template `{Quote,DeliveryNote,PurchaseOrder,PurchaseConfirmation,
PaymentReminder,CreditNote}Dto` mirrors this shape with type-specific fields
added / removed. Field names follow the existing Python serializers where
they exist.

```json
{
  "id": 17,
  "type": "Invoice",
  "contract": 12,
  "customer": {
    "id": 42,
    "name": "ACME SA",
    "default_currency": "CHF",
    "postal_addresses": [ { "…PostalAddressDto…", "is_default": true } ],
    "phone_addresses":  [ { "…PhoneAddressDto…",  "is_default": true } ],
    "email_addresses":  [ { "…EmailAddressDto…",  "is_default": true } ]
  },
  "contact_person": { "…PersonDto…" },
  "currency": "CHF",
  "date_of_creation": "2026-04-16",
  "last_pricing_date": "2026-04-16",
  "status": "sent",
  "discount": "0.00",
  "last_calculated_price": "1234.56",
  "last_calculated_tax": "95.00",
  "custom_payment_terms": null,
  "payable_until": "2026-05-16",
  "items": [
    {
      "id": 201,
      "position_number": 10,
      "product_type": {
        "id": 301,
        "title": "Consulting hour",
        "description": "…",
        "product_type_identifier": "CONS-H",
        "tariff": { "id": 1, "rate": "8.1" }
      },
      "description_override": null,
      "quantity": "10.00",
      "unit": "h",
      "unit_price": "120.00",
      "discount": "0.00",
      "position_total_without_tax": "1200.00",
      "position_tax": "97.20",
      "position_total_with_tax": "1297.20"
    }
  ],
  "tax_summary": [
    { "rate": "8.1", "taxable_amount": "1200.00", "tax_amount": "97.20" }
  ],
  "user_extension": { "…UserExtensionDto…" },
  "template_set": 3
}
```

### Type-specific hints

| Type | Notes |
| --- | --- |
| `Quote` | include `valid_until`, no `payable_until`. |
| `DeliveryNote` | tax/price fields usually absent; include `date_of_delivery`. |
| `PurchaseOrder` | `supplier` instead of `customer`. |
| `PurchaseConfirmation` | `customer` present; `confirmed_delivery_date`. |
| `PaymentReminder` | include `reminder_level`, `original_invoice` ref, `outstanding_amount`. |
| `CreditNote` | include `original_invoice` ref, `reason`. |

## Open items for stage 1

- [ ] Confirm exact field names against current Python serializers
      (`koalixcrm/contracts/serializers/*.py` and
      `koalixcrm/contacts/serializers/*.py`) — prefer existing names over
      reinventing.
- [ ] Decide whether nested objects get their own `endpoint` (for POST/PATCH
      of nested children) or are read-only snapshots inside the parent DTO.
      For this migration, **read-only embedded is enough** — the worker only
      reads.
- [ ] Pin the `tax_summary` shape — currently computed on the fly in
      `CommercialDocument.serialize_to_xml`. Either compute it in the
      Django serializer (preferred — data is already loaded) or compute it
      in Java from `items`. Decide in stage 1.
- [ ] Pagination: worker only GETs by id, so default DRF pagination is fine
      and not an issue.
