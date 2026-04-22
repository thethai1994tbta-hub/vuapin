# Deploy to Heroku - Complete Guide

## Quick Deploy (5 minutes)

This is the easiest way to get your Vua Pin app online immediately.

### Step 1: Create Heroku Account
Go to https://www.heroku.com and sign up (free)

### Step 2: Install Heroku CLI
Download from https://devcenter.heroku.com/articles/heroku-cli

Windows: Download installer and run it

### Step 3: Login to Heroku
```bash
heroku login
```
This will open a browser to authenticate.

### Step 4: Create Heroku App
```bash
cd C:\Users\theth\pinnnn
heroku create vuapin-app
```
Replace `vuapin-app` with your desired app name (must be unique across Heroku)

### Step 5: Set Environment Variables
```bash
heroku config:set EMAIL_SENDER=your-email@gmail.com
heroku config:set EMAIL_PASSWORD=your-app-password
heroku config:set FLASK_ENV=production
```

**IMPORTANT for Gmail:**
1. Go to Google Account > Security settings
2. Enable 2-Step Verification
3. Create an "App Password" for Gmail
4. Use this App Password, NOT your main Gmail password

### Step 6: Deploy
```bash
git push heroku master
```

Wait for the build to complete...

### Step 7: Open Your App
```bash
heroku open
```

Your app is now LIVE online!

---

## Verify Deployment

Test these URLs:

```
https://your-app-name.herokuapp.com/              # Home page
https://your-app-name.herokuapp.com/admin         # Admin dashboard
https://your-app-name.herokuapp.com/cell-types    # API test
```

---

## Database Configuration

By default, your app uses SQLite which works fine for starting out.

**For higher traffic (optional later):**
Add PostgreSQL add-on:
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

Then update `server.py` to use PostgreSQL connection string from `DATABASE_URL` environment variable.

---

## Monitoring

### View Logs
```bash
heroku logs --tail
```

### Monitor in Dashboard
Go to https://dashboard.heroku.com and click your app

### View Database
```bash
heroku run python -c "import json; print(open('orders.json').read())"
```

---

## Common Issues

### Email Not Sending
- Verify Gmail App Password is correct (not your main password)
- Check heroku logs: `heroku logs --tail`
- Ensure 2-Step Verification is enabled on Gmail

### App Won't Start
- Check logs: `heroku logs --tail`
- Verify all environment variables are set: `heroku config`
- Try rebuilding: `heroku apps:destroy --app vuapin-app` and redeploy

### Database Issues
- SQLite works locally, for production use PostgreSQL add-on
- Current setup saves to `vuapin.db` which is cleared on Heroku restart

---

## Update Your App

After making changes locally:

```bash
git add .
git commit -m "Update: your changes"
git push heroku master
```

---

## Cost

**Free Tier:**
- $0/month for app
- $0/month for SQLite
- Limited to 550 dyno hours/month
- Sleep after 30 mins of inactivity (free dyno)

**To keep always running:**
- Add payment method ($5/month minimum for hobby dyno)

---

## Your Live App URL

After deployment, your app will be at:
```
https://your-app-name.herokuapp.com
```

Share this link with customers!

---

## Next Steps

1. Test all features at your live URL
2. Add a custom domain (optional):
   ```bash
   heroku domains:add yourdomain.com
   ```
3. Set up monitoring and alerts
4. Backup your data regularly
5. Monitor email delivery and customer feedback

---

## Support

For issues:
1. Check heroku logs: `heroku logs --tail`
2. Review PRODUCTION_CHECKLIST.md
3. Contact: thethai1994tbta@gmail.com
