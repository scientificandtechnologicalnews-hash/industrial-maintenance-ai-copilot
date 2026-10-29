# Historias de usuario

## HU-01 — Registrar una avería
Como técnico, quiero registrar una avería de una máquina,
para que quede documentada y otros técnicos puedan consultarla.

Criterios de aceptación:
- Sin sesión, no puedo acceder al formulario (redirige a login).
- El formulario exige máquina, título y descripción del síntoma.
- El técnico asignado es siempre el usuario que ha iniciado sesión,
  nunca un valor del formulario.
- Al guardar, el estado inicial es "abierta".

## HU-02 — Consultar el historial de averías
Como técnico, quiero ver todas las averías registradas,
para aprender de casos anteriores aunque no sean míos.

Criterios de aceptación:
- Veo las averías de todos los técnicos, no solo las mías.
- Puedo filtrar por estado y por máquina.
- El listado está paginado.

## HU-03 — Buscar documentación técnica
Como técnico, quiero buscar por palabras clave en los documentos,
para encontrar manuales y fallos conocidos sin leer todo el archivo.

Criterios de aceptación:
- La búsqueda da preferencia a documentos de la misma máquina que la
  avería activa, sin excluir resultados válidos de otras máquinas.
- Si no hay coincidencias, el sistema lo indica, no devuelve resultados
  al azar.
- Puedo ver qué documento concreto respalda cada resultado (fuente
  trazable).

## HU-04 — Registrar una solución verificada
Como técnico, quiero confirmar la causa raíz y la solución de una
avería, para que quede como conocimiento reutilizable.

Criterios de aceptación:
- Solo puedo marcar una avería como resuelta si indico causa y
  procedimiento.
- Al resolver con datos suficientes, se crea un CasoResuelto vinculado.
- Un anónimo o un técnico sin la avería asignada no puede resolverla
  en mi nombre (ver HU-05).

## HU-05 — Protección de acceso (seguridad)
Como administrador del sistema, quiero que nadie pueda ver ni modificar
información restringida sin los permisos adecuados.

Criterios de aceptación:
- Un anónimo que accede a una URL protegida recibe un redirect al login
  (páginas) o 403 (API), nunca 200 con datos.
- Un técnico sin permiso que intenta editar la avería de otro recibe
  403, aunque adivine la URL correcta (IDOR).
- Tras varios intentos fallidos de login, la cuenta se bloquea
  temporalmente.