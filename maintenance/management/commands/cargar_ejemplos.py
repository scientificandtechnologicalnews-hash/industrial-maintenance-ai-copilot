import json
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from maintenance.models import Averia, CasoResuelto, DocumentoRAG, Maquina


class Command(BaseCommand):
    help = "Carga 5 ejemplos completos: máquina, documento, avería y caso resuelto"

    def add_arguments(self, parser):
        parser.add_argument(
            "ruta", nargs="?", default="data/ejemplos_iniciales.json",
        )
        parser.add_argument(
            "--usuario", default=None,
            help="Técnico al que se asignan las averías. Por defecto, el primer superusuario.",
        )

    def handle(self, *args, **opts):
        ruta = Path(opts["ruta"])
        if not ruta.exists():
            raise CommandError(f"No existe el archivo: {ruta}")

        User = get_user_model()
        if opts["usuario"]:
            tecnico = User.objects.filter(username=opts["usuario"]).first()
            if tecnico is None:
                raise CommandError(f"No existe el usuario '{opts['usuario']}'")
        else:
            # Sin --usuario, usamos tu superusuario: en la Fase 3 todavía
            # no existen los roles Técnico/Administrador (eso es la Fase 4).
            tecnico = User.objects.filter(is_superuser=True).first()
            if tecnico is None:
                raise CommandError(
                    "No hay ningún superusuario. Crea uno con 'python manage.py "
                    "createsuperuser' o indica --usuario."
                )

        datos = json.loads(ruta.read_text(encoding="utf-8"))
        contadores = {"maquinas": 0, "documentos": 0, "averias": 0, "casos": 0}

        # atomic: o se carga todo o no se carga nada
        with transaction.atomic():
            for ejemplo in datos:
                m = ejemplo["maquina"]
                maquina, creada = Maquina.objects.get_or_create(
                    codigo=m["codigo"], defaults=m,
                )
                contadores["maquinas"] += creada

                d = ejemplo["documento"]
                _, creado = DocumentoRAG.objects.update_or_create(
                    maquina=maquina, titulo=d["titulo"],
                    defaults={
                        "tipo": d["tipo"],
                        "contenido": d["contenido"],
                        "fuente_url": d.get("fuente_url", ""),
                    },
                )
                contadores["documentos"] += creado

                a = ejemplo["averia"]
                averia, creada = Averia.objects.update_or_create(
                    maquina=maquina, titulo=a["titulo"],
                    defaults={
                        "tecnico": tecnico,
                        "descripcion_sintoma": a["descripcion_sintoma"],
                        "acciones_realizadas": a.get("acciones_realizadas", ""),
                        "notas_adicionales": a.get("notas_adicionales", ""),
                        "prioridad": a["prioridad"],
                        "estado": a["estado"],
                    },
                )
                contadores["averias"] += creada

                c = ejemplo.get("caso_resuelto")
                if c:
                    _, creado = CasoResuelto.objects.update_or_create(
                        averia=averia,
                        defaults={
                            "causa_raiz": c["causa_raiz"],
                            "procedimiento_solucion": c["procedimiento_solucion"],
                            "tiempo_reparacion_horas": c.get("tiempo_reparacion_horas"),
                            "lecciones_aprendidas": c.get("lecciones_aprendidas", ""),
                            "tecnico_valida": tecnico,
                        },
                    )
                    contadores["casos"] += creado

        self.stdout.write(self.style.SUCCESS(
            f"Máquinas creadas: {contadores['maquinas']} | "
            f"Documentos creados: {contadores['documentos']} | "
            f"Averías creadas: {contadores['averias']} | "
            f"Casos resueltos creados: {contadores['casos']} | "
            f"Técnico usado: {tecnico.username}"
        ))

