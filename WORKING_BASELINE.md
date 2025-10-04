# Working Baseline Documentation

## Current State (Commit: d2baabe)
This commit represents the WORKING baseline of the HMD website before any quote form modifications.

### What Works ✅
- **Site loads immediately** - No "page not working" symptoms
- **Full navigation visible** - HOME, DIENSTEN, PORTFOLIO, CONTACT all display
- **Complete layout rendering** - All sections load properly
- **Original WhatsApp integration** - "Offerte Aanvragen" button opens WhatsApp directly
- **All CSS and JavaScript functional** - No missing dependencies

### Current "Offerte Aanvragen" Button Behavior
Located in: `templates/partials/header.html` (lines ~55-60)
```html
<a id="open-afspraak" class="site-button-secondry btn-effect"
   href="{{ SITE_SETTINGS_WA_URL }}?text={{ 'Ik wil een offerte. Pagina: '|urlencode }}{{ request.build_absolute_uri|urlencode }}"
   target="_blank" rel="noopener nofollow">
   Offerte Aanvragen
</a>
```

**Current behavior:**
- Direct WhatsApp link
- Message: "Ik wil een offerte. Pagina: [current page URL]"
- Opens in new tab/window

### Template Structure
- `templates/base.html` - Main template with all JS includes
- `templates/partials/header.html` - Navigation and quote button
- `templates/partials/footer.html` - Footer content
- JavaScript files loaded directly in base.html (not via scripts.html)

### Critical Learning Points 🚨
1. **scripts.html causes conflicts** - Don't include it, causes infinite loops
2. **Navigation classes matter** - `collapse` class hides navigation
3. **JavaScript order is critical** - Keep existing JS loading order
4. **Template syntax errors break everything** - Always validate after changes

### Next Steps
Goal: Replace direct WhatsApp link with professional form modal that:
1. Collects comprehensive quote information
2. Formats professional WhatsApp message
3. Preserves existing design completely
4. Maintains all current functionality

### Emergency Recovery
If changes break the site:
```bash
git reset --hard d2baabe
git clean -fd
python manage.py runserver 8001
```

### File Locations
- Quote button: `templates/partials/header.html:55-60`
- Main template: `templates/base.html`
- Navigation: `templates/partials/header.html:170+`
- CSS includes: `templates/partials/head.html`
- JS includes: `templates/base.html:34+`