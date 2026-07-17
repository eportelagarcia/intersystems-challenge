import gzip,csv,glob,os,io,multiprocessing
from concurrent.futures import ProcessPoolExecutor

def p(f):
 r=[]
 with open(f,'rb') as fh:raw=gzip.decompress(fh.read())
 sio=io.StringIO(raw.decode('utf-8'))
 line=sio.readline()
 while line and line[0]=='#':line=sio.readline()
 for w in csv.reader(sio):
  b_str=w[11][1:-1];s_str=w[16][1:-1]
  if not b_str or not s_str:continue
  b_min=float('inf');b_max=float('-inf');has_b=False
  for x in b_str.split(','):
   if x and x!='NaN':v=float(x);b_min=min(b_min,v);b_max=max(b_max,v);has_b=True
  if not has_b:continue
  s_min=float('inf');s_max=float('-inf');has_s=False
  for x in s_str.split(','):
   if x and x!='NaN':v=float(x);s_min=min(s_min,v);s_max=max(s_max,v);has_s=True
  if not has_s:continue
  pct=max((b_max-b_min)/b_min*100,(s_max-s_min)/s_min*100)
  if pct>100:r.append(f'{w[1]},{b_min},{b_max},{s_min},{s_max},{pct}')
 return r

def main():
 os.makedirs('/home/irisowner/dev/data/out',exist_ok=True)
 files=glob.glob('/home/irisowner/dev/data/in/*.csv.gz')
 with open('/home/irisowner/dev/data/out/result.csv','w') as o:
  o.write('source_id,bp_min_flux,bp_max_flux,rp_min_flux,rp_max_flux,percentage_change\n')
  with ProcessPoolExecutor(mp_context=multiprocessing.get_context('spawn')) as ex:
   for b in ex.map(p,files):
    if b:o.write('\n'.join(b)+'\n')

if __name__=='__main__':
 main()
