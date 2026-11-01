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
 /* points on the surface of a rounded plus made of two boxes */
 function inPlus(x,y){return (Math.abs(x)<=.55&&Math.abs(y)<=1.6)||(Math.abs(y)<=.55&&Math.abs(x)<=1.6)}
 var N=reduced?2000:5200,pos=new Float32Array(N*3),col=new Float32Array(N*3),base=new Float32Array(N*3),k=0,cA=new T.Color(0x0e7c72),cB=new T.Color(0x0a5c55),cG=new T.Color(0xc99a3b);
 while(k<N){var x=(Math.random()*2-1)*1.6,y=(Math.random()*2-1)*1.6,z=(Math.random()*2-1)*.55;if(!inPlus(x,y))continue;
  var edge=Math.min(1.6-Math.abs(x),1.6-Math.abs(y),.55-Math.abs(z),Math.abs(x)>.55?.55-Math.abs(y):9,Math.abs(y)>.55?.55-Math.abs(x):9);
  if(Math.abs(edge)>.06&&Math.random()<.9)continue;
  pos[k*3]=base[k*3]=x;pos[k*3+1]=base[k*3+1]=y;pos[k*3+2]=base[k*3+2]=z;
  var cc=Math.random()<.08?cG:(Math.random()<.5?cA:cB);col[k*3]=cc.r;col[k*3+1]=cc.g;col[k*3+2]=cc.b;k++;}
 var geo=new T.BufferGeometry();geo.setAttribute("position",new T.BufferAttribute(pos,3));geo.setAttribute("color",new T.BufferAttribute(col,3));
 var pts=new T.Points(geo,new T.PointsMaterial({size:.055,vertexColors:true,transparent:true,opacity:1}));g.add(pts);
 /* orbit ring */
 var M=900,rp=new Float32Array(M*3);for(var i=0;i<M;i++){var a=i/M*Math.PI*2,r=2.45+Math.sin(i*.7)*.04;rp[i*3]=Math.cos(a)*r;rp[i*3+1]=Math.sin(a)*r*.32;rp[i*3+2]=Math.sin(a)*r;}
 var rg=new T.BufferGeometry();rg.setAttribute("position",new T.BufferAttribute(rp,3));var ring=new T.Points(rg,new T.PointsMaterial({size:.03,color:0xc99a3b,transparent:true,opacity:.7}));
 var ringG=new T.Group();ringG.add(ring);ringG.rotation.z=.35;scene.add(ringG);
 var sat=new T.Mesh(new T.SphereGeometry(.09,20,20),new T.MeshBasicMaterial({color:0xc99a3b}));ringG.add(sat);
 var mx=0,my=0,drag=0,down=null,vis=true,last=performance.now(),t0=last;
 addEventListener("pointermove",function(e){mx=(e.clientX/innerWidth-.5);my=(e.clientY/innerHeight-.5)});
 stage.addEventListener("pointerdown",function(e){down=e.clientX});addEventListener("pointerup",function(){down=null});
 stage.addEventListener("pointermove",function(e){if(down!==null){drag+=(e.clientX-down)*.006;down=e.clientX}});
 new IntersectionObserver(function(en){vis=en[0].isIntersecting},{threshold:.02}).observe(stage);
 addEventListener("resize",function(){rd.setSize(W(),H());cam.aspect=W()/H();cam.updateProjectionMatrix()});
 (function loop(now){requestAnimationFrame(loop);if(!vis)return;var t=(now-t0)/1000;last=now;
  if(!reduced){g.rotation.y=Math.sin(t*.45)*.75+drag+mx*.5;g.rotation.x=Math.sin(t*.3)*.15+my*.35+.12;
   var p=geo.attributes.position.array;for(var j=0;j<N;j+=3){var b=j*3,w=Math.sin(t*1.6+base[b]*2+base[b+1]*2)*.025;p[b]=base[b]*(1+w);p[b+1]=base[b+1]*(1+w);}
   geo.attributes.position.needsUpdate=true;
   ring.rotation.y=-t*.25;var a=t*.6;sat.position.set(Math.cos(a)*2.45,Math.sin(a)*2.45*.32,Math.sin(a)*2.45);}
  rd.render(scene,cam)})(last);
}
})();
