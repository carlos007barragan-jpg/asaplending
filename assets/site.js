/* ASAP Lending — site behavior: nav, lead forms, calculators, application wizard */
(function(){
  var ES = document.documentElement.lang === 'es';
  var API = 'https://zfflgvjnkcjnbwydurlp.supabase.co/functions/v1/public';
  var PHONE = '(913) 513-2656';
  var T = ES ? {
    sending:'Enviando…', ok:'Recibido. Una persona de nuestro equipo le llamará pronto.',
    err:'No se pudo enviar desde aquí. Llame o envíe un texto al '+PHONE+'.',
    strong:'sólido', works:'funciona', thin:'ajustado', next:'Continuar', req:'Complete los campos marcados antes de continuar.'
  } : {
    sending:'Sending…', ok:'Received. A decision-maker on our team will call you shortly.',
    err:'That did not send from here. Call or text '+PHONE+'.',
    strong:'strong', works:'works', thin:'thin', next:'Continue', req:'Fill in the marked fields before you continue.'
  };
  function $(id){return document.getElementById(id)}
  function money(n){n=Math.round(n||0);return (n<0?'-$':'$')+Math.abs(n).toLocaleString('en-US')}
  function val(id){var e=$(id);return e?(parseFloat(String(e.value).replace(/[^0-9.\-]/g,''))||0):0}

  var y=$('yr'); if(y) y.textContent=new Date().getFullYear();

  /* nav */
  var b=document.querySelector('.burger');
  if(b) b.addEventListener('click',function(){var o=document.body.classList.toggle('navopen');b.setAttribute('aria-expanded',o?'true':'false')});

  /* lead forms */
  function post(form,data,msgEl,btn){
    var label=btn.textContent; btn.disabled=true; btn.textContent=T.sending;
    msgEl.className='fmsg';
    fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
      .then(function(r){if(!r.ok) throw new Error(r.status);return r.json()})
      .then(function(){msgEl.textContent=T.ok;msgEl.className='fmsg ok';form.reset();btn.style.display='none'})
      .catch(function(){msgEl.textContent=T.err;msgEl.className='fmsg err';btn.disabled=false;btn.textContent=label});
  }
  document.querySelectorAll('form[data-lead]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var d={}; new FormData(f).forEach(function(v,k){d[k]=v});
      var extra=[]; ['state','address'].forEach(function(k){if(d[k]){extra.push(k+': '+d[k]);delete d[k]}});
      if(extra.length) d.msg=(extra.join(' · ')+(d.msg?'\n'+d.msg:''));
      d.source='ASAP Lending — '+f.getAttribute('data-lead')+(ES?' (ES)':'');
      d.page=location.pathname;
      post(f,d,f.querySelector('.fmsg'),f.querySelector('button[type=submit]'));
    });
  });

  /* flip deal calculator */
  if($('fc-buy')){
    var fc=function(){
      var buy=val('fc-buy'),rehab=val('fc-rehab'),arv=val('fc-arv'),mo=val('fc-mo'),rate=val('fc-rate')/100,pts=val('fc-pts')/100,down=val('fc-down')/100,sell=val('fc-sell')/100;
      var cost=buy+rehab, loan=cost*(1-down), cash=cost-loan, fee=loan*pts, carry=loan*rate/12*mo, sc=arv*sell;
      var net=arv-cost-fee-carry-sc, roi=cash+fee+carry>0?net/(cash+fee+carry)*100:0;
      $('fc-loan').textContent=money(loan); $('fc-cash').textContent=money(cash);
      $('fc-fee').textContent=money(fee); $('fc-carry').textContent=money(carry);
      $('fc-sc').textContent=money(sc); $('fc-roi').textContent=roi.toFixed(0)+'%';
      $('fc-net').textContent=money(net);
      $('fc-netbox').className='o big '+(net>=0?'pos':'neg');
    };
    document.querySelectorAll('[id^="fc-"]').forEach(function(e){if(e.tagName==='INPUT')e.addEventListener('input',fc)}); fc();
  }

  /* max offer (rule-of-thumb) */
  if($('mo-arv')){
    var mo=function(){
      var arv=val('mo-arv'),rep=val('mo-rep'),pct=val('mo-pct')/100,fee=val('mo-fee');
      $('mo-out').textContent=money(arv*pct-rep-fee);
      $('mo-line').textContent=money(arv)+' × '+(pct*100).toFixed(0)+'% − '+money(rep)+(fee?' − '+money(fee):'');
    };
    ['mo-arv','mo-rep','mo-pct','mo-fee'].forEach(function(i){$(i).addEventListener('input',mo)}); mo();
  }

  /* DSCR */
  if($('dr-loan')){
    var dr=function(){
      var L=val('dr-loan'),R=val('dr-rent'),TI=val('dr-ti'),h='';
      [5.5,6,6.5,7,7.5,8,8.5].forEach(function(rt){
        var r=rt/100/12,n=360,pi=L*r/(1-Math.pow(1+r,-n)),piti=pi+TI,d=piti>0?R/piti:0;
        var c=d>=1.2?'s':d>=1?'w':'t', w=d>=1.2?T.strong:d>=1?T.works:T.thin;
        h+='<tr><td class="num-c">'+rt.toFixed(1)+'%</td><td class="num-c">'+money(pi)+'</td><td class="num-c">'+money(piti)+'</td><td class="num-c"><b>'+d.toFixed(2)+'</b></td><td><span class="verdict '+c+'">'+w+'</span></td></tr>';
      });
      $('dr-body').innerHTML=h;
    };
    ['dr-loan','dr-rent','dr-ti'].forEach(function(i){$(i).addEventListener('input',dr)}); dr();
  }

  /* application wizard */
  var wf=$('apply-form');
  if(wf){
    wf.classList.add('js-wiz');
    var sets=[].slice.call(wf.querySelectorAll('fieldset')), dots=[].slice.call(document.querySelectorAll('.wiz-prog div')), cur=0, wmsg=wf.querySelector('.fmsg');
    var summary=function(){
      var d={}; new FormData(wf).forEach(function(v,k){if(v&&k!=='company'&&k!=='agree')d[k]=v});
      var lines=[]; wf.querySelectorAll('[data-label]').forEach(function(el){
        var k=el.name; if(el.type==='radio'&&!el.checked) return;
        if(d[k]) lines.push(el.getAttribute('data-label')+': '+d[k]);
      });
      return lines.join('\n');
    };
    var show=function(i){
      cur=i; sets.forEach(function(s,k){s.classList.toggle('on',k===i)});
      dots.forEach(function(s,k){s.className=k===i?'on':(k<i?'done':'')});
      if(i===sets.length-1) $('apply-review').textContent=summary();
      wmsg.className='fmsg';
      var top=wf.getBoundingClientRect().top+window.scrollY-110; if(window.scrollY>top) window.scrollTo(0,top);
    };
    var valid=function(i){
      var ok=true; sets[i].querySelectorAll('input,select,textarea').forEach(function(el){if(!el.checkValidity()){ok=false}});
      if(!ok){var bad=sets[i].querySelector(':invalid'); if(bad&&bad.reportValidity) bad.reportValidity(); wmsg.textContent=T.req; wmsg.className='fmsg err'}
      return ok;
    };
    wf.querySelectorAll('[data-next]').forEach(function(x){x.addEventListener('click',function(){if(valid(cur)) show(cur+1)})});
    wf.querySelectorAll('[data-back]').forEach(function(x){x.addEventListener('click',function(){show(cur-1)})});
    wf.addEventListener('submit',function(e){
      e.preventDefault(); if(!valid(cur)) return;
      var fd=new FormData(wf);
      var d={name:fd.get('name'),phone:fd.get('phone'),email:fd.get('email'),company:fd.get('company')||'',
        interest:'Investor lending — '+(fd.get('loan_type')||'Application'),
        msg:'ONLINE APPLICATION\n'+summary(),
        source:'ASAP Lending — Online application'+(ES?' (ES)':''),page:location.pathname};
      post(wf,d,wmsg,wf.querySelector('button[type=submit]'));
    });
    show(0);
  }

  /* photo gallery appears only when the photo files exist */
  var g=document.querySelector('[data-gallery]');
  if(g){
    g.querySelectorAll('img').forEach(function(im){
      var ok=function(){g.hidden=false}, bad=function(){var f=im.closest('figure'); if(f) f.remove()};
      if(im.complete){im.naturalWidth?ok():bad()} else {im.addEventListener('load',ok); im.addEventListener('error',bad)}
    });
  }
})();
