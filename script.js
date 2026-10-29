
(function(){var q=document.getElementById("q");if(!q)return;
var cards=[].slice.call(document.querySelectorAll("#list .card")),chips=document.querySelectorAll("#chips button"),none=document.getElementById("none"),cat="";
function run(){var t=q.value.toLowerCase().trim(),n=0;cards.forEach(function(c){var ok=(!cat||c.dataset.cat===cat)&&(!t||c.textContent.toLowerCase().indexOf(t)>-1);c.hidden=!ok;if(ok)n++});none.hidden=n>0}
q.addEventListener("input",run);
chips.forEach(function(b){b.addEventListener("click",function(){cat=b.dataset.c;chips.forEach(function(x){x.classList.toggle("on",x===b)});run()})});
var p=new URLSearchParams(location.search).get("q");if(p){q.value=p;run()}})();
