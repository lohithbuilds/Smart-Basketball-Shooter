const $ = id => document.getElementById(id);
const strategy = () => $('strategy').value;
let state = null;
async function api(url, body) {
    const response = await fetch(url, {
        method: body ? 'POST' : 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
        body: body ? JSON.stringify(body) : undefined
    });

    const contentType = response.headers.get('content-type') || '';
    const responseText = await response.text();

    if (!contentType.includes('application/json')) {
        throw new Error(
            `Server returned non-JSON response (${response.status}). ` +
            responseText.slice(0, 200)
        );
    }

    let data;

    try {
        data = JSON.parse(responseText);
    } catch (error) {
        throw new Error('Invalid JSON response from server.');
    }

    if (!response.ok) {
        throw new Error(data.error || `Request failed: ${response.status}`);
    }

    return data;
}
function toast(msg){$('toast').textContent=msg;$('toast').classList.add('show');setTimeout(()=>$('toast').classList.remove('show'),2200)}
function render(s){state=s;$('points').textContent=s.total_points;$('accuracy').textContent=s.accuracy+'%';$('makes').textContent=`${s.makes} makes · ${s.misses} misses`;$('shots').textContent=s.total_shots;$('streak').textContent=s.best_streak;$('epsilon').textContent=Number(s.epsilon).toFixed(2);$('explorePct').textContent=s.exploration_pct+'%';$('exploitPct').textContent=s.exploitation_pct+'%';$('exploreBar').style.width=s.exploration_pct+'%';$('exploitBar').style.width=s.exploitation_pct+'%';
 const max=Math.max(3,...s.positions.map(p=>p.estimated_reward));$('armBars').innerHTML=s.positions.map(p=>`<div class="arm-row"><span class="name">${p.name}</span><div class="bar-bg"><div class="bar-fill" style="width:${Math.max(0,p.estimated_reward)/max*100}%"></div></div><span class="val">${p.estimated_reward.toFixed(2)}</span></div>`).join('');
 $('log').innerHTML=s.history.length?s.history.slice().reverse().map(h=>`<div class="log-item"><span>${h.shot}. ${h.position} <small>(${h.decision})</small></span><span class="${h.made?'made':'missed'}">${h.made?'MADE +'+h.reward:'MISSED'}</span></div>`).join(''):'<p class="empty">Your agent\'s decisions will appear here.</p>';
 drawChart(s.reward_history);}
function drawChart(rewards){const c=$('rewardChart'),ctx=c.getContext('2d'),w=c.clientWidth||700,h=230,dpr=window.devicePixelRatio||1;c.width=w*dpr;c.height=h*dpr;ctx.scale(dpr,dpr);ctx.clearRect(0,0,w,h);const pad={l:35,r:12,t:12,b:25},cw=w-pad.l-pad.r,ch=h-pad.t-pad.b;ctx.strokeStyle='#293b4e';ctx.fillStyle='#8fa1b5';ctx.font='10px DM Sans';for(let i=0;i<=3;i++){let y=pad.t+ch*i/3;ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(w-pad.r,y);ctx.stroke();ctx.fillText(String(3-i),8,y+3)}if(!rewards.length){ctx.fillText('Take shots to generate learning data',pad.l+10,h/2);return}const maxN=Math.max(2,rewards.length);let avg=[];for(let i=0;i<rewards.length;i++){let slice=rewards.slice(Math.max(0,i-19),i+1);avg.push(slice.reduce((a,b)=>a+b,0)/slice.length)}const line=(arr,color)=>{ctx.beginPath();arr.forEach((v,i)=>{let x=pad.l+i/(maxN-1)*cw,y=pad.t+ch-(v/3)*ch;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.strokeStyle=color;ctx.lineWidth=1.8;ctx.stroke()};line(rewards,'#ff9d45');line(avg,'#63b3ed');ctx.fillText('SHOT NUMBER',w/2-30,h-5)}
async function refresh(){try{render(await api('/api/state'))}catch(e){toast(e.message)}}
async function manualShot(pos){try{const d=await api('/api/shot',{position:pos});render(d.state);shotMessage(d.result)}catch(e){toast(e.message)}}
function shotMessage(r){$('lastShot').innerHTML=`<span class="ball">🏀</span><div><strong class="${r.made?'made':'missed'}">${r.made?'SWISH! +'+r.reward+' POINTS':'MISSED SHOT'}</strong><small>${r.position} · ${r.decision} · Estimated reward ${r.estimated_value.toFixed(2)}</small></div>`}
document.querySelectorAll('.spot').forEach(b=>b.addEventListener('click',()=>manualShot(b.dataset.position)));
$('agentBtn').addEventListener('click',async()=>{try{const d=await api('/api/agent-shot',{strategy:strategy()});render(d.state);shotMessage(d.result)}catch(e){toast(e.message)}});
$('resetBtn').addEventListener('click',async()=>{try{render(await api('/api/reset', {}));$('lastShot').innerHTML='<span class="ball">🏀</span><div><strong>New session started</strong><small>Agent estimates have been reset.</small></div>';toast('Game reset.')}catch(e){toast(e.message)}});
$('strategy').addEventListener('change',()=>toast('Strategy set to '+$('strategy').selectedOptions[0].text));
$('benchmarkBtn').addEventListener('click',async()=>{const b=$('benchmarkBtn');b.disabled=true;b.textContent='Running…';try{const d=await api('/api/benchmark');const sorted=[...d.results].sort((a,b)=>b.points-a.points);$('benchmarkResults').innerHTML=`<table class="benchmark-table"><thead><tr><th>STRATEGY</th><th>TOTAL POINTS</th><th>ACCURACY</th><th>BEST ESTIMATE</th></tr></thead><tbody>${sorted.map((r,i)=>`<tr><td class="${i===0?'winner':''}">${i===0?'🏆 ':''}${r.label}</td><td>${r.points}</td><td>${r.accuracy}%</td><td>${r.best_position.replaceAll('_',' ')}</td></tr>`).join('')}</tbody></table><p class="empty">${d.rounds.toLocaleString()} shots per strategy · identical environment seed for reproducibility. One run can vary with the seed.</p>`}catch(e){toast(e.message)}finally{b.disabled=false;b.textContent='Run benchmark'}});
window.addEventListener('resize',()=>state&&drawChart(state.reward_history));refresh();
