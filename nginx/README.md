# How to generate SSL Certificate

1. Install [Mkcert](https://github.com/FiloSottile/mkcert)

   ```shell
   curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
   chmod +x mkcert-v*-linux-amd64
   sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
   mkcert -install
   ```

2. Generate Certificate
   
   ```shell
   cd ngnix
   mkcert langflow.languagestudio.com
   ```

3. Run the Nginx Container

    ```shell
    docker run -d \
      --name langflow-nginx \
      -p 80:80 \
      -p 3000:3000 \
      --add-host=host.docker.internal:host-gateway \
      -v "$(pwd)/default.conf":/etc/nginx/conf.d/default.conf \
      -v "$(pwd)/langflow.languagestudio.com.pem":/etc/nginx/ssl/langflow.languagestudio.com.pem \
      -v "$(pwd)/langflow.languagestudio.com-key.pem":/etc/nginx/ssl/langflow.languagestudio.com-key.pem \
      nginx:latest
    ```

If the page timeout, try enabling the firewall.

```shell
sudo ufw allow 3001
```