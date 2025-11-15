# Example Delivery Note Patterns

This document shows example delivery note formats that the system can extract data from.

## Example 1: Standard Delivery Note

```
DELIVERY NOTE
Bon de Livraison

Note Number: BL-2024-001
Date: 15/01/2024

FROM (Supplier):
ABC Logistics Corp.
123 Warehouse Street
75001 Paris, France

TO (Customer):
XYZ Retail Store
456 Shopping Avenue
69001 Lyon, France

Items:
- Product A x 100 units
- Product B x 50 units
- Product C x 25 units

Total Amount: 1,250.00 EUR
```

## Example 2: French Format

```
BON DE LIVRAISON

Numéro: BDL-2024-0042
Date de livraison: 20/02/2024

Fournisseur:
Société Transport Express
15 Rue de Commerce
33000 Bordeaux

Client:
Magasin Central
89 Avenue des Entreprises
44000 Nantes

Montant Total: 3,450.50 EUR
```

## Example 3: Bilingual Format

```
DELIVERY NOTE / BON DE LIVRAISON

Delivery No: DN-2024-123
Date: 2024-03-10

Supplier / Fournisseur:
Global Shipping Inc.
50 Industrial Park
Montreal, QC H1A 1A1

Customer / Client:
Tech Solutions Ltd.
75 Business Plaza
Toronto, ON M5H 2N2

Total: 2,890.00 CAD
Currency: CAD
```

## Extraction Pattern Examples

The system uses regex patterns to extract fields. Here are the patterns it looks for:

### Delivery Note Number
- `Note Number: BL-2024-001`
- `Numéro: BDL-2024-0042`
- `Delivery No: DN-2024-123`
- `Bon #: 12345`

### Date
- `Date: 15/01/2024`
- `Date de livraison: 20/02/2024`
- `Delivery Date: 2024-03-10`

### Supplier/Customer
- `FROM: Company Name`
- `Fournisseur: Company Name`
- `Supplier: Company Name`
- `TO: Company Name`
- `Client: Company Name`
- `Customer: Company Name`

### Amount
- `Total: 1,250.00 EUR`
- `Montant Total: 3,450.50 EUR`
- `Total Amount: 2,890.00 CAD`

## Tips for Document Preparation

1. Ensure text is clear and readable
2. Avoid handwritten notes if possible
3. Use standard fonts
4. Keep good contrast between text and background
5. Orient document correctly (not upside down or rotated)
