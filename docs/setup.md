# Setup do Ambiente

## Requisitos

- Python 3.x
- pip

Nao existe `requirements.txt` no projeto neste momento.

## 1. Criar ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Instalar dependencias minimas

```bash
pip install django==4.2.11 pillow django-debug-toolbar
```

## 3. Aplicar migracoes

```bash
python manage.py migrate
```

## 4. Criar superusuario (opcional)

```bash
python manage.py createsuperuser
```

## 5. Rodar aplicacao

```bash
python manage.py runserver
```

## Enderecos uteis

- Aplicacao: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Debug toolbar (desenvolvimento): `http://127.0.0.1:8000/__debug__/`
