import json
import re

with open('Relatorio_Oficial_OBLI_2024_2_Cooeducar.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('portal_data.json', 'r', encoding='utf-8') as f:
    portal_data = json.load(f)

with open('test_css.py', 'r', encoding='utf-8') as f:
    test_css_code = f.read()

extra_css_match = re.search(r'extra_css = """(.*?)"""', test_css_code, re.DOTALL)
extra_css = extra_css_match.group(1) if extra_css_match else ""

# Add print isolation for individual student modal
extra_css += """
    @media print {
      body.printing-modal .top-navbar,
      body.printing-modal .report-container {
        display: none !important;
      }
      body.printing-modal .modal-backdrop {
        position: static !important;
        background: transparent !important;
        backdrop-filter: none !important;
        padding: 0 !important;
        display: block !important;
        opacity: 1 !important;
      }
      body.printing-modal .modal-container {
        box-shadow: none !important;
        border: 2px solid #0B2265 !important;
        max-width: 100% !important;
        max-height: none !important;
        transform: none !important;
        page-break-inside: avoid !important;
      }
      body.printing-modal .modal-close-btn,
      body.printing-modal .modal-footer-btns {
        display: none !important;
      }
    }
"""

style_idx = html.find('</style>')
if style_idx != -1:
    html = html[:style_idx] + extra_css + "\n  </style>" + html[style_idx+8:]

# Enhance navbar: Add "🔍 Consulta & Raio-X" and Theme Toggle
old_nav_pills = """      <button class="nav-btn active" onclick="filterSection('ALL', this)">📑 Todas as Salas (Completo)</button>
      <button class="nav-btn" onclick="filterSection('panorama-escola', this)">🏛️ Panorama Escola</button>"""

new_nav_pills = """      <button class="nav-btn active" onclick="filterSection('ALL', this)">📑 Visão Geral Completa</button>
      <button class="nav-btn" onclick="filterSection('explorer-alunos', this)">🔍 Consulta & Raio-X</button>
      <button class="nav-btn" onclick="filterSection('panorama-escola', this)">🏛️ Panorama Escola</button>"""

if old_nav_pills in html:
    html = html.replace(old_nav_pills, new_nav_pills)

# Add theme toggle button before print button
old_print_btn = """<button class="btn-print" onclick="window.print()">
      🖨️ Imprimir / Salvar PDF
    </button>"""

new_print_and_theme = """<div style="display: flex; align-items: center; gap: 8px;">
      <button class="theme-toggle-btn" id="theme-toggle-btn" onclick="toggleTheme()" title="Alternar entre modo claro e escuro">
        🌙 Modo Escuro
      </button>
      <button class="btn-print" onclick="window.print()">
        🖨️ Imprimir / Salvar PDF
      </button>
    </div>"""

if old_print_btn in html:
    html = html.replace(old_print_btn, new_print_and_theme)

# Create Explorer Section HTML
explorer_html = """
    <!-- ===================================================================== -->
    <!-- CENTRAL DE CONSULTA INTERATIVA & RAIO-X INDIVIDUAL (PORTAL WEB)       -->
    <!-- ===================================================================== -->
    <section id="explorer-alunos" class="report-page" data-turma="explorer-alunos">
      <div class="explorer-header">
        <div class="explorer-title">
          <span>🔍</span> Central de Consulta Rápida & Raio-X Individual
        </div>
        <div class="explorer-desc">
          Pesquise qualquer estudante da Cooeducar para abrir o diagnóstico completo de desempenho, detalhamento de acertos e erros questão por questão (Reading e Listening) e posicionamento na turma.
        </div>
        
        <div class="explorer-controls">
          <div class="search-box-wrap">
            <span class="search-icon-inside">🔎</span>
            <input type="text" id="stu-search-input" class="search-box-input" placeholder="Digite o nome do aluno (ex: Benício, Alice, Sara, Maria...)" oninput="handleSearch(this.value)" autocomplete="off">
            <button id="stu-search-clear" class="search-clear-btn" onclick="clearSearch()">✕</button>
          </div>
          
          <div class="filter-pills-row" id="turma-filter-row">
            <button class="filter-chip active" onclick="setTurmaFilter('ALL', this)">Todas as Turmas (78)</button>
            <button class="filter-chip" onclick="setTurmaFilter('6º Ano', this)">6º Ano (12)</button>
            <button class="filter-chip" onclick="setTurmaFilter('7º Ano', this)">7º Ano (20)</button>
            <button class="filter-chip" onclick="setTurmaFilter('8º Ano', this)">8º Ano (7)</button>
            <button class="filter-chip" onclick="setTurmaFilter('9º Ano', this)">9º Ano (9)</button>
            <button class="filter-chip" onclick="setTurmaFilter('1ª Série EM', this)">1ª Série EM (8)</button>
            <button class="filter-chip" onclick="setTurmaFilter('2ª Série EM', this)">2ª Série EM (10)</button>
            <button class="filter-chip" onclick="setTurmaFilter('3ª Série EM', this)">3ª Série EM (12)</button>
          </div>
        </div>
      </div>

      <div class="sort-and-count-bar">
        <div class="stu-count-indicator" id="stu-count-text">
          Mostrando <strong>70</strong> alunos avaliados
        </div>
        <div class="sort-control">
          <label for="sort-select">Ordenar por:</label>
          <select id="sort-select" class="sort-select" onchange="handleSort(this.value)">
            <option value="score-desc">Maior Pontuação Geral (Decrescente)</option>
            <option value="score-asc">Menor Pontuação Geral (Crescente)</option>
            <option value="reading-desc">Maior Reading (Leitura)</option>
            <option value="listening-desc">Maior Listening (Escuta)</option>
            <option value="name-asc">Nome do Aluno (A - Z)</option>
          </select>
        </div>
      </div>

      <div class="stu-cards-grid" id="stu-cards-container">
        <!-- Renderizado dinamicamente via JS -->
      </div>
    </section>
"""

panorama_end = html.find('</section>')
if panorama_end != -1:
    html = html[:panorama_end+10] + "\n" + explorer_html + "\n" + html[panorama_end+10:]

modal_and_script = f"""
  <!-- ===================================================================== -->
  <!-- MODAL FLUTUANTE: RAIO-X INDIVIDUAL DO ALUNO                           -->
  <!-- ===================================================================== -->
  <div class="modal-backdrop" id="stu-modal-backdrop" onclick="handleBackdropClick(event)">
    <div class="modal-container" id="stu-modal-card">
      <div class="modal-header-hero">
        <button class="modal-close-btn" onclick="closeStudentModal()" title="Fechar">✕</button>
        <div class="modal-stu-title" id="m-stu-name">Nome do Aluno</div>
        <div class="modal-stu-sub">
          <span class="modal-pill" id="m-stu-turma">Turma</span>
          <span class="modal-pill" id="m-stu-num">Nº 00</span>
          <span class="modal-pill" id="m-stu-rank">1º Lugar</span>
          <span class="modal-pill" id="m-stu-school-rank">Top Escola</span>
        </div>
      </div>

      <div class="modal-body-content">
        <div class="modal-kpis-row">
          <div class="modal-kpi-card">
            <div class="modal-kpi-label">Pontuação Geral</div>
            <div class="modal-kpi-val" id="m-kpi-total">0 / 30</div>
            <div class="modal-kpi-sub" id="m-kpi-pct">0.0% de aproveitamento</div>
          </div>
          <div class="modal-kpi-card" style="border-left: 3px solid #2563EB;">
            <div class="modal-kpi-label" style="color: #2563EB;">Reading (Leitura)</div>
            <div class="modal-kpi-val" id="m-kpi-reading" style="color: #2563EB;">0 / 20</div>
            <div class="modal-kpi-sub" id="m-kpi-r-pct">0.0% nas questões 01-20</div>
          </div>
          <div class="modal-kpi-card" style="border-left: 3px solid #DC2626;">
            <div class="modal-kpi-label" style="color: #DC2626;">Listening (Escuta)</div>
            <div class="modal-kpi-val" id="m-kpi-listening" style="color: #DC2626;">0 / 10</div>
            <div class="modal-kpi-sub" id="m-kpi-l-pct">0.0% nas questões 21-30</div>
          </div>
        </div>

        <div style="background: var(--bg-page); border-radius: 12px; padding: 14px 18px; margin-bottom: 20px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
          <div>
            <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: var(--text-muted); margin-bottom: 2px;">Diagnóstico de Perfil</div>
            <div id="m-stu-profile-badge" style="font-size: 14px; font-weight: 800; color: var(--coo-navy);">Perfil Equilibrado</div>
          </div>
          <div id="m-stu-insight-text" style="font-size: 13px; color: var(--text-muted); font-weight: 600; max-width: 450px;">
            Desempenho consolidado nas duas habilidades avaliadas.
          </div>
        </div>

        <!-- DETALHAMENTO DAS 30 QUESTÕES -->
        <div class="matrix-section-title">
          <span>📖 Questões 01 a 20: Compreensão Leitora (Reading)</span>
          <span style="font-size: 12px; font-weight: 700; color: #2563EB;" id="m-reading-summary">Acertos: 0/20</span>
        </div>
        <div class="q-grid" id="m-grid-reading"></div>

        <div class="matrix-section-title">
          <span>🎧 Questões 21 a 30: Compreensão Auditiva (Listening)</span>
          <span style="font-size: 12px; font-weight: 700; color: #DC2626;" id="m-listening-summary">Acertos: 0/10</span>
        </div>
        <div class="q-grid" id="m-grid-listening"></div>

        <div class="modal-footer-btns">
          <button class="btn-secondary" onclick="closeStudentModal()">✕ Fechar Raio-X</button>
          <button class="btn-primary" onclick="printStudentBoletim()">🖨️ Imprimir Boletim Deste Aluno</button>
        </div>
      </div>
    </div>
  </div>

  <!-- SCRIPT DINÂMICO DO PORTAL -->
  <script>
    const PORTAL_DATA = {json.dumps(portal_data, ensure_ascii=False)};
    let activeTurmaFilter = 'ALL';
    let currentSearchQuery = '';
    let currentSortOrder = 'score-desc';
    let selectedStudent = null;

    // Inicialização ao carregar página
    document.addEventListener('DOMContentLoaded', () => {{
      initTheme();
      renderCards();
      setupClickableElements();
    }});

    // Gerenciamento de Tema (Dark / Light)
    function initTheme() {{
      const savedTheme = localStorage.getItem('cooeducar_theme') || 'light';
      document.documentElement.setAttribute('data-theme', savedTheme);
      updateThemeButton(savedTheme);
    }}

    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('cooeducar_theme', next);
      updateThemeButton(next);
    }}

    function updateThemeButton(theme) {{
      const btn = document.getElementById('theme-toggle-btn');
      if (btn) {{
        btn.innerHTML = theme === 'dark' ? '☀️ Modo Claro' : '🌙 Modo Escuro';
      }}
    }}

    // Filtros e Busca
    function setTurmaFilter(turma, btnEl) {{
      activeTurmaFilter = turma;
      document.querySelectorAll('#turma-filter-row .filter-chip').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      renderCards();
    }}

    function handleSearch(val) {{
      currentSearchQuery = val.trim().toLowerCase();
      const clearBtn = document.getElementById('stu-search-clear');
      if (clearBtn) clearBtn.style.display = currentSearchQuery.length > 0 ? 'flex' : 'none';
      renderCards();
    }}

    function clearSearch() {{
      const input = document.getElementById('stu-search-input');
      if (input) {{
        input.value = '';
        currentSearchQuery = '';
        const clearBtn = document.getElementById('stu-search-clear');
        if (clearBtn) clearBtn.style.display = 'none';
        renderCards();
        input.focus();
      }}
    }}

    function handleSort(val) {{
      currentSortOrder = val;
      renderCards();
    }}

    // Renderização dos Cards de Estudantes
    function renderCards() {{
      const container = document.getElementById('stu-cards-container');
      const countEl = document.getElementById('stu-count-text');
      if (!container) return;

      let list = [...PORTAL_DATA.students];

      // Filtro de Turma
      if (activeTurmaFilter !== 'ALL') {{
        list = list.filter(s => s.turma === activeTurmaFilter);
      }}

      // Filtro de Busca
      if (currentSearchQuery) {{
        list = list.filter(s => s.name.toLowerCase().includes(currentSearchQuery) || s.turma.toLowerCase().includes(currentSearchQuery));
      }}

      // Ordenação
      list.sort((a, b) => {{
        if (!a.present && b.present) return 1;
        if (a.present && !b.present) return -1;
        if (!a.present && !b.present) return a.name.localeCompare(b.name);

        switch (currentSortOrder) {{
          case 'score-desc':
            return b.total_score - a.total_score || b.reading_score - a.reading_score || a.name.localeCompare(b.name);
          case 'score-asc':
            return a.total_score - b.total_score || a.reading_score - b.reading_score || a.name.localeCompare(b.name);
          case 'reading-desc':
            return b.reading_score - a.reading_score || b.total_score - a.total_score || a.name.localeCompare(b.name);
          case 'listening-desc':
            return b.listening_score - a.listening_score || b.total_score - a.total_score || a.name.localeCompare(b.name);
          case 'name-asc':
            return a.name.localeCompare(b.name);
          default:
            return b.total_score - a.total_score;
        }}
      }});

      if (countEl) {{
        const presCount = list.filter(s => s.present).length;
        countEl.innerHTML = `Mostrando <strong>${{list.length}}</strong> alunos (${{presCount}} presentes)`;
      }}

      if (list.length === 0) {{
        container.innerHTML = `
          <div style="grid-column: 1 / -1; padding: 40px; text-align: center; color: var(--text-muted); background: var(--bg-card); border-radius: 14px; border: 1px dashed var(--border-light);">
            <div style="font-size: 32px; margin-bottom: 8px;">🔍</div>
            <div style="font-size: 16px; font-weight: 800; color: var(--text-dark);">Nenhum aluno encontrado</div>
            <div style="font-size: 13px;">Tente buscar com outro termo ou selecione "Todas as Turmas".</div>
          </div>
        `;
        return;
      }}

      container.innerHTML = list.map(s => {{
        const initials = s.name.split(' ').map(n => n[0]).slice(0, 2).join('');
        let badgeClass = 'badge-rank-std';
        let badgeText = `${{s.rank_turma}}º na Turma`;
        if (s.rank_turma === 1) {{ badgeClass = 'badge-rank-1'; badgeText = '🥇 1º Lugar'; }}
        else if (s.rank_turma === 2) {{ badgeClass = 'badge-rank-2'; badgeText = '🥈 2º Lugar'; }}
        else if (s.rank_turma === 3) {{ badgeClass = 'badge-rank-3'; badgeText = '🥉 3º Lugar'; }}
        else if (!s.present) {{ badgeClass = 'badge-rank-std'; badgeText = 'Ausente'; }}

        return `
          <div class="stu-card" onclick="openStudentModal('${{s.id}}')">
            <div>
              <div class="stu-card-top">
                <div class="stu-card-avatar">${{initials}}</div>
                <div class="stu-card-info">
                  <div class="stu-card-name" title="${{s.name}}">${{s.name}}</div>
                  <div class="stu-card-meta">
                    <span>${{s.turma}}</span>
                    <span>•</span>
                    <span>#${{s.num}}</span>
                  </div>
                </div>
                <span class="stu-card-badge ${{badgeClass}}">${{badgeText}}</span>
              </div>

              ${{s.present ? `
                <div class="stu-card-score-box">
                  <div>
                    <div style="font-size: 10px; font-weight: 800; text-transform: uppercase; color: var(--text-muted);">Nota Geral</div>
                    <div class="stu-card-main-score">${{s.total_score}}<span style="font-size: 13px; font-weight: 600; opacity: 0.7;"> / 30</span></div>
                  </div>
                  <div class="stu-card-pct-badge">${{s.pct_total}}%</div>
                </div>

                <div class="stu-card-bars">
                  <div>
                    <div class="stu-card-bar-item">
                      <span style="color: #2563EB;">📖 Reading</span>
                      <span><strong>${{s.reading_score}}</strong>/20 (${{s.pct_reading}}%)</span>
                    </div>
                    <div class="stu-card-track">
                      <div class="stu-card-fill-r" style="width: ${{s.pct_reading}}%;"></div>
                    </div>
                  </div>
                  <div>
                    <div class="stu-card-bar-item">
                      <span style="color: #DC2626;">🎧 Listening</span>
                      <span><strong>${{s.listening_score}}</strong>/10 (${{s.pct_listening}}%)</span>
                    </div>
                    <div class="stu-card-track">
                      <div class="stu-card-fill-l" style="width: ${{s.pct_listening}}%;"></div>
                    </div>
                  </div>
                </div>
              ` : `
                <div style="background: var(--bg-page); border-radius: 10px; padding: 24px 12px; margin-bottom: 14px; text-align: center; color: var(--text-muted); font-size: 13px; font-weight: 700;">
                  ⚠️ Aluno ausente no dia da aplicação
                </div>
              `}}
            </div>

            <div class="stu-card-footer">
              <span>Raio-X Completo ➔</span>
              <span style="color: var(--text-muted); font-size: 11px;">#${{s.rank_escola}} no Geral</span>
            </div>
          </div>
        `;
      }}).join('');
    }}

    // Abrir Modal do Aluno
    function openStudentModal(stuId) {{
      const student = PORTAL_DATA.students.find(s => s.id === stuId);
      if (!student) return;
      selectedStudent = student;

      document.getElementById('m-stu-name').innerText = student.name;
      document.getElementById('m-stu-turma').innerText = student.turma;
      document.getElementById('m-stu-num').innerText = `Chamada #${{student.num}}`;
      document.getElementById('m-stu-rank').innerText = student.present ? `${{student.rank_turma}}º na Turma` : 'Ausente';
      document.getElementById('m-stu-school-rank').innerText = student.present ? `#${{student.rank_escola}} Geral na Escola` : 'Sem classificação';

      document.getElementById('m-kpi-total').innerText = student.present ? `${{student.total_score}} / 30` : '0 / 30';
      document.getElementById('m-kpi-pct').innerText = student.present ? `${{student.pct_total}}% de aproveitamento geral` : 'Aluno ausente';

      document.getElementById('m-kpi-reading').innerText = student.present ? `${{student.reading_score}} / 20` : '0 / 20';
      document.getElementById('m-kpi-r-pct').innerText = student.present ? `${{student.pct_reading}}% nas questões 01-20` : '0.0%';

      document.getElementById('m-kpi-listening').innerText = student.present ? `${{student.listening_score}} / 10` : '0 / 10';
      document.getElementById('m-kpi-l-pct').innerText = student.present ? `${{student.pct_listening}}% nas questões 21-30` : '0.0%';

      document.getElementById('m-reading-summary').innerText = student.present ? `Acertos: ${{student.reading_score}} / 20 (${{student.pct_reading}}%)` : 'Ausente';
      document.getElementById('m-listening-summary').innerText = student.present ? `Acertos: ${{student.listening_score}} / 10 (${{student.pct_listening}}%)` : 'Ausente';

      // Diagnóstico Pedagógico
      let profileTitle = '⚖️ Desempenho Equilibrado';
      let profileDesc = 'O aluno demonstrou domínio balanceado entre compreensão textual e percepção auditiva.';
      if (!student.present) {{
        profileTitle = '⚠️ Avaliação Não Realizada';
        profileDesc = 'O aluno não compareceu à aplicação oficial da OBLI 2024.2.';
      }} else if (student.pct_listening >= student.pct_reading + 15) {{
        profileTitle = '🎧 Destaque Superior em Listening';
        profileDesc = 'Excelente percepção auditiva e fonética em inglês, superando o rendimento leitor.';
      }} else if (student.pct_reading >= student.pct_listening + 15) {{
        profileTitle = '📖 Destaque Superior em Reading';
        profileDesc = 'Forte repertório gramatical e vocabulário analítico, com facilidade em textos e enunciados.';
      }} else if (student.total_score >= 20) {{
        profileTitle = '🌟 Alto Rendimento Global (Destaque OBLI)';
        profileDesc = 'Pontuação notável e consistente em ambas as áreas da maratona.';
      }}

      document.getElementById('m-stu-profile-badge').innerText = profileTitle;
      document.getElementById('m-stu-insight-text').innerText = profileDesc;

      // Renderizar Questões Reading (01 a 20)
      const rContainer = document.getElementById('m-grid-reading');
      const rDetails = student.details.slice(0, 20);
      rContainer.innerHTML = rDetails.map(d => renderQBox(d)).join('');

      // Renderizar Questões Listening (21 a 30)
      const lContainer = document.getElementById('m-grid-listening');
      const lDetails = student.details.slice(20, 30);
      lContainer.innerHTML = lDetails.map(d => renderQBox(d)).join('');

      const backdrop = document.getElementById('stu-modal-backdrop');
      backdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    }}

    function renderQBox(d) {{
      let boxClass = 'q-box-wrong';
      let symbol = '✗';
      let detailText = `Gab: ${{d.correct_ans}}`;

      if (d.is_annulled) {{
        boxClass = 'q-box-annulled';
        symbol = '★';
        detailText = 'Anulada (+1)';
      }} else if (d.is_correct) {{
        boxClass = 'q-box-correct';
        symbol = '✓';
        detailText = 'Acerto';
      }}

      const displayAns = d.student_ans ? d.student_ans : '-';
      const qNumFormatted = d.q < 10 ? `Q0${{d.q}}` : `Q${{d.q}}`;

      return `
        <div class="q-box ${{boxClass}}" title="${{qNumFormatted}} • Marcada: [${{displayAns}}] • Oficial: [${{d.correct_ans}}]">
          <span class="q-box-num">${{qNumFormatted}}</span>
          <span class="q-box-ans">${{displayAns}} ${{symbol}}</span>
          <span class="q-box-detail">${{detailText}}</span>
        </div>
      `;
    }}

    function openStudentModalByName(name) {{
      const cleanName = name.trim().toLowerCase();
      const student = PORTAL_DATA.students.find(s => s.name.toLowerCase() === cleanName);
      if (student) {{
        openStudentModal(student.id);
      }}
    }}

    function closeStudentModal() {{
      const backdrop = document.getElementById('stu-modal-backdrop');
      backdrop.classList.remove('active');
      document.body.style.overflow = '';
      selectedStudent = null;
    }}

    function handleBackdropClick(e) {{
      if (e.target.id === 'stu-modal-backdrop') {{
        closeStudentModal();
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeStudentModal();
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {{
        e.preventDefault();
        filterSection('explorer-alunos');
        const input = document.getElementById('stu-search-input');
        if (input) input.focus();
      }}
    }});

    function printStudentBoletim() {{
      document.body.classList.add('printing-modal');
      window.print();
      setTimeout(() => {{
        document.body.classList.remove('printing-modal');
      }}, 1000);
    }}

    // Conectar todos os nomes clicáveis das tabelas e barras
    function setupClickableElements() {{
      document.querySelectorAll('.stu-bar-row').forEach(row => {{
        const nameEl = row.querySelector('.stu-bar-name');
        if (nameEl) {{
          const name = nameEl.innerText.trim();
          row.classList.add('clickable-student');
          row.setAttribute('title', `Clique para ver o Raio-X de ${{name}}`);
          row.onclick = () => openStudentModalByName(name);
        }}
      }});

      document.querySelectorAll('.data-table tbody tr').forEach(tr => {{
        const nameEl = tr.querySelector('.font-bold.text-dark');
        if (nameEl) {{
          const name = nameEl.innerText.trim();
          tr.classList.add('clickable-student');
          tr.setAttribute('title', `Clique para ver o Raio-X de ${{name}}`);
          tr.onclick = (e) => {{
            openStudentModalByName(name);
          }};
        }}
      }});
    }}
  </script>
"""

# Replace existing script or append before </body>
script_idx = html.rfind('</script>')
if script_idx != -1:
    body_end = html.find('</body>')
    html = html[:body_end] + modal_and_script + "\n</body>" + html[body_end+7:]

# Write to index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Regenerated index.html with printing-modal styles! Length:", len(html))
