Desde el primer commit, la configuración sensible (clave secreta, modo depuración, orígenes permitidos) se gestiona mediante variables de entorno, nunca en el código fuente. Esto corrige una debilidad detectada en una iteración anterior del proyecto.

Averia y CasoResuelto se modelan como entidades separadas con relación uno a uno, porque no toda avería genera conocimiento reutilizable: solo cuando hay causa raíz confirmada y procedimiento verificado. Esto evita mezclar “lo que pasó” con “lo que aprendimos”, y permite auditar cuántas averías llegan a convertirse en conocimiento consolidado.

