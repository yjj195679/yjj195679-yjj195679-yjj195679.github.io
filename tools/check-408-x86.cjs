const assert = require('node:assert/strict');
const {parseByte,calculateFlags} = require('../js/408-x86.js');
const signed=n=>n>=128?n-256:n;
assert.equal(parseByte('-128'),128);assert.equal(parseByte('0xFF'),255);
for(const v of ['256','-129','0x100','0x','', '1.5', '1e2', 'NaN']) assert.throws(()=>parseByte(v));
assert.throws(()=>calculateFlags('MUL','2','3'));
for(let a=0;a<256;++a)for(let b=0;b<256;++b){
  for(const op of ['ADD','SUB','CMP','TEST']){
    const r=calculateFlags(op,String(a),String(b));
    const raw=op==='ADD'?a+b:op==='TEST'?a&b:a-b;
    const result=((raw%256)+256)%256;
    const math=op==='ADD'?signed(a)+signed(b):signed(a)-signed(b);
    assert.equal(r.result,result);
    assert.equal(r.zf,+(result===0));assert.equal(r.sf,+(result>=128));
    assert.equal(r.cf,op==='TEST'?0:+(op==='ADD'?raw>255:raw<0));
    assert.equal(r.of,op==='TEST'?0:+(math< -128 || math>127));
    if(op==='SUB'||op==='CMP'){
      assert.equal(r.jumps.JA,a>b);assert.equal(r.jumps.JAE,a>=b);assert.equal(r.jumps.JB,a<b);assert.equal(r.jumps.JBE,a<=b);
      assert.equal(r.jumps.JG,signed(a)>signed(b));assert.equal(r.jumps.JGE,signed(a)>=signed(b));assert.equal(r.jumps.JL,signed(a)<signed(b));assert.equal(r.jumps.JLE,signed(a)<=signed(b));
    }
  }
}
let r=calculateFlags('CMP','0xFF','1');assert(r.jumps.JA&&r.jumps.JL);assert(!r.writes);
r=calculateFlags('ADD','0x7F','1');assert.equal(r.of,1);assert.equal(r.cf,0);
console.log('Passed: all 262144 byte operation pairs, four flags, signed/unsigned branches, input validation.');
