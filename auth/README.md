```shell
openssl genrsa -out jwt-private.pem 2048
```

```shell
openssl genrsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```