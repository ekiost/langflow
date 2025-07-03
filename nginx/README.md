# How to generate SSL Certificate

1. Install [Mkcert](https://github.com/FiloSottile/mkcert)

```
curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
chmod +x mkcert-v*-linux-amd64
sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
mkcert -install
```

2. Generate Certificate

```
mkcert langflow.languagestudio.com
```
