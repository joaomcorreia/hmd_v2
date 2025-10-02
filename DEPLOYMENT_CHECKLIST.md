# Pre-deployment Checklist

## Before deploying to staging:
- [ ] All code committed to git
- [ ] Local tests pass: `python manage.py test`
- [ ] No Django warnings: `python manage.py check`
- [ ] Static files collect without errors: `python manage.py collectstatic`
- [ ] Admin interface works locally
- [ ] All pages render correctly
- [ ] Environment variables configured for staging

## Before deploying to production:
- [ ] Staging deployment successful and tested
- [ ] All features tested on staging environment
- [ ] Performance acceptable on staging
- [ ] SSL certificate ready for main domain
- [ ] Backup of current production site (if updating)
- [ ] Environment variables configured for production
- [ ] DNS records ready (if new domain)
- [ ] Email settings tested

## Post-deployment verification:

### Staging (test3.hmdklusbedrijf.nl):
- [ ] Homepage loads correctly
- [ ] Admin interface accessible: `/admin/`
- [ ] All page sections display properly
- [ ] Contact forms work
- [ ] Static files (CSS/JS/images) load
- [ ] No console errors in browser
- [ ] Mobile responsiveness works
- [ ] Admin sidebar navigation works

### Production (hmdklusbedrijf.nl):
- [ ] Homepage loads correctly
- [ ] Admin interface accessible: `/admin/`
- [ ] All page sections display properly
- [ ] Contact forms work and send emails
- [ ] Static files (CSS/JS/images) load
- [ ] No console errors in browser
- [ ] Mobile responsiveness works
- [ ] SSL certificate valid and working
- [ ] Performance acceptable (loading times)
- [ ] SEO elements working (meta tags, etc.)
- [ ] Admin sidebar navigation works

## Rollback plan:
If issues are found in production:
1. Revert to previous git commit
2. Or disable problematic features
3. Or redirect to maintenance page
4. Fix issues in staging first before re-deploying

## Monitoring:
- Set up server monitoring for uptime
- Monitor error logs daily for first week
- Check site performance regularly
- Monitor for spam/security issues