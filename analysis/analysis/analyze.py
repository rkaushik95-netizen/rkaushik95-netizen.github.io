"""Reproduce two portfolio studies. Run with Python 3, pandas and openpyxl.
Retail input: UCI Online Retail.xlsx. Quality data: deliberately synthetic.
No claim of business impact or causation is made.
"""
from pathlib import Path
import json, random, argparse, hashlib
import pandas as pd
P=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(); parser.add_argument('--retail', required=True); args=parser.parse_args()
df=pd.read_excel(args.retail, dtype={'InvoiceNo':str,'StockCode':str})
raw=len(df); duplicate=int(df.duplicated().sum()); d=df.drop_duplicates().copy()
d['InvoiceNo']=d['InvoiceNo'].fillna(''); d['value']=d.Quantity*d.UnitPrice
cancel=d.InvoiceNo.str.upper().str.startswith('C'); positive=(~cancel)&(d.Quantity>0)&(d.UnitPrice>0)
s=d[positive].copy(); s['month']=s.InvoiceDate.dt.strftime('%Y-%m')
full=s[(s.InvoiceDate>='2011-01-01')&(s.InvoiceDate<'2011-12-01')]
monthly=full.groupby('month').agg(value=('value','sum'),lines=('value','size')).reset_index()
countries=full.groupby('Country').agg(value=('value','sum'),lines=('value','size')).sort_values('value',ascending=False).reset_index()
negative=d[cancel&(d.Quantity<0)&(d.UnitPrice>0)]
retail={'raw_rows':raw,'duplicates':duplicate,'unique_rows':len(d),'sale_lines':len(s),'excluded':len(d)-len(s),'cancel_lines':int(cancel.sum()),'missing_customer':int(d.CustomerID.isna().sum()),'sales_value':round(float(s.value.sum()),2),'cancel_value':round(float(-negative.value.sum()),2),'period':'1 Dec 2010 - 9 Dec 2011','full_month_total':round(float(full.value.sum()),2),'full_month_lines':len(full),'monthly':monthly.round(2).to_dict('records'),'countries':countries.head(5).round(2).to_dict('records'),'input_sha256':hashlib.sha256(Path(args.retail).read_bytes()).hexdigest()}
monthly.to_csv(P/'data/retail-monthly.csv',index=False); countries.to_csv(P/'data/retail-countries.csv',index=False)
random.seed(41)
rows=[]
for i in range(1200):
    channel=random.choices(['Chat','Voice','Email'],weights=[5,3,2])[0]
    issue=random.choices(['No defect','Resolution','Documentation','Process','Communication'],weights=[72,11,7,6,4])[0]
    rows.append({'audit_id':f'SYN-{i+1:04d}','channel':channel,'result':issue,'coachable':issue in ['Resolution','Documentation','Communication']})
q=pd.DataFrame(rows); q.to_csv(P/'data/synthetic-quality.csv',index=False)
f=q[q.result!='No defect']; defects=f.result.value_counts().to_dict()
quality={'audits':len(q),'failed':len(f),'passed':int((q.result=='No defect').sum()),'coachable':int(q.coachable.sum()),'defects':defects,'channels':q.groupby('channel').agg(audits=('audit_id','count'),fails=('result',lambda x:(x!='No defect').sum())).reset_index().to_dict('records')}
(P/'data/results.json').write_text(json.dumps({'retail':retail,'quality':quality},indent=2))
print(json.dumps({'retail':retail,'quality':quality},indent=2))
