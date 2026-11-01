(function(){
var R={"nebulizer": ["nebulizer", "nebuliser"], "thermometer": ["thermometer"], "bp-apparatus": ["bp apparatus", "bp", "blood pressure", "sphygmomanometer"], "glucometer": ["glucometer", "glucose", "sugar"], "pulse-oximeter": ["pulse oximeter", "oximeter", "spo2"], "stethoscope": ["stethoscope"], "wheelchair": ["wheelchair"], "hospital-bed": ["hospital bed"], "oxygen-concentrator": ["oxygen concentrator", "oxygen"], "syringes": ["syringes", "syringe"], "iv-cannula": ["iv cannula", "cannula", "branula"], "surgical-gloves": ["surgical gloves", "gloves", "glove"], "audiometer": ["audiometer", "audiometry"], "hearing-aid": ["hearing aid", "hearing"]};
document.querySelectorAll("form[data-search]").forEach(function(f){f.addEventListener("submit",function(ev){var q=(f.item.value||"").toLowerCase().trim();if(!q)return;for(var k in R){for(var i=0;i<R[k].length;i++){if(q.indexOf(R[k][i])>-1&&q.length<=R[k][i].length+12){ev.preventDefault();location.href="/products/"+k+"/";return}}}});});
var els=document.querySelectorAll(".reveal");
if(!("IntersectionObserver" in window)||matchMedia("(prefers-reduced-motion: reduce)").matches){els.forEach(function(x){x.classList.add("in")});return}
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target)}})},{rootMargin:"0px 0px -8% 0px"});
els.forEach(function(x){io.observe(x)});
})();
