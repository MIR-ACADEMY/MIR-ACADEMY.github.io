/* MIRACDX Studio — Animation Library
   Each generator returns a self-contained JS string (no <script> tags).
   The Studio injects it into a page as <script data-mir-anim="NAME">.
   Snippets are idempotent: they reuse an existing <canvas id="mir-bg">,
   so reloading a saved file re-runs cleanly without stacking canvases. */
(function (global) {
  function hexToRgba(hex, a) {
    hex = (hex || '#000000').replace('#', '');
    if (hex.length === 3) hex = hex.split('').map(function (c) { return c + c; }).join('');
    var n = parseInt(hex, 16);
    var r = (n >> 16) & 255, g = (n >> 8) & 255, b = n & 255;
    return 'rgba(' + r + ',' + g + ',' + b + ',' + a + ')';
  }

  var CANVAS_BOOT =
    "var cv=document.getElementById('mir-bg');" +
    "if(!cv){cv=document.createElement('canvas');cv.id='mir-bg';" +
    "cv.style.cssText='position:fixed;inset:0;z-index:0;pointer-events:none';" +
    "document.body.insertBefore(cv,document.body.firstChild);}" +
    "if(cv.__mirStop){cv.__mirStop();}" +
    "var x=cv.getContext('2d'),W,H,raf;";

  var SNIPPETS = {
    none: function () {
      return "(function(){var cv=document.getElementById('mir-bg');" +
        "if(cv){if(cv.__mirStop)cv.__mirStop();cv.parentNode.removeChild(cv);}})();";
    },

    datarain: function (c) {
      var c1 = hexToRgba(c.gold2 || '#e2c48a', 0.95);
      var c2 = hexToRgba(c.teal || '#7ad9c8', 0.25);
      var bg = hexToRgba(c.bg || '#050505', 0.08);
      return "(function(){" + CANVAS_BOOT +
        "var cols,drops,FS=16," +
        "glyphs='01<>{}[]/=+*MIRACDEMY\\u30A2\\u30AB\\u30C7\\u30DF\\u30FC10110100';" +
        "function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight;cols=Math.floor(W/FS);" +
        "drops=Array(cols).fill(0).map(function(){return Math.random()*-50;});}" +
        "function step(){x.fillStyle='" + bg + "';x.fillRect(0,0,W,H);x.font=FS+'px monospace';" +
        "for(var i=0;i<cols;i++){var ch=glyphs[Math.floor(Math.random()*glyphs.length)];var y=drops[i]*FS;" +
        "x.fillStyle='" + c1 + "';x.fillText(ch,i*FS,y);" +
        "x.fillStyle='" + c2 + "';x.fillText(glyphs[Math.floor(Math.random()*glyphs.length)],i*FS,y-FS);" +
        "if(y>H&&Math.random()>.975)drops[i]=0;drops[i]+=0.55;}raf=requestAnimationFrame(step);}" +
        "addEventListener('resize',rs);rs();step();" +
        "cv.__mirStop=function(){cancelAnimationFrame(raf);removeEventListener('resize',rs);};})();";
    },

    neural: function (c) {
      var node = hexToRgba(c.gold || '#c8a96e', 0.9);
      var glow = hexToRgba(c.gold || '#c8a96e', 0.08);
      var edge = (c.teal || '#7ad9c8');
      var sig = hexToRgba(c.gold2 || '#e2c48a', 1);
      return "(function(){" + CANVAS_BOOT +
        "var nodes,signals,LINK=130;" +
        "function init(){var n=Math.min(90,Math.floor(W*H/16000));nodes=[];" +
        "for(var i=0;i<n;i++)nodes.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.35,vy:(Math.random()-.5)*.35,r:Math.random()*1.6+1});signals=[];}" +
        "function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight;init();}" +
        "function step(){x.clearRect(0,0,W,H);" +
        "for(var i=0;i<nodes.length;i++){for(var j=i+1;j<nodes.length;j++){var a=nodes[i],b=nodes[j],d=Math.hypot(a.x-b.x,a.y-b.y);" +
        "if(d<LINK){var o=(1-d/LINK)*.32;" +
        "x.strokeStyle=" + JSON.stringify(edge) + ";x.globalAlpha=o;x.lineWidth=.6;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke();x.globalAlpha=1;" +
        "if(Math.random()<0.0009)signals.push({a:a,b:b,t:0});}}}" +
        "for(var k=signals.length-1;k>=0;k--){var s=signals[k];s.t+=.025;if(s.t>=1){signals.splice(k,1);continue;}" +
        "var px=s.a.x+(s.b.x-s.a.x)*s.t,py=s.a.y+(s.b.y-s.a.y)*s.t;x.fillStyle='" + sig + "';x.globalAlpha=1-Math.abs(s.t-.5)*2;x.beginPath();x.arc(px,py,2.4,0,7);x.fill();x.globalAlpha=1;}" +
        "for(var m=0;m<nodes.length;m++){var p=nodes[m];p.x+=p.vx;p.y+=p.vy;if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;" +
        "x.fillStyle='" + node + "';x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fill();" +
        "x.fillStyle='" + glow + "';x.beginPath();x.arc(p.x,p.y,p.r*4,0,7);x.fill();}raf=requestAnimationFrame(step);}" +
        "addEventListener('resize',rs);rs();step();" +
        "cv.__mirStop=function(){cancelAnimationFrame(raf);removeEventListener('resize',rs);};})();";
    },

    particles: function (c) {
      var dot = hexToRgba(c.gold2 || '#e2c48a', 0.85);
      var g0 = c.gold || '#c8a96e', g1 = c.teal || '#7ad9c8';
      return "(function(){" + CANVAS_BOOT +
        "var P,mouse={x:-999,y:-999},LINK=120;" +
        "function init(){var n=Math.min(140,Math.floor(W*H/11000));P=[];" +
        "for(var i=0;i<n;i++)P.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.5,vy:(Math.random()-.5)*.5,r:Math.random()*1.4+.6});}" +
        "function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight;init();}" +
        "addEventListener('mousemove',function(e){mouse.x=e.clientX;mouse.y=e.clientY;});" +
        "function step(){x.clearRect(0,0,W,H);" +
        "for(var i=0;i<P.length;i++){for(var j=i+1;j<P.length;j++){var a=P[i],b=P[j],d=Math.hypot(a.x-b.x,a.y-b.y);" +
        "if(d<LINK){var o=(1-d/LINK)*.5;var gr=x.createLinearGradient(a.x,a.y,b.x,b.y);" +
        "gr.addColorStop(0," + JSON.stringify(g0) + ");gr.addColorStop(1," + JSON.stringify(g1) + ");" +
        "x.strokeStyle=gr;x.globalAlpha=o;x.lineWidth=.5;x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke();x.globalAlpha=1;}}}" +
        "for(var m=0;m<P.length;m++){var p=P[m];var mdx=p.x-mouse.x,mdy=p.y-mouse.y,md=Math.hypot(mdx,mdy);" +
        "if(md<140){p.vx+=mdx/md*.06;p.vy+=mdy/md*.06;}p.vx*=.985;p.vy*=.985;p.x+=p.vx;p.y+=p.vy;" +
        "if(p.x<0||p.x>W)p.vx*=-1;if(p.y<0||p.y>H)p.vy*=-1;p.x=Math.max(0,Math.min(W,p.x));p.y=Math.max(0,Math.min(H,p.y));" +
        "x.fillStyle='" + dot + "';x.beginPath();x.arc(p.x,p.y,p.r,0,7);x.fill();}raf=requestAnimationFrame(step);}" +
        "addEventListener('resize',rs);rs();step();" +
        "cv.__mirStop=function(){cancelAnimationFrame(raf);removeEventListener('resize',rs);};})();";
    },

    grid: function (c) {
      var horiz = c.gold || '#c8a96e', vert = c.teal || '#7ad9c8';
      var glow = hexToRgba(c.gold || '#c8a96e', 0.18);
      return "(function(){" + CANVAS_BOOT +
        "var t=0;function rs(){W=cv.width=innerWidth;H=cv.height=innerHeight;}" +
        "function step(){x.fillStyle='" + (c.bg || '#050505') + "';x.fillRect(0,0,W,H);" +
        "var hz=H*0.5,vp=W/2,spacing=46,depth=22;" +
        "for(var i=0;i<depth;i++){var p=((i+(t*0.6)%1)/depth);var y=hz+Math.pow(p,2.2)*(H-hz);var o=(1-p)*.5;" +
        "x.strokeStyle=" + JSON.stringify(horiz) + ";x.globalAlpha=o*0.7;x.lineWidth=1;x.beginPath();x.moveTo(0,y);x.lineTo(W,y);x.stroke();x.globalAlpha=1;}" +
        "var lines=26;for(var k=-lines;k<=lines;k++){var fx=vp+k*spacing;var o2=Math.max(0,1-Math.abs(k)/lines)*.5;" +
        "x.strokeStyle=" + JSON.stringify(vert) + ";x.globalAlpha=o2;x.lineWidth=1;x.beginPath();x.moveTo(vp+k*8,hz);x.lineTo(fx,H);x.stroke();x.globalAlpha=1;}" +
        "var g=x.createLinearGradient(0,hz-60,0,hz+60);g.addColorStop(0,'rgba(0,0,0,0)');g.addColorStop(.5,'" + glow + "');g.addColorStop(1,'rgba(0,0,0,0)');" +
        "x.fillStyle=g;x.fillRect(0,hz-60,W,120);t+=0.016;raf=requestAnimationFrame(step);}" +
        "addEventListener('resize',rs);rs();step();" +
        "cv.__mirStop=function(){cancelAnimationFrame(raf);removeEventListener('resize',rs);};})();";
    }
  };

  global.MIRAnim = {
    names: ['none', 'datarain', 'neural', 'particles', 'grid'],
    labels: { none: 'None', datarain: 'Data Rain', neural: 'Neural Network', particles: 'Particles', grid: 'Infinite Grid' },
    snippet: function (name, colors) {
      var gen = SNIPPETS[name] || SNIPPETS.none;
      return gen(colors || {});
    }
  };
})(window);
