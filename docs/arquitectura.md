# Arquitectura

## Diagrama entidad-relación

```mermaid
erDiagram
    USER ||--o{ AVERIA : registra
    MAQUINA ||--o{ AVERIA : sufre
    MAQUINA ||--o{ DOCUMENTO_RAG : documenta
    AVERIA ||--o| CASO_RESUELTO : genera

    MAQUINA {
        int id
        string nombre
        string codigo
        string categoria
        bool activa
    }
    AVERIA {
        int id
        string titulo
        string descripcion_sintoma
        string acciones_realizadas
        string estado
        datetime fecha_apertura
    }
    DOCUMENTO_RAG {
        int id
        string titulo
        string tipo
        text contenido
        string archivo
    }
    CASO_RESUELTO {
        int id
        text causa_raiz
        text procedimiento_solucion
        string tiempo_reparacion
        text lecciones_aprendidas
        datetime fecha_validacion
    }
```

## Arquitectura de componentes

```
Usuario
  │
  ▼
React + Vite  ──HTTP/JSON──▶  Django REST Framework
                                  │
                                  ├─ Autenticación y permisos
                                  ├─ Serializadores y validación
                                  ├─ Servicio de búsqueda RAG (palabras clave)
                                  │
                                  ▼
                              Django ORM ──▶ PostgreSQL
```

## Responsabilidades por capa
- **React:** formularios, tablas, estados de carga/error. No es la
  barrera de seguridad.
- **DRF:** valida, serializa y aplica permisos por endpoint.
- **Servicios de negocio (Django):** lógica como "crear CasoResuelto
  solo si hay causa y procedimiento", separada de las vistas.
- **PostgreSQL:** persistencia relacional.