(function () {
  if (!document.body.classList.contains("preview-mode")) {
    return;
  }

  function applyBackgroundImage(el, url) {
    if (!el) return;
    if (url) {
      el.style.backgroundImage = 'url(' + url + ')';
    } else {
      el.style.backgroundImage = '';
    }
  }

  function getCsrfToken() {
    var name = "csrftoken";
    var cookies = document.cookie ? document.cookie.split('; ') : [];
    for (var i = 0; i < cookies.length; i++) {
      var parts = cookies[i].split('=');
      var key = decodeURIComponent(parts[0]);
      if (key === name) {
        return decodeURIComponent(parts.slice(1).join('='));
      }
    }
    return '';
  }

  function fallbackNavigation(el) {
    if (el.dataset.adminUrl) {
      window.top.location.href = el.dataset.adminUrl;
    }
  }


  function collectPreviewTargets(scope, wrapper) {
    var map = {};
    var seen = typeof WeakSet !== 'undefined' ? new WeakSet() : null;
    function add(el) {
      if (!el || !el.dataset) {
        return;
      }
      if (seen && seen.has(el)) {
        return;
      }
      if (seen) {
        seen.add(el);
      }
      var key = el.dataset.previewTarget;
      if (!key) {
        return;
      }
      (map[key] = map[key] || []).push(el);
    }
    if (wrapper) {
      wrapper.querySelectorAll('[data-preview-target]').forEach(add);
    }
    if (scope) {
      document.querySelectorAll('[data-preview-target][data-preview-scope="' + scope + '"]').forEach(add);
    }
    return map;
  }

  function bindAboutPreview(form) {
    var wrapper = form.closest('.preview-about-wrapper');
    var targets = collectPreviewTargets('homeaboutpanel', wrapper);
    if (!Object.keys(targets).length) {
      return;
    }

    function applyValue(key, raw) {
      var nodes = targets[key] || [];
      var value = '';
      if (typeof raw === 'string') {
        value = raw.trim();
      } else if (raw != null) {
        value = String(raw);
      }
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || el.dataset.previewAltDefault || el.getAttribute('alt') || '';
        var attr = el.dataset.previewAttr;
        var finalValue = value || fallback;
        if (attr) {
          if (!finalValue) {
            finalValue = fallback || '#';
          }
          el.setAttribute(attr, finalValue);
        } else {
          el.textContent = finalValue;
        }
      });
    }

    function wire(fieldName) {
      var field = form.querySelector('[name="' + fieldName + '"]');
      if (!field) {
        return;
      }
      var handler = function () {
        applyValue(fieldName, field.value || '');
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    }

    wire('title_emphasis');
    wire('title_rest');
    wire('lead_text');
    wire('body_text');
    wire('cta_label');
    wire('cta_url');
  }



  function sameOrigin(href) {
    try {
      var url = new URL(href, window.location.origin);
      return url.origin === window.location.origin;
    } catch (err) {
      return false;
    }
  }

  function ensurePreviewUrl(href, adminReturn) {
    if (!href) {
      return href;
    }
    var url = new URL(href, window.location.origin);
    url.searchParams.set('preview', '1');
    if (adminReturn) {
      url.searchParams.set('admin_return', adminReturn);
    }
    var result = url.pathname + url.search + url.hash;
    return result;
  }

  function bindPreviewNavigation() {
    if (!document.body.classList.contains('preview-mode')) {
      return;
    }
    var adminReturn = document.body.dataset.previewAdminReturn || '';
    document.addEventListener('click', function (evt) {
      var link = evt.target.closest('a');
      if (!link) {
        return;
      }
      if (link.dataset.previewIgnore === '1') {
        return;
      }
      var href = link.getAttribute('href');
      if (!href || href.startsWith('#') || href.startsWith('javascript:')) {
        return;
      }
      if (link.target && link.target !== '' && link.target !== '_self') {
        return;
      }
      if (!sameOrigin(href)) {
        return;
      }
      evt.preventDefault();
      window.location.href = ensurePreviewUrl(href, adminReturn);
    }, true);
  }


  function bindValuePreview(form) {
    if (form.dataset.previewModel !== 'homevalueblock') {
      return;
    }
    var targets = collectPreviewTargets('homevalue');

    function update(key, value, attr) {
      var nodes = targets[key] || [];
      var trimmed = value != null ? String(value).trim() : '';
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || '';
        var finalValue = trimmed || fallback;
        if (attr) {
          el.setAttribute(attr, finalValue || fallback);
        } else {
          el.textContent = finalValue;
        }
      });
    }

    function wire(name, attr) {
      var field = form.querySelector('[name="' + name + '"]');
      if (!field) {
        return;
      }
      var handler = function () {
        update(name, field.value || '', attr);
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    }

    wire('title_emphasis');
    wire('title_rest');
    wire('body');
    wire('link_1_label');
    wire('link_2_label');
    wire('link_3_label');
    wire('link_1_url', 'href');
    wire('link_2_url', 'href');
    wire('link_3_url', 'href');

    var altField = form.querySelector('[name="image_alt"]');
    if (altField) {
      var handler = function () {
        var value = altField.value || '';
        document.querySelectorAll('[data-preview-alt-target="image_alt"]').forEach(function (el) {
          var fallback = el.dataset.previewDefault || el.getAttribute('alt') || '';
          el.setAttribute('alt', value.trim() || fallback);
        });
      };
      altField.addEventListener('input', handler);
      altField.addEventListener('change', handler);
      handler();
    }

    var imageField = form.querySelector('[name="image"]');
    if (imageField) {
      imageField.addEventListener('change', function () {
        var file = imageField.files && imageField.files[0];
        if (file) {
          var reader = new FileReader();
          reader.onload = function (e) {
            update('image', e.target.result, 'src');
          };
          reader.readAsDataURL(file);
        }
      });
    }
  }

  function bindCarouselPreview(form) {
    var model = form.dataset.previewModel;
    if (model !== 'homecarouselitem' && model !== 'aboutcarouselitem') {
      return;
    }
    var scope = form.dataset.previewScope || '';
    if (!scope) {
      return;
    }
    var localWrapper = form.closest('.preview-carousel-wrapper');
    var targets = collectPreviewTargets(scope, localWrapper);

    var altNodes = [];
    function collectAlt(root) {
      if (!root) return;
      root.querySelectorAll('[data-preview-alt-target]').forEach(function (el) {
        if (scope && el.dataset.previewScope && el.dataset.previewScope !== scope) {
          return;
        }
        altNodes.push(el);
      });
    }
    collectAlt(localWrapper);
    document.querySelectorAll('[data-preview-alt-target][data-preview-scope="' + scope + '"]').forEach(function (el) {
      altNodes.push(el);
    });

    function applyTargets(key, raw) {
      var nodes = targets[key] || [];
      var value = '';
      if (typeof raw === 'string') {
        value = raw.trim();
      } else if (raw != null) {
        value = String(raw);
      }
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || el.dataset.previewAltDefault || el.getAttribute('alt') || '';
        var attr = el.dataset.previewAttr;
        var finalValue = value || fallback;
        if (attr) {
          if (!finalValue) {
            finalValue = fallback;
          }
          if (finalValue) {
            el.setAttribute(attr, finalValue);
          }
        } else {
          el.textContent = finalValue || fallback;
        }
      });
    }

    function updateAlt(value) {
      var textValue = value ? value.trim() : '';
      altNodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || el.dataset.previewAltDefault || el.getAttribute('alt') || '';
        var finalValue = textValue || fallback;
        if (el.tagName === 'IMG') {
          el.setAttribute('alt', finalValue);
        }
      });
      applyTargets('alt_text_display', textValue);
    }

    function wire(fieldName, custom) {
      var field = form.querySelector('[name="' + fieldName + '"]');
      if (!field) {
        return;
      }
      if (typeof custom === 'function') {
        custom(field);
        return;
      }
      var handler = function () {
        applyTargets(fieldName + '_display', field.value || '');
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    }

    wire('alt_text', function (field) {
      var handler = function () {
        updateAlt(field.value || '');
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    });

    wire('order', function (field) {
      var handler = function () {
        var value = field.value || '';
        applyTargets('order_display', value);
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    });

    var imageField = form.querySelector('[name="image"]');
    if (imageField) {
      imageField.addEventListener('change', function () {
        var file = imageField.files && imageField.files[0];
        if (file) {
          var reader = new FileReader();
          reader.onload = function (e) {
            applyTargets('image', e.target.result);
          };
          reader.readAsDataURL(file);
        } else {
          applyTargets('image', '');
        }
      });
    }
  }

  function bindAboutHeroPreview(form) {
    if (form.dataset.previewModel !== 'abouthero') {
      return;
    }
    var scope = form.dataset.previewScope || 'abouthero';
    var targets = collectPreviewTargets(scope);

    function apply(key, raw, attr) {
      var nodes = targets[key] || [];
      var value = '';
      if (typeof raw === 'string') {
        value = raw.trim();
      } else if (raw != null) {
        value = String(raw);
      }
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || el.dataset.previewAltDefault || '';
        var attribute = attr || el.dataset.previewAttr;
        var finalValue = value || fallback;
        if (attribute) {
          if (!finalValue) {
            finalValue = fallback || '';
          }
          el.setAttribute(attribute, finalValue);
        } else {
          el.textContent = finalValue || fallback;
        }
      });
    }

    var titleField = form.querySelector('[name="title"]');
    if (titleField) {
      var titleHandler = function () {
        apply('title', titleField.value || '');
      };
      titleField.addEventListener('input', titleHandler);
      titleField.addEventListener('change', titleHandler);
      titleHandler();
    }

    var heroEl = document.querySelector('[data-preview-scope="' + scope + '"]');
    if (heroEl) {
      var defaultBg = heroEl.getAttribute('data-preview-background') || heroEl.style.backgroundImage || '';

      function toCssUrl(value) {
        if (!value) {
          return '';
        }
        return value.indexOf('url(') === 0 ? value : 'url(' + value + ')';
      }

      function setBackground(value) {
        if (value) {
          heroEl.style.backgroundImage = toCssUrl(value);
        } else if (defaultBg) {
          heroEl.style.backgroundImage = toCssUrl(defaultBg);
        } else {
          heroEl.style.backgroundImage = '';
        }
      }

      setBackground('');

      var imageField = form.querySelector('[name="background_image"]');
      if (imageField) {
        imageField.addEventListener('change', function () {
          var file = imageField.files && imageField.files[0];
          if (file) {
            var reader = new FileReader();
            reader.onload = function (e) {
              setBackground(e.target.result);
            };
            reader.readAsDataURL(file);
          } else {
            setBackground('');
          }
        });
      }

      var clearField = form.querySelector('input[name="background_image-clear"]');
      if (clearField) {
        clearField.addEventListener('change', function () {
          if (clearField.checked) {
            setBackground('');
          } else if (!(imageField && imageField.files && imageField.files.length)) {
            setBackground('');
          }
        });
      }
    }
  }

  function bindAboutCompanyPreview(form) {
    if (form.dataset.previewModel !== 'aboutcompanyblock') {
      return;
    }
    var scope = form.dataset.previewScope || 'aboutcompany';
    var targets = collectPreviewTargets(scope);
    if (!Object.keys(targets).length) {
      return;
    }

    function apply(key, raw, attr) {
      var nodes = targets[key] || [];
      var value = '';
      if (typeof raw === 'string') {
        value = raw.trim();
      } else if (raw != null) {
        value = String(raw);
      }
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || el.dataset.previewAltDefault || '';
        var attribute = attr || el.dataset.previewAttr;
        var finalValue = value || fallback;
        if (attribute) {
          if (!finalValue) {
            finalValue = fallback || '';
          }
          el.setAttribute(attribute, finalValue);
        } else {
          el.textContent = finalValue || fallback;
        }
      });
    }

    function wire(name, attr) {
      var field = form.querySelector('[name="' + name + '"]');
      if (!field) {
        return;
      }
      var handler = function () {
        apply(name, field.value || '', attr);
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    }

    wire('years_number');
    wire('years_label');
    wire('heading');
    wire('body');
    wire('cta_label');
    wire('cta_url', 'href');
  }

  function bindAboutBenefitPreview(form) {
    if (form.dataset.previewModel !== 'aboutbenefit') {
      return;
    }
    var scope = form.dataset.previewScope || '';
    if (!scope) {
      return;
    }
    var wrapper = document.querySelector('.preview-about-benefit-wrapper[data-preview-scope="' + scope + '"]');
    var targets = collectPreviewTargets(scope, wrapper);
    if (!Object.keys(targets).length) {
      return;
    }

    function apply(key, raw, attr) {
      var nodes = targets[key] || [];
      var value = '';
      if (typeof raw === 'string') {
        value = raw.trim();
      } else if (raw != null) {
        value = String(raw);
      }
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || '';
        var attribute = attr || el.dataset.previewAttr;
        var finalValue = value || fallback;
        if (attribute) {
          if (!finalValue) {
            finalValue = fallback || '';
          }
          el.setAttribute(attribute, finalValue);
        } else {
          el.textContent = finalValue || fallback;
        }
      });
    }

    function wire(name, attr) {
      var field = form.querySelector('[name="' + name + '"]');
      if (!field) {
        return;
      }
      var handler = function () {
        apply(name, field.value || '', attr);
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    }

    wire('title');
    wire('subtitle');
    wire('description');

    var imageField = form.querySelector('[name="image"]');
    var clearField = form.querySelector('input[name="image-clear"]');
    function updateImageFromFile(file) {
      var imageNodes = targets.image || [];
      if (!imageNodes.length) {
        return;
      }
      if (file) {
        var reader = new FileReader();
        reader.onload = function (e) {
          imageNodes.forEach(function (el) {
            el.setAttribute('src', e.target.result);
          });
        };
        reader.readAsDataURL(file);
      } else {
        var fallback = imageNodes[0].dataset.previewDefault || '';
        imageNodes.forEach(function (el) {
          if (fallback) {
            el.setAttribute('src', fallback);
          }
        });
      }
    }
    if (imageField) {
      imageField.addEventListener('change', function () {
        updateImageFromFile(imageField.files && imageField.files[0]);
      });
    }
    if (clearField) {
      clearField.addEventListener('change', function () {
        if (clearField.checked) {
          updateImageFromFile(null);
        }
      });
    }

    var altField = form.querySelector('[name="image_alt"]');
    if (altField) {
      var altHandler = function () {
        apply('image_alt', altField.value || '', 'alt');
      };
      altField.addEventListener('input', altHandler);
      altField.addEventListener('change', altHandler);
      altHandler();
    }
  }
  function bindAboutProcessPreview(form) {
    if (form.dataset.previewModel !== 'aboutprocessstep') {
      return;
    }
    var scope = form.dataset.previewScope || '';
    if (!scope) {
      return;
    }
    var wrapper = form.closest('.preview-about-process-wrapper');
    var targets = collectPreviewTargets(scope, wrapper);

    function apply(key, raw, attr) {
      var nodes = targets[key] || [];
      var value = '';
      if (typeof raw === 'string') {
        value = raw.trim();
      } else if (raw != null) {
        value = String(raw);
      }
      nodes.forEach(function (el) {
        var fallback = el.dataset.previewDefault || el.dataset.previewAltDefault || '';
        var attribute = attr || el.dataset.previewAttr;
        var finalValue = value || fallback;
        if (attribute) {
          if (!finalValue) {
            finalValue = fallback || '';
          }
          el.setAttribute(attribute, finalValue);
        } else {
          el.textContent = finalValue || fallback;
        }
      });
    }

    function wire(name, attr) {
      var field = form.querySelector('[name="' + name + '"]');
      if (!field) {
        return;
      }
      var handler = function () {
        apply(name, field.value || '', attr);
      };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    }

    wire('step_title');
    wire('heading');
    wire('description');

    var imageField = form.querySelector('[name="image"]');
    if (imageField) {
      imageField.addEventListener('change', function () {
        var file = imageField.files && imageField.files[0];
        if (file) {
          var reader = new FileReader();
          reader.onload = function (e) {
            apply('image', e.target.result, 'src');
          };
          reader.readAsDataURL(file);
        } else {
          apply('image', '', 'src');
        }
      });
    }
  }

  function bindSlidePreview(form) {
    var wrapper = form.closest('.preview-slide-wrapper');
    if (!wrapper) return;
    var live = wrapper.querySelector('.preview-slide-live');
    if (live) {
      applyBackgroundImage(live, live.getAttribute('data-preview-background'));
    }

    var targets = {};
    wrapper.querySelectorAll('[data-preview-target]').forEach(function (el) {
      var key = el.dataset.previewTarget;
      (targets[key] = targets[key] || []).push(el);
    });

    function updateTarget(key, value) {
      (targets[key] || []).forEach(function (el) {
        var defaultValue = el.dataset.previewDefault || '';
        var hide = el.dataset.previewHideWhenEmpty === 'true';
        if (!value) {
          if (hide) {
            el.style.display = 'none';
          } else {
            el.style.display = '';
            el.textContent = defaultValue;
          }
        } else {
          el.style.display = '';
          el.textContent = value;
        }
      });
    }

    var handlers = {
      title: function (field) { updateTarget('title', field.value.trim()); },
      subtitle: function (field) { updateTarget('subtitle', field.value.trim()); },
      cta1_label: function (field) { updateTarget('cta1_label', field.value.trim()); },
      cta2_label: function (field) { updateTarget('cta2_label', field.value.trim()); },
      cta1_url: function (field) { updateTarget('cta1_url', field.value.trim()); },
      cta2_url: function (field) { updateTarget('cta2_url', field.value.trim()); },
      order: function (field) { updateTarget('order', field.value.trim()); },
      is_active: function (field) { updateTarget('is_active', field.checked ? 'Actief' : 'Niet actief'); },
      image: function (field) {
        if (!live) return;
        var file = field.files && field.files[0];
        if (file) {
          var reader = new FileReader();
          reader.onload = function (e) {
            applyBackgroundImage(live, e.target.result);
          };
          reader.readAsDataURL(file);
        } else {
          applyBackgroundImage(live, live.getAttribute('data-preview-background'));
        }
      }
    };

    Object.keys(handlers).forEach(function (name) {
      var field = form.querySelector('[name="' + name + '"]');
      if (!field) return;
      var handler = function () { handlers[name](field); };
      field.addEventListener('input', handler);
      field.addEventListener('change', handler);
      handler();
    });
  }

  function bindForm(form) {
    form.addEventListener('submit', function (evt) {
      evt.preventDefault();
      var endpoint = form.getAttribute('action') || form.dataset.previewEndpoint;
      if (!endpoint) {
        modal.setError('Geen endpoint gevonden.');
        return;
      }
      var formData = new FormData(form);
      fetch(endpoint, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken()
        },
        credentials: 'same-origin'
      }).then(function (resp) {
        if (resp.ok) {
          return resp.json();
        }
        return resp.json().then(function (data) {
          throw data;
        }).catch(function () {
          throw { html: '<p>Er ging iets mis. Probeer het opnieuw.</p>' };
        });
      }).then(function (data) {
        if (data.html) {
          modal.open(data.html);
        }
        if (data.success) {
          modal.close();
          window.location.reload();
        }
      }).catch(function (data) {
        if (data && data.html) {
          modal.open(data.html);
        } else {
          modal.setError('Er ging iets mis. Probeer het opnieuw.');
        }
      });
    });
  }

  var modal = (function () {
    var backdrop = document.createElement('div');
    backdrop.className = 'preview-modal-backdrop';
    backdrop.innerHTML = [
      '<div class="preview-modal" role="dialog" aria-modal="true">',
      '  <button type="button" class="preview-modal-close" data-preview-modal-close>&times;</button>',
      '  <div class="preview-modal-content">',
      '    <div class="preview-modal-body"></div>',
      '  </div>',
      '</div>'
    ].join('');
    document.body.appendChild(backdrop);

    var body = backdrop.querySelector('.preview-modal-body');

    function close() {
      backdrop.classList.remove('is-open');
      document.body.classList.remove('preview-modal-open');
      body.innerHTML = '';
    }

    backdrop.addEventListener('click', function (evt) {
      if (evt.target === backdrop || evt.target.hasAttribute('data-preview-modal-close')) {
        close();
      }
    });

    document.addEventListener('keydown', function (evt) {
      if (evt.key === 'Escape' && backdrop.classList.contains('is-open')) {
        close();
      }
    });

    return {
      open: function (html) {
        body.innerHTML = html;
        backdrop.classList.add('is-open');
        document.body.classList.add('preview-modal-open');
        attachPreviewTriggers(body);
        var form = body.querySelector('form');
        if (form) {
          bindForm(form);
          bindSlidePreview(form);
          bindAboutPreview(form);
          bindCarouselPreview(form);
          bindValuePreview(form);
          bindAboutHeroPreview(form);
          bindAboutCompanyPreview(form);
          bindAboutBenefitPreview(form);
          bindAboutProcessPreview(form);
          var firstInput = form.querySelector('input, textarea, select');
          if (firstInput) {
            firstInput.focus();
          }
        }
      },
      close: close,
      setLoading: function () {
        body.innerHTML = '<div class="preview-modal-loading">Bezig met laden...</div>';
        backdrop.classList.add('is-open');
        document.body.classList.add('preview-modal-open');
      },
      setError: function (message) {
        body.innerHTML = '<div class="preview-modal-error">' + message + '</div>';
      }
    };
  })();

  function openEditor(el) {
    var app = el.dataset.previewApp;
    var model = el.dataset.previewModel;
    var pk = el.dataset.previewId;
    var endpoint = el.dataset.previewEndpoint;
    if (!endpoint && app && model && pk) {
      endpoint = '/admin/preview/' + encodeURIComponent(app) + '/' + encodeURIComponent(model) + '/' + encodeURIComponent(pk) + '/';
    }
    if (!endpoint) {
      fallbackNavigation(el);
      return;
    }

    modal.setLoading();
    fetch(endpoint, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      credentials: 'same-origin'
    }).then(function (resp) {
      if (!resp.ok) {
        throw new Error('Fetch mislukt');
      }
      return resp.json();
    }).then(function (data) {
      if (data && data.html) {
        modal.open(data.html);
        var form = document.querySelector('.preview-modal-body form');
        if (form) {
          form.setAttribute('action', endpoint);
        }
      } else {
        throw new Error('Ongeldig antwoord');
      }
    }).catch(function () {
      modal.close();
      fallbackNavigation(el);
    });
  }

  function attachPreviewTriggers(root) {
    var scope = root || document;
    scope.querySelectorAll('[data-preview-app][data-preview-model][data-preview-id]').forEach(function (el) {
      if (el.dataset.previewBound) return;
      el.dataset.previewBound = '1';
      el.addEventListener('click', function (evt) {
        evt.preventDefault();
        openEditor(el);
      });
    });
  }

  attachPreviewTriggers(document);
  bindPreviewNavigation();
})();


