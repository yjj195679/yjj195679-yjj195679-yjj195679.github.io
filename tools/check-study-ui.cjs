/* Minimal static UI checks; no dependencies or external credentials. */
"use strict";
const fs=require("node:fs");
const path=require("node:path");
const vm=require("node:vm");
const root=path.resolve(__dirname,"..");
const read=p=>fs.readFileSync(path.join(root,p),"utf8");
const exists=p=>fs.existsSync(path.join(root,p));
let checks=0;
const test=(message,condition)=>{checks++;if(!condition)throw Error(message)};
const targets=[
 "index.html","courses.html","writing-vocabulary.html","math-formulas.html",
 "projects.html","education.html","achievements.html","life.html","guestbook.html",
 "en/index.html","en/courses.html","en/projects.html","en/education.html",
 "en/achievements.html","en/life.html","en/guestbook.html"
];
for(const p of targets){
 const html=read(p);
 const ids=[...html.matchAll(/\bid=["']([^"']+)["']/g)].map(x=>x[1]);
 test(p+": duplicate ids",new Set(ids).size===ids.length);
 for(const m of html.matchAll(/\b(?:href|src)=["']([^"']+)["']/g)){
  const url=m[1];
  if(/^(https?:|mailto:|tel:|data:|javascript:|blob:)/i.test(url))continue;
  if(url.startsWith("#")){
    if(url.length>1)test(p+": missing #anchor "+url,ids.includes(decodeURIComponent(url.slice(1))));
    continue;
  }
  const clean=url.split(/[?#]/)[0];
  if(!clean)continue;
  const file=path.normalize(path.join(clean.startsWith("/")?"":path.dirname(p),clean.replace(/^\//,""))).replaceAll("\\","/");
  test(p+": missing local resource "+url,exists(file)||exists(file+"/index.html"));
 }
}
const vocabulary=read("writing-vocabulary.html");
test("writing cards should remain 68",(vocabulary.match(/class="writing-entry glass"/g)||[]).length===68);
test("cloud sync status missing",vocabulary.includes('id="writing-sync-status"'));
const jsFiles=["js/main.js","js/408-simulations.js","js/writing-vocabulary.js"];
for(const p of jsFiles){
 new vm.Script(read(p),{filename:p});
 test(p+" compiles",true);
}
const sim=read("js/408-simulations.js");
test("special simulation render must be guarded",sim.includes("Array.isArray(step.values)&&Array.isArray(step.positions)"));
test("circle simulation sizing missing",read("css/408-handbook.css").includes(".bfs-node{height:60px"));
test("vocabulary print CSS contains escaped newline bug",!read("css/vocabulary.css").includes("\\n  .js-ready"));
const main=read("js/main.js");
const match=main.match(/const publishedPdfNames\s*=\s*new Set\(\[([\s\S]*?)\]\);/);
test("PDF existence guard missing",!!match);
const pdfNames=JSON.parse("["+match[1]+"]");
for(const name of pdfNames)test("missing generated PDF: "+name,exists("documents/exports/"+name+".pdf"));
const schema=read("supabase/writing_word_progress.sql");
test("RLS migration missing",schema.includes("enable row level security")&&schema.includes("revoke all"));
test("Edge function missing",exists("supabase/functions/writing-progress/index.ts"));
console.log("PASS: "+checks+" static UI, SVG simulation, PDF and cookie-sync checks");
