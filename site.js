(function(){
var R={"nebulizer": ["nebulizer", "nebuliser"], "thermometer": ["thermometer"], "bp-apparatus": ["bp apparatus", "bp", "blood pressure", "sphygmomanometer"], "glucometer": ["glucometer", "glucose", "sugar"], "pulse-oximeter": ["pulse oximeter", "oximeter", "spo2"], "stethoscope": ["stethoscope"], "wheelchair": ["wheelchair"], "hospital-bed": ["hospital bed"], "oxygen-concentrator": ["oxygen concentrator", "oxygen"], "syringes": ["syringes", "syringe"], "iv-cannula": ["iv cannula", "cannula", "branula"], "surgical-gloves": ["surgical gloves", "gloves", "glove"], "audiometer": ["audiometer", "audiometry"], "hearing-aid": ["hearing aid", "hearing"]};
var reduced=matchMedia("(prefers-reduced-motion: reduce)").matches;
document.querySelectorAll("form[data-search]").forEach(function(f){f.addEventListener("submit",function(ev){var q=(f.item.value||"").toLowerCase().trim();if(!q)return;for(var k in R){for(var i=0;i<R[k].length;i++){if(q.indexOf(R[k][i])>-1&&q.length<=R[k][i].length+12){ev.preventDefault();location.href="/products/"+k+"/";return}}}});});
/* smooth scroll */
var lenis=null;
if(window.Lenis&&!reduced){lenis=new Lenis({lerp:.09,smoothWheel:true});(function raf(t){lenis.raf(t);requestAnimationFrame(raf)})(performance.now());}
/* progress bar, compact header, parallax orbs */
var bar=document.querySelector(".progress"),hdr=document.querySelector("header"),orbs=[].slice.call(document.querySelectorAll("[data-parallax]"));
function onScroll(y){var h=document.documentElement.scrollHeight-innerHeight;if(bar)bar.style.width=(h>0?y/h*100:0)+"%";if(hdr)hdr.classList.toggle("compact",y>40);
if(!reduced)orbs.forEach(function(o){o.style.transform="translateY("+(y*parseFloat(o.dataset.parallax)).toFixed(1)+"px)"});steps();}
var stepEls=[].slice.call(document.querySelectorAll(".band .steps li"));
function steps(){if(!stepEls.length)return;var line=innerHeight*.6;stepEls.forEach(function(li){li.classList.toggle("on",li.getBoundingClientRect().top<line)})}
if(lenis)lenis.on("scroll",function(e){onScroll(e.scroll)});else addEventListener("scroll",function(){onScroll(scrollY)},{passive:true});
onScroll(scrollY);
/* tile glow follows the pointer */
document.querySelectorAll(".tile").forEach(function(t){t.addEventListener("pointermove",function(e){var r=t.getBoundingClientRect();t.style.setProperty("--mx",(e.clientX-r.left)+"px");t.style.setProperty("--my",(e.clientY-r.top)+"px")})});
/* table of contents highlight */
var tocLinks=[].slice.call(document.querySelectorAll(".toc a"));
if(tocLinks.length&&"IntersectionObserver" in window){var heads=tocLinks.map(function(a){return document.getElementById(a.getAttribute("href").slice(1))}).filter(Boolean);
 var tio=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){tocLinks.forEach(function(a){a.classList.toggle("on",a.getAttribute("href")==="#"+en.target.id)})}})},{rootMargin:"0px 0px -70% 0px"});
 heads.forEach(function(h){tio.observe(h)});
 tocLinks.forEach(function(a){a.addEventListener("click",function(ev){var t=document.getElementById(a.getAttribute("href").slice(1));if(t&&lenis){ev.preventDefault();lenis.scrollTo(t,{offset:-96})}})});}
/* reveal */
var els=document.querySelectorAll(".reveal");
if(!("IntersectionObserver" in window)||reduced){els.forEach(function(x){x.classList.add("in")})}
else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target)}})},{rootMargin:"0px 0px -8% 0px"});els.forEach(function(x){io.observe(x)});}
/* flagship: 3D particle medical cross with orbit ring */
var stage=document.getElementById("stage");
if(stage){var c=navigator.connection||{};var ok=!c.saveData&&!/(^|-)2g$/.test(c.effectiveType||"");
 if(ok){var go=function(){var sc=document.createElement("script");sc.src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js";sc.async=true;sc.onload=init3d;document.head.appendChild(sc)};
  addEventListener("load",function(){(window.requestIdleCallback||function(f){setTimeout(f,800)})(go,{timeout:2500})});}}
function init3d(){
 if(!window.THREE)return;var T=THREE;var W=function(){return stage.clientWidth},H=function(){return stage.clientHeight};
 var rd;try{rd=new T.WebGLRenderer({antialias:true,alpha:true})}catch(e){return}
 rd.setPixelRatio(Math.min(devicePixelRatio,2));rd.setSize(W(),H());stage.insertBefore(rd.domElement,stage.firstChild);stage.classList.add("has3d");
 var scene=new T.Scene(),cam=new T.PerspectiveCamera(36,W()/H(),.1,100);cam.position.set(0,0,7.2);
 var g=new T.Group();scene.add(g);
 /* morph targets: medical cross, heart, capsule, globe */
 var N=reduced?2200:5200,cA=new T.Color(0x0e7c72),cB=new T.Color(0x0a5c55),cG=new T.Color(0xc99a3b);
 function inPlus(x,y){return (Math.abs(x)<=.55&&Math.abs(y)<=1.6)||(Math.abs(y)<=.55&&Math.abs(x)<=1.6)}
 function crossPts(){var a=new Float32Array(N*3),k=0;while(k<N){var x=(Math.random()*2-1)*1.6,y=(Math.random()*2-1)*1.6,z=(Math.random()*2-1)*.55;if(!inPlus(x,y))continue;
  var e=Math.min(1.6-Math.abs(x),1.6-Math.abs(y),.55-Math.abs(z),Math.abs(x)>.55?.55-Math.abs(y):9,Math.abs(y)>.55?.55-Math.abs(x):9);if(Math.abs(e)>.06&&Math.random()<.9)continue;
  a[k*3]=x;a[k*3+1]=y;a[k*3+2]=z;k++}return a}
 function heartPts(){var a=new Float32Array(N*3);for(var k=0;k<N;k++){var t=Math.random()*Math.PI*2,f=Math.random()<.75?1:Math.sqrt(Math.random());
  var x=16*Math.pow(Math.sin(t),3),y=13*Math.cos(t)-5*Math.cos(2*t)-2*Math.cos(3*t)-Math.cos(4*t);x*=.105*f;y*=.105*f;
  var th=.55*Math.sqrt(Math.max(0,1-f*f*.6));a[k*3]=x;a[k*3+1]=y+.25;a[k*3+2]=(Math.random()*2-1)*th}return a}
 function capsulePts(){var a=new Float32Array(N*3),r=.62,L=1.15,c=Math.cos(.75),sn=Math.sin(.75);for(var k=0;k<N;k++){var u=Math.random()*2-1,ph=Math.random()*Math.PI*2,x,y,z;
  if(Math.random()<.62){y=u*L;x=Math.cos(ph)*r;z=Math.sin(ph)*r}else{var v=Math.random()*Math.PI/2,s2=u<0?-1:1;x=Math.cos(ph)*Math.cos(v)*r;z=Math.sin(ph)*Math.cos(v)*r;y=s2*(L+Math.sin(v)*r)}
  a[k*3]=x*c-y*sn;a[k*3+1]=x*sn+y*c;a[k*3+2]=z}return a}
 function globePts(){var a=new Float32Array(N*3),R=1.75;for(var k=0;k<N;k++){var y=1-k/(N-1)*2,r=Math.sqrt(1-y*y),th=k*2.39996;a[k*3]=Math.cos(th)*r*R;a[k*3+1]=y*R;a[k*3+2]=Math.sin(th)*r*R}return a}
 var shapes=[crossPts(),heartPts(),capsulePts(),globePts()];
 var pos=new Float32Array(shapes[0]),col=new Float32Array(N*3);
 for(var k=0;k<N;k++){var cc=Math.random()<.08?cG:(Math.random()<.5?cA:cB);col[k*3]=cc.r;col[k*3+1]=cc.g;col[k*3+2]=cc.b}
 var geo=new T.BufferGeometry();geo.setAttribute("position",new T.BufferAttribute(pos,3));geo.setAttribute("color",new T.BufferAttribute(col,3));
 var pts=new T.Points(geo,new T.PointsMaterial({size:.05,vertexColors:true,transparent:true,opacity:1}));g.add(pts);
 /* orbit ring */
 var M=900,rp=new Float32Array(M*3);for(var i=0;i<M;i++){var an=i/M*Math.PI*2,rr=2.45+Math.sin(i*.7)*.04;rp[i*3]=Math.cos(an)*rr;rp[i*3+1]=Math.sin(an)*rr*.32;rp[i*3+2]=Math.sin(an)*rr}
 var rg=new T.BufferGeometry();rg.setAttribute("position",new T.BufferAttribute(rp,3));var ring=new T.Points(rg,new T.PointsMaterial({size:.03,color:0xc99a3b,transparent:true,opacity:.7}));
 var ringG=new T.Group();ringG.add(ring);ringG.rotation.z=.35;scene.add(ringG);
 var sat=new T.Mesh(new T.SphereGeometry(.09,20,20),new T.MeshBasicMaterial({color:0xc99a3b}));ringG.add(sat);
 var mx=0,my=0,drag=0,down=null,vis=true,last=performance.now(),t0=last,HOLD=3.6,MORPH=1.7;
 addEventListener("pointermove",function(e){mx=(e.clientX/innerWidth-.5);my=(e.clientY/innerHeight-.5)});
 stage.addEventListener("pointerdown",function(e){down=e.clientX});addEventListener("pointerup",function(){down=null});
 stage.addEventListener("pointermove",function(e){if(down!==null){drag+=(e.clientX-down)*.006;down=e.clientX}});
 new IntersectionObserver(function(en){vis=en[0].isIntersecting},{threshold:.02}).observe(stage);
 addEventListener("resize",function(){rd.setSize(W(),H());cam.aspect=W()/H();cam.updateProjectionMatrix()});
 function ease(x){return x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2}
 (function loop(now){requestAnimationFrame(loop);if(!vis)return;var t=(now-t0)/1000;last=now;
  if(!reduced){g.rotation.y=Math.sin(t*.45)*.75+drag+mx*.5;g.rotation.x=Math.sin(t*.3)*.15+my*.35+.12;
   var cyc=HOLD+MORPH,n=Math.floor(t/cyc),ph=t-n*cyc,A=shapes[n%4],B=shapes[(n+1)%4],m=ph<HOLD?0:ease((ph-HOLD)/MORPH),p=geo.attributes.position.array,br=Math.sin(t*1.6);
   for(var j=0;j<N;j++){var b=j*3,w=1+Math.sin(t*1.6+j)*.012;p[b]=(A[b]+(B[b]-A[b])*m)*w;p[b+1]=(A[b+1]+(B[b+1]-A[b+1])*m)*w;p[b+2]=(A[b+2]+(B[b+2]-A[b+2])*m)*w}
   geo.attributes.position.needsUpdate=true;
   ring.rotation.y=-t*.25;var an2=t*.6;sat.position.set(Math.cos(an2)*2.45,Math.sin(an2)*2.45*.32,Math.sin(an2)*2.45);}
 rd.render(scene,cam)})(last);
}
})();
