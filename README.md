# Backend-ES02

## API REST

La API usa JWT y requiere autenticación para las operaciones sobre visitas.

- `POST /api/token/`: obtiene los tokens enviando `username` y `password`.
- `POST /api/token/refresh/`: obtiene un nuevo access token usando `refresh`.
- `/api/visitas/`: CRUD de visitas mediante el router de DRF.
- `/cliente/`: cliente web integrado que consume la API usando JWT.

Incluye el token en las solicitudes protegidas con:

```text
Authorization: Bearer <access_token>
```

Los orígenes permitidos se configuran mediante `CORS_ALLOWED_ORIGINS` en
`.env`. Por defecto se permiten los clientes locales en el puerto `3000`.

Para validar la API localmente:

```powershell
python manage.py test visitas.tests.VisitaApiTests --keepdb
```

## Despliegue con Vercel y Supabase

1. En Supabase crea un proyecto y copia la cadena de conexión PostgreSQL desde
   **Connect > PostgreSQL**. Usa la conexión **Session pooler** si Vercel
   presenta problemas con conexiones directas.
2. En Vercel importa este repositorio. El archivo `vercel.json` usa
   `api/index.py` como entrada de Django.
3. En **Settings > Environment Variables** agrega:

   ```text
   DATABASE_URL=postgresql://postgres:[PASSWORD]@.../postgres
   SECRET_KEY=<valor-largo-aleatorio>
   DEBUG=False
   ALLOWED_HOSTS=backend-es-02.vercel.app
   CORS_ALLOWED_ORIGINS=https://<cliente>.vercel.app
   ```

   Sustituye los dominios por los reales. No subas el `.env` ni la contraseña
   de Supabase al repositorio.
4. Después del primer despliegue ejecuta las migraciones contra Supabase:

   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   ```

   Puedes ejecutar estos comandos localmente usando temporalmente el mismo
   `DATABASE_URL` de Supabase.
