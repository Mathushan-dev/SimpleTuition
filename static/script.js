document.addEventListener('DOMContentLoaded', function(){
  // no sidebar nav: use top admin cards for panel switching

  // Wrap admin UI initialization so we can re-run after AJAX swaps
  function initAdminUI(){
    // confirmation on remove user forms
    document.querySelectorAll('form[action="/admin/remove_user"]').forEach(function(f){
      f.removeEventListener('submit', f._delHandler)
      var h = function(e){ if(!confirm('Delete this user? This action cannot be undone.')){ e.preventDefault(); } }
      f.addEventListener('submit', h)
      f._delHandler = h
    })

    // Admin dashboard panel switching
    function showPanel(name, push){
      document.querySelectorAll('[data-panel-content]').forEach(function(el){
        el.style.display = (el.dataset.panelContent === name) ? 'block' : 'none'
      })
      document.querySelectorAll('.admin-card').forEach(function(card){
        if(card.dataset.panel === name) card.classList.add('active'); else card.classList.remove('active')
      })
      // update badge counts if available on page data attributes
      var counts = {
        users: document.querySelectorAll('[data-panel-content="users"] .list-item').length,
        lessons: document.querySelectorAll('[data-panel-content="lessons"] .list-item').length,
        subjects: document.querySelectorAll('[data-panel-content="subjects"] .list-item').length,
        assignments: document.querySelectorAll('[data-panel-content="assignments"] .list-item').length,
        reports: document.querySelectorAll('[data-panel-content="reports"] .info-item').length
      }
      document.querySelectorAll('.admin-card .badge, .admin-nav .badge').forEach(function(b){
        var key = b.dataset.badgeFor
        if(counts[key] !== undefined) b.textContent = counts[key]
      })
      if(push){ history.replaceState(null, '', '#'+name) }
    }

    // card click — switch panels or fetch server page if missing
    document.querySelectorAll('.admin-card[data-panel]').forEach(function(card){
      card.removeEventListener('click', card._cardHandler)
      var handler = function(e){
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return
        var p = card.dataset.panel
        var href = card.dataset.href || '#'
        if(document.querySelector('[data-panel-content="'+p+'"]')){
          e.preventDefault(); showPanel(p, true); return
        }
        e.preventDefault();
        fetch(href, {headers:{'X-Requested-With':'XMLHttpRequest'}}).then(function(resp){
          if(resp.status === 200) return resp.text(); throw new Error('non-200')
        }).then(function(text){
          var parser = new DOMParser(); var doc = parser.parseFromString(text, 'text/html'); var newDash = doc.querySelector('.dashboard')
          if(newDash){ var cur = document.querySelector('.dashboard'); cur.parentNode.replaceChild(newDash, cur); history.pushState({}, '', href); initAdminUI() }
          else { window.location = href }
        }).catch(function(){ window.location = href })
      }
      card.addEventListener('click', handler)
      card._cardHandler = handler
    })

    // show initial panel if present
    if(document.querySelector('[data-panel-content]')){
      var initial = (location.hash && location.hash.length>1) ? location.hash.substring(1) : 'users'
      showPanel(initial, false)
    }

    // Subjects interactivity: search + toggle details
    try{
      var subjSearch = document.getElementById('subject-search')
      if(subjSearch){
        subjSearch.addEventListener('input', function(){
          var q = subjSearch.value.trim().toLowerCase()
          document.querySelectorAll('#subjects-list .list-item').forEach(function(card){
            var name = card.dataset.name || ''
            var id = (card.dataset.id || '') + ''
            var show = !q || name.indexOf(q)!==-1 || id.indexOf(q)!==-1
            card.style.display = show ? '' : 'none'
          })
        })
      }
      document.querySelectorAll('#subjects-list .toggle-details').forEach(function(btn){
        btn.removeEventListener('click', btn._handler)
        var h = function(){ var c = this.closest('.card'); c.classList.toggle('expanded') }
        btn.addEventListener('click', h)
        btn._handler = h
      })
    }catch(e){}

    // Assignments interactivity: search + toggle + inline form remains functional
    try{
      var assignSearch = document.getElementById('assign-search')
      if(assignSearch){
        assignSearch.addEventListener('input', function(){
          var q = assignSearch.value.trim().toLowerCase()
          document.querySelectorAll('#assignments-list .list-item').forEach(function(card){
            var subj = (card.dataset.subject||'')+''
            var stud = (card.dataset.student||'')+''
            var show = !q || subj.indexOf(q)!==-1 || stud.indexOf(q)!==-1
            card.style.display = show ? '' : 'none'
          })
        })
      }
      document.querySelectorAll('#assignments-list .toggle-details').forEach(function(btn){
        btn.removeEventListener('click', btn._handler)
        var h = function(){ var c = this.closest('.card'); c.classList.toggle('expanded') }
        btn.addEventListener('click', h)
        btn._handler = h
      })
    }catch(e){}

    // Create user modal handlers
    var openBtn = document.getElementById('open-create-user')
    var modal = document.getElementById('create-user-modal')
    var closeBtn = document.getElementById('close-create-user')
    if(openBtn && modal){ openBtn.addEventListener('click', function(){ modal.style.display = 'flex' }) }
    if(closeBtn && modal){ closeBtn.addEventListener('click', function(){ modal.style.display = 'none' }) }

    // copy temp password button
    var copyBtn = document.getElementById('copy-temp-pass')
    if(copyBtn){
      copyBtn.removeEventListener('click', copyBtn._copyHandler)
      var copyHandler = function(){
        var t = document.getElementById('created-temp-pass'); if(!t) return
        navigator.clipboard.writeText(t.textContent).then(function(){ copyBtn.textContent = 'Copied'; setTimeout(function(){ copyBtn.textContent = 'Copy' }, 2000) })
      }
      copyBtn.addEventListener('click', copyHandler)
      copyBtn._copyHandler = copyHandler
    }
  }

  // initialize UI on first load
  initAdminUI()

  // On load: if SPA panels exist on this page, show the panel from hash (or users default)
  var hasPanels = !!document.querySelector('[data-panel-content]')
  if(hasPanels){
    var initial = (location.hash && location.hash.length>1) ? location.hash.substring(1) : 'users'
    showPanel(initial, false)
  }

  // If we're on a server-rendered admin route (eg. /admin/users), highlight matching card
  try{
    var path = location.pathname || ''
    document.querySelectorAll('.admin-card').forEach(function(c){ c.classList.remove('active'); var href = c.dataset.href || ''; if(href && (href === path || path.indexOf(href) === 0)) c.classList.add('active') })
  }catch(e){}

  // No sidebar minimize/hover behavior — cards replace the side nav

  // handle browser back/forward — refetch and replace dashboard when possible
  window.addEventListener('popstate', function(){
    var href = location.pathname + location.search
    fetch(href, {headers:{'X-Requested-With':'XMLHttpRequest'}}).then(function(resp){
      if(resp.status === 200) return resp.text();
      throw new Error('non-200')
    }).then(function(text){
      var parser = new DOMParser(); var doc = parser.parseFromString(text, 'text/html'); var newDash = doc.querySelector('.dashboard')
      if(newDash){ var cur = document.querySelector('.dashboard'); cur.parentNode.replaceChild(newDash, cur); initAdminUI() }
      else { window.location = href }
    }).catch(function(){ window.location = href })
  })
});
