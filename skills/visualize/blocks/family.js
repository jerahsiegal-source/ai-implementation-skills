// Prototype chrome: switch formats and looks. The look is remembered per viewer.
(function(){
  const formats=[["project.html","Combined"],["health-brief.html","Health Brief"],["pulse-board.html","Pulse Board"],["insight-tabs.html","Insight Tabs"],["margin-notes.html","Margin Notes"],["mission-map.html","Mission Map"],["decision-desk.html","Decision Desk"]];
  const looks=[["paper","Paper"],["studio","Studio"],["night","Night"]];
  const proto=document.documentElement.hasAttribute("data-proto");
  let look=document.documentElement.dataset.look||"studio";if(proto)try{look=localStorage.getItem("viz-look3")||look}catch(e){}
  if(location.hash.slice(1)&&looks.some(l=>l[0]===location.hash.slice(1)))look=location.hash.slice(1);
  const qs=new URLSearchParams(location.search);
  if(qs.get("look"))look=qs.get("look");
  document.documentElement.dataset.look=look;
  window.FAM={};
  if(qs.get("embed")){document.documentElement.classList.add("embed");setupDrawer();addEventListener("keydown",e=>{if(e.key==="Escape"&&window.FAM.close)window.FAM.close()});return}
  if(!proto){setupDrawer();addEventListener("keydown",e=>{if(e.key==="Escape"&&window.FAM.close)window.FAM.close()});return}
  const here=location.pathname.split("/").pop();
  const bar=document.createElement("div");bar.className="proto";
  bar.innerHTML=`<nav aria-label="Formats"><span>Format</span>${formats.map(f=>`<a href="${f[0]}" class="${f[0]===here?"on":""}">${f[1]}</a>`).join("")}</nav>
   <div class="looks" role="group" aria-label="Look"><span>Look</span>${looks.map(l=>`<button data-l="${l[0]}" class="${l[0]===look?"on":""}" aria-pressed="${l[0]===look}">${l[1]}</button>`).join("")}</div>`;
  document.body.prepend(bar);
  bar.querySelectorAll("button").forEach(b=>b.onclick=()=>{document.documentElement.dataset.look=b.dataset.l;try{localStorage.setItem("viz-look3",b.dataset.l)}catch(e){}
    bar.querySelectorAll("button").forEach(x=>{x.classList.toggle("on",x===b);x.setAttribute("aria-pressed",x===b)});window.dispatchEvent(new Event("lookchange"))});
  bar.querySelectorAll("nav a").forEach(a=>a.addEventListener("click",()=>{a.href=a.getAttribute("href").split("#")[0]+"#"+document.documentElement.dataset.look}));
  setupDrawer();
  function setupDrawer(){window.FAM.openDrawer=function(html){let d=document.querySelector(".drawer");if(!d){d=document.createElement("aside");d.className="drawer";d.setAttribute("aria-label","Detail");document.body.append(d)}
    d.innerHTML=`<button class="x" aria-label="Close detail"><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4.5 4.5l7 7M11.5 4.5l-7 7"/></svg></button>`+html;
    let sc=document.querySelector(".scrim");if(!sc){sc=document.createElement("div");sc.className="scrim";document.body.append(sc)}
    const close=()=>{d.classList.remove("open");sc.classList.remove("open");window.dispatchEvent(new Event("drawerclose"))};sc.onclick=close;window.FAM.close=close;
    d.classList.add("open");sc.classList.add("open");d.querySelector(".x").onclick=close;d.querySelector(".x").focus()}}
  addEventListener("keydown",e=>{if(e.key==="Escape"&&window.FAM.close)window.FAM.close()});
})();
