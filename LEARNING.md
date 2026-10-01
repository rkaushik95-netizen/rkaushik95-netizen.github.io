# How to explain the work

Quality uses 1,200 synthetic audits, random seed 41. Resolution defects are 132 / 346 failed audits (38.2%). Failures are 346 / 1,200 audits (28.8%). Those denominators answer different questions. These patterns are illustrative, not a team's actual performance. Coaching is a hypothesis, not a proven improvement.

Retail uses the original UCI Online Retail Excel. Install pandas and openpyxl, then run `python retail-analysis.py --retail /path/to/Online\ Retail.xlsx` from the website folder.

- Invoice numbers stay as text to preserve the cancellation prefix C.
- Deduplication is a modeling choice. Compare results with and without it before an operational decision.
- Quantity times UnitPrice gives sales-line value, not profit or net accounting revenue.
- Positive sale lines exclude C invoices, non-positive quantities and non-positive prices.
- December 2011 has only nine days, so the complete-month comparison ends in November.
- Missing customer IDs remain for aggregate sales, but require separate treatment for customer segmentation.
- One year's observations cannot establish stable seasonality or causation.

Outputs are in results.json and the aggregate CSVs. Website text is static; re-check it if the script or source changes. Studies were prepared with assistance for this portfolio. Review and learn the method before an interview; do not claim unaided coding, a workplace deployment or real business impact.
