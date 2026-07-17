import gzip,csv,glob,os
from multiprocessing import Pool
def p(f):
 r=[]
 with gzip.open(f,'rt') as g:
  l=g.readline()
  while l[0]=='#':l=g.readline()
  for w in csv.reader(g):
   b=[float(x) for x in w[11][1:-1].split(',') if x!='NaN']
   s=[float(x) for x in w[16][1:-1].split(',') if x!='NaN']
   if not b or not s:continue
   n,x,m,y=min(b),max(b),min(s),max(s)
   v=max((x-n)/n*100,(y-m)/m*100)
   if v>100:r.append(f'{w[1]},{n},{x},{m},{y},{v}')
 return r
if __name__=='__main__':
 os.makedirs('/home/irisowner/dev/data/out',exist_ok=True)
 with open('/home/irisowner/dev/data/out/result.csv','w') as o:
  o.write('source_id,bp_min_flux,bp_max_flux,rp_min_flux,rp_max_flux,percentage_change\n')
  [o.write('\n'.join(b)+'\n') for b in Pool().map(p,glob.glob('/home/irisowner/dev/data/in/*.csv.gz')) if b]