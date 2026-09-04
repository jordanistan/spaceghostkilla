(() => {
  // Scroll-reveal
  const reveal = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        reveal.unobserve(entry.target);
      }
    }
  }, { threshold: 0.12 });
  document.querySelectorAll('.reveal').forEach(el => reveal.observe(el));

  // Vulnerability filters
  const filters = document.querySelectorAll('.filter');
  const cards = document.querySelectorAll('.vuln-card');
  filters.forEach(button => {
    button.addEventListener('click', () => {
      filters.forEach(b => b.classList.remove('active'));
      button.classList.add('active');
      const filter = button.dataset.filter;
      cards.forEach(card => {
        const categories = card.dataset.category.split(' ');
        card.classList.toggle('hidden', filter !== 'all' && !categories.includes(filter));
      });
    });
  });

  // Themed local navigation terminal — intentionally not a shell.
  const form = document.getElementById('terminal-form');
  const input = document.getElementById('terminal-input');
  const output = document.getElementById('terminal-output');

  const print = (html) => {
    const p = document.createElement('p');
    p.innerHTML = html;
    output.appendChild(p);
    output.scrollTop = output.scrollHeight;
  };

  const commands = {
    help() {
      print('<span class="prompt">AVAILABLE:</span> help, status, vulns, owasp, research, disclosure, about, clear');
    },
    status() {
      print('HOSTNAME: <b>SPACEGHOSTIKILLA</b> // PHANTOM PROTOCOL: <b style="color:#5cffb0">ONLINE</b> // MODE: DEFENSIVE RESEARCH');
    },
    vulns() {
      print('Opening vulnerability index...');
      document.getElementById('vulnerabilities').scrollIntoView({ behavior: 'smooth' });
    },
    owasp() {
      print('Study path: broken access control, injection, cryptographic failures, insecure design, misconfiguration, vulnerable components, authentication failures, integrity failures, logging/monitoring failures, and SSRF.');
    },
    research() {
      print('Opening field notes...');
      document.getElementById('research').scrollIntoView({ behavior: 'smooth' });
    },
    disclosure() {
      print('Opening responsible disclosure policy...');
      document.getElementById('disclosure').scrollIntoView({ behavior: 'smooth' });
    },
    about() {
      print('SPACEGHOSTIKILLA is a themed personal security research node focused on vulnerability understanding, detection engineering, and remediation.');
    },
    clear() {
      output.innerHTML = '';
    }
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const cmd = input.value.trim().toLowerCase();
    if (!cmd) return;
    print(`<span style="color:#ca33a0">user@spaceghostikilla:~$</span> ${cmd.replace(/[<>]/g, '')}`);
    if (commands[cmd]) commands[cmd]();
    else print(`command not found: <b>${cmd.replace(/[<>]/g, '')}</b> — type <b>help</b>`);
    input.value = '';
  });

  // Starfield background
  const canvas = document.getElementById('starfield');
  const ctx = canvas.getContext('2d');
  let stars = [];
  let width = 0;
  let height = 0;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.min(180, Math.floor((width * height) / 8500));
    stars = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      r: Math.random() * 1.2 + .2,
      a: Math.random() * .55 + .12,
      v: Math.random() * .012 + .003,
      phase: Math.random() * Math.PI * 2,
    }));
  };

  const draw = (t = 0) => {
    ctx.clearRect(0, 0, width, height);
    for (const s of stars) {
      const alpha = reduced ? s.a : s.a * (.75 + Math.sin(t * s.v + s.phase) * .25);
      ctx.beginPath();
      ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(233, 199, 255, ${Math.max(0.05, alpha)})`;
      ctx.fill();
    }
    if (!reduced) requestAnimationFrame(draw);
  };

  resize();
  window.addEventListener('resize', resize, { passive: true });
  requestAnimationFrame(draw);
})();
