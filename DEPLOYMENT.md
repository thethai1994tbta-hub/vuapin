# Hướng dẫn triển khai Vua Pin

## Development

```bash
python server.py
```
Truy cập: http://127.0.0.1:5000

## Production Deployment

### Option 1: Gunicorn (Recommended)

```bash
pip install -r requirements.txt
pip install gunicorn

# Chạy với 4 worker
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Hoặc chạy với systemd service
```

Systemd service file (`/etc/systemd/system/vua-pin.service`):
```ini
[Unit]
Description=Vua Pin Battery E-commerce
After=network.target

[Service]
User=www-data
WorkingDirectory=/home/vua-pin/app
ExecStart=/home/vua-pin/app/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start vua-pin
sudo systemctl enable vua-pin
```

### Option 2: Docker

```bash
# Build image
docker build -t vua-pin .

# Run container
docker run -d -p 5000:5000 \
  -e EMAIL_SENDER="your_email@gmail.com" \
  -e EMAIL_PASSWORD="your_app_password" \
  -v /data/vua-pin:/app/data \
  vua-pin

# Docker Compose
docker-compose up -d
```

`docker-compose.yml`:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - EMAIL_SENDER=${EMAIL_SENDER}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Option 3: Nginx + Gunicorn

```nginx
upstream vua_pin {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name example.com www.example.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://vua_pin;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
    }
}
```

### Option 4: Heroku

```bash
heroku login
heroku create your-app-name

# Set environment variables
heroku config:set EMAIL_SENDER="your_email@gmail.com"
heroku config:set EMAIL_PASSWORD="your_app_password"

# Deploy
git push heroku main
```

## SSL/HTTPS

### Let's Encrypt with Certbot (for Nginx)

```bash
sudo certbot --nginx -d example.com -d www.example.com
```

### Self-signed certificate

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Backup & Maintenance

```bash
# Backup database
cp vuapin.db vuapin.db.backup

# Compress and upload
tar czf vua-pin-backup-$(date +%Y%m%d).tar.gz vuapin.db

# Monitor logs
journalctl -u vua-pin -f
tail -f /var/log/nginx/error.log
```

## Monitoring

### Check service status
```bash
systemctl status vua-pin
```

### View logs
```bash
journalctl -u vua-pin -n 100
docker logs -f <container_id>
```

### Health check endpoint
```bash
curl http://example.com/api/admin/orders
```

## Performance Tuning

### Gunicorn workers
```bash
# Formula: (2 x CPU cores) + 1
# Example: 4 core CPU = (2 x 4) + 1 = 9 workers
gunicorn -w 9 -b 0.0.0.0:5000 wsgi:app
```

### Connection timeout
```bash
gunicorn -w 4 --timeout 30 wsgi:app
```

## Troubleshooting

### Port already in use
```bash
sudo lsof -i :5000
sudo kill -9 <PID>
```

### Database locked
```bash
# Stop service, delete database, restart
sudo systemctl stop vua-pin
rm /app/vuapin.db
sudo systemctl start vua-pin
```

### Email not sending
- Verify EMAIL_SENDER and EMAIL_PASSWORD
- Use Gmail App Password (not regular password)
- Check firewall allows SMTP (port 587)

## Security Checklist

- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Use environment variables for sensitive data
- [ ] Set FLASK_DEBUG=0 in production
- [ ] Restrict admin panel IP (optional)
- [ ] Regular database backups
- [ ] Monitor error logs
- [ ] Update dependencies regularly

## Support

Contact: 0814830562 | vuapin.shop@gmail.com
