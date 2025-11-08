"""Aplicación web mínima para visualizar y controlar la campaña."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from flask import Flask, Response, abort, redirect, render_template, request, url_for

from ..services import CampaignEngine


_TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"


def create_app(engine: Optional[CampaignEngine] = None) -> Flask:
    """Crear la aplicación Flask configurada con un ``CampaignEngine``."""

    app = Flask(__name__, template_folder=str(_TEMPLATE_DIR))
    campaign_engine = engine or CampaignEngine()

    @app.context_processor
    def inject_utilities() -> dict:
        return {"sorted": sorted, "len": len}

    @app.get("/")
    def index() -> str:
        message = request.args.get("message")
        return render_template(
            "index.html",
            state=campaign_engine.state,
            message=message,
        )

    @app.post("/advance")
    def advance_day() -> Response:
        activated = campaign_engine.advance_day()
        if activated:
            message = "Se activaron: " + ", ".join(event.id for event in activated)
        else:
            message = "No se activaron eventos en este día."
        return redirect(url_for("index", message=message))

    @app.get("/regions/<region_name>")
    def region_detail(region_name: str) -> str:
        region = campaign_engine.state.regions.get(region_name)
        if region is None:
            abort(404)
        return render_template(
            "region.html",
            region=region,
            state=campaign_engine.state,
        )

    @app.get("/heroes/<hero_name>")
    def hero_detail(hero_name: str) -> str:
        hero = campaign_engine.state.heroes.get(hero_name)
        if hero is None:
            abort(404)
        return render_template(
            "hero.html",
            hero=hero,
            state=campaign_engine.state,
        )

    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover - ejecución manual
    app.run(debug=True, host="0.0.0.0", port=8000)
