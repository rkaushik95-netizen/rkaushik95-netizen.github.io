"""Synthetic educational evaluation. No trained model or real system."""
from pathlib import Path
import csv
rows=list(csv.DictReader((Path(__file__).resolve().parent/'data/synthetic-ai-evaluation.csv').open()))
tp=sum(r['reference_label']=='defect' and r['automated_label']=='defect' for r in rows)
fn=sum(r['reference_label']=='defect' and r['automated_label']=='clear' for r in rows)
fp=sum(r['reference_label']=='clear' and r['automated_label']=='defect' for r in rows)
tn=sum(r['reference_label']=='clear' and r['automated_label']=='clear' for r in rows)
assert (tp,fn,fp,tn)==(24,6,8,62)
print({'tp':tp,'fn':fn,'fp':fp,'tn':tn,'agreement':(tp+tn)/len(rows),'defect_recall':tp/(tp+fn),'defect_precision':tp/(tp+fp)})
