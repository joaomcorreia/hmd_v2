
(() => {

    // ===== CONFIG YOU CAN TUNE PER PROJECT =====
    const CFG = {
        relay: '/ai/contextual/',
        title: 'Demo Klus BV Assistent',
        icon: "{% static 'img/apps/demo-klus-assistent.png' %}",  // your 160px image
        iconSizeHeader: 56,   // visible, detailed
        iconSizeBubble: 40,
        brand: '#00a651',
        system: `Je bent de AI-assistent van Demo Klus BV.  
Standaard antwoord je in het Nederlands. 
Maar als de gebruiker in het Engels of Arabisch begint, ga dan verder in die taal. 
Antwoord altijd kort en duidelijk in dezelfde taal die de gebruiker gebruikt.
- Focus: schilderwerk, elektra, tegelwerk, stucwerk, badkamer/keuken, vloeren, dakwerk.
- Als iemand een prijs wil: geef grove uitleg en stel voor een afspraak te maken via WhatsApp.
- Eindig niet altijd met dezelfde zin; varieer beleefd.
- Zaken buiten onze diensten? Kort antwoorden en vriendelijk terug naar onze diensten.
Voordat je een gesprek afsluit:
- Verzamel nog enkele extra details die belangrijk zijn voor de klus (bijv. type dienst, grootte/opervlakte, gewenste datum, eventueel budget).
- Vraag dan: “Zal ik een WhatsApp-bericht voor u opstellen met al deze details zodat u het direct kunt versturen?”
- Als de gebruiker akkoord gaat, genereer een duidelijk, WhatsApp-klaar bericht dat alles samenvat.
- Toon het bericht altijd eerst aan de gebruiker ter bevestiging voordat het wordt verstuurd.`
    };
    // ===========================================

    const d = document, root = d.getElementById('hmd-assistant');

    // base styles
    const css = d.createElement('style');
    css.textContent = `
.hmd-chat{font:14px/1.45 system-ui,-apple-system,Segoe UI,Roboto,Arial;color:#111}
.hmd-head{display:flex;align-items:center;gap:10px;background:${CFG.brand};color:#fff;padding:10px 12px;border-radius:12px 12px 0 0}
.hmd-head img{width:${CFG.iconSizeHeader}px;height:${CFG.iconSizeHeader}px;border-radius:50%;background:#fff;flex:0 0 auto}
.hmd-body{background:#fff;border:1px solid #e6e6e6;border-top:0;border-radius:0 0 12px 12px;overflow:hidden}
.hmd-log{height:280px;overflow:auto;padding:10px 12px}
.hmd-row{display:flex;gap:8px;margin:8px 0;align-items:flex-start}
.hmd-row img{width:${CFG.iconSizeBubble}px;height:${CFG.iconSizeBubble}px;border-radius:50%;flex:0 0 auto}
.hmd-bot{background:#f5f7fb;border:1px solid #e5ecfb;padding:8px 10px;border-radius:10px;max-width:80%}
.hmd-user{background:#eefaf3;border:1px solid #d5f0e1;margin-left:auto;padding:8px 10px;border-radius:10px;max-width:80%}
.hmd-input{display:flex;gap:8px;padding:10px;border-top:1px solid #eee;background:#fff}
.hmd-input input{flex:1;border:1px solid #ddd;border-radius:10px;padding:10px}
.hmd-input button{border:0;background:${CFG.brand};color:#fff;border-radius:10px;padding:10px 14px;font-weight:700;cursor:pointer}
.hmd-float{position:fixed;right:18px;bottom:18px;z-index:9999}
.hmd-fab{border:0;border-radius:999px;background:${CFG.brand};color:#fff;cursor:pointer;width:56px;height:56px;box-shadow:0 10px 28px rgba(0,0,0,.25);font-size:22px}
.hmd-panel{display:none;width:min(360px,92vw)}
`;
    d.head.appendChild(css);

    // build UI
    function build(container) {
        const wrap = d.createElement('div');
        wrap.className = 'hmd-chat';

        const head = d.createElement('div');
        head.className = 'hmd-head';
        head.innerHTML = `<img alt=""><strong>${CFG.title}</strong>`;

        head.querySelector('img').src = CFG.icon;

        const body = d.createElement('div');
        body.className = 'hmd-body';

        const log = d.createElement('div'); log.className = 'hmd-log';
        const input = d.createElement('div'); input.className = 'hmd-input';
        input.innerHTML = `<input type="text" placeholder="Typ uw vraag..."><button>Verstuur</button>`;

        body.append(log, input);
        wrap.append(head, body);
        container.append(wrap);

        // greeting
        addBot(log, 'Hoi! Waarmee kan ik u helpen?');

        // events
        const field = input.querySelector('input');
        const send = input.querySelector('button');
        send.onclick = () => {
            const q = field.value.trim();
            if (!q) return;
            addUser(log, q);
            field.value = '';
            ask(q).then(a => addBot(log, a)).catch(() => addBot(log, 'Sorry, even geen verbinding.'));
        };
        field.addEventListener('keydown', e => {
            if (e.key === 'Enter') { send.click(); }
        });

        return wrap;
    }

    function addBot(log, text) {
        const row = d.createElement('div'); row.className = 'hmd-row';
        row.innerHTML = `<img src="${CFG.icon}" alt=""><div class="hmd-bot"></div>`;
        row.querySelector('.hmd-bot').textContent = text;
        log.append(row); log.scrollTop = log.scrollHeight;
    }
    function addUser(log, text) {
        const row = d.createElement('div'); row.className = 'hmd-row';
        row.innerHTML = `<div class="hmd-user"></div>`;
        row.querySelector('.hmd-user').textContent = text;
        log.append(row); log.scrollTop = log.scrollHeight;
    }

    async function ask(prompt) {
        // Get CSRF token for Django
        const csrfToken = getCsrfToken();
        
        const r = await fetch(CFG.relay, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ 
                question: prompt,
                current_page: 'frontend',
                page_context: 'customer'
            })
        });
        const j = await r.json();
        return j?.response || j?.error || 'Geen antwoord.';
    }

    function getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') return value;
        }
        
        // Fallback: try to get from meta tag
        const csrfMeta = document.querySelector('meta[name="csrf-token"]');
        if (csrfMeta) return csrfMeta.getAttribute('content');
        
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) return csrfInput.value;
        
        return '';
    }

    // mount
    if (root) {
        build(root);
    } else {
        // floating fallback
        const dock = d.createElement('div'); dock.className = 'hmd-float';
        const fab = d.createElement('button'); fab.className = 'hmd-fab'; fab.textContent = '💬';
        const panel = d.createElement('div'); panel.className = 'hmd-panel';
        dock.append(panel, fab); d.body.appendChild(dock);
        fab.onclick = () => {
            if (panel.style.display === 'block') { panel.style.display = 'none'; return; }
            panel.style.display = 'block'; panel.innerHTML = ''; build(panel);
        };
    }

})();
