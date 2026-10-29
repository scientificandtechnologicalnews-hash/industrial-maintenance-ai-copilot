# Requisitos — Industrial Maintenance AI Copilot

## Problema
Centros logísticos y empresas con maquinaria industrial (motores, PLC,
sensores, variadores...) tienen manuales dispersos, pierden tiempo
buscando soluciones a averías ya conocidas, y el conocimiento técnico
depende de las personas con más experiencia.

## Usuarios (MVP)
| Rol | Acciones |
|---|---|
| Administrador | Gestiona máquinas, documentos, usuarios y casos resueltos |
| Técnico de mantenimiento | Consulta máquinas y documentos, registra averías, solicita orientación, confirma soluciones |
| Visitante | Ve información pública, sin sesión |



## Alcance del MVP
- CRUD de máquinas y documentos técnicos (gestión por el administrador).
- Registro y consulta de averías, visibles para todos los técnicos.
- Búsqueda de documentos por palabras clave, con puntuación explicable
  (sin PDF, sin embeddings).
- Al confirmar la causa de una avería, se puede generar un CasoResuelto.
- API REST de solo lectura más los endpoints de escritura necesarios
  para averías y soluciones.
- Dos vistas en React que consumen la API real.
- Autenticación, roles y permisos por endpoint y por objeto.

## Fuera del MVP (trabajo futuro)
- Subida y validación de PDF.
- Sesiones de diagnóstico con hipótesis/comprobaciones estructuradas.
- Embeddings o búsqueda semántica.
- Rol de estudiante de FP.
- Integración con CMMS/ERP/SCADA externos.

## Requisitos funcionales (MVP)
| ID | Requisito | Criterio mínimo |
|---|---|---|
| RF-01 | Consultar máquinas | Listado público, filtrable |
| RF-02 | Registrar avería | Guarda título, máquina, síntomas; técnico lo asigna el servidor |
| RF-03 | Consultar historial | Listado paginado, visible para cualquier técnico |
| RF-04 | Ver detalle de avería | Incluye estado y, si existe, el caso resuelto asociado |
| RF-05 | Cambiar estado | Solo el autor o un administrador; valores restringidos |
| RF-06 | Buscar documentos | Por palabras clave, con relevancia explicable |
| RF-07 | Registrar solución | Crea un CasoResuelto solo con datos suficientes (causa + procedimiento) |
| RF-08 | Autenticación | Toda operación privada exige sesión |
| RF-09 | Autorización | Permisos por endpoint y por objeto, verificados en el servidor |

## Requisitos no funcionales
- Seguridad: igual que en el proyecto anterior (ver `docs/pruebas.md`
  cuando exista), más límite de intentos de login desde el principio.
- Configuración por variables de entorno desde el primer commit.
- Pruebas automatizadas desde la Fase 3 en adelante.
- Mensajes de error comprensibles, sin trazas internas.

