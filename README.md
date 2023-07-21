## Frontend Setup

```sh
cd frontend
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Backend Setup

```sh
cd backend
pip install flask SQLAlchemy
```

### Run

```sh
uwsgi --socket 0.0.0.0:8000 --protocol=http -w wsgi:app
```