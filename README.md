### Local Development

Create `.env.dev` file in root directory

Refer to `.env.example` for required environment variables

Symlink `.env.dev` to `.env`

```bash
ln -s .env.dev .env
```

Start containers:

```bash
docker compose watch
```
