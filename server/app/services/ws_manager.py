"""
WebSocket для командных игр: менеджер соединений + фоновый тикер.

Фаза 2: сервер сам пушит состояние сессии подключённым клиентам — это
заменяет HTTP-поллинг. Тикер раз в INTERVAL секунд по сессиям, где есть
активные сокеты, двигает серверный прогресс (sync_progress: авто-старт
лобби, авто-переход вопроса по таймеру) и рассылает state, если он изменился.

Однопроцессный режим (uvicorn --reload): рассылка прямая, в памяти процесса.
Для нескольких воркеров сюда добавляется Redis Pub/Sub (см. план, фаза 2+).
"""
import asyncio
import json
from typing import Dict, Set

from fastapi import WebSocket


class GameConnectionManager:
    """Хранит активные WS-соединения по session_id и рассылает им state."""

    def __init__(self):
        self.active: Dict[str, Set[WebSocket]] = {}
        self._last_hash: Dict[str, str] = {}

    async def connect(self, session_id: str, ws: WebSocket) -> None:
        await ws.accept()
        self.active.setdefault(session_id, set()).add(ws)

    def disconnect(self, session_id: str, ws: WebSocket) -> None:
        conns = self.active.get(session_id)
        if not conns:
            return
        conns.discard(ws)
        if not conns:
            self.active.pop(session_id, None)
            self._last_hash.pop(session_id, None)

    def session_ids(self):
        return list(self.active.keys())

    def has(self, session_id: str) -> bool:
        return bool(self.active.get(session_id))

    async def send_state(self, session_id: str, state: dict) -> None:
        dead = []
        for ws in list(self.active.get(session_id, [])):
            try:
                await ws.send_json(state)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(session_id, ws)

    async def broadcast_if_changed(self, session_id: str, state: dict) -> None:
        """Рассылать только при изменении состояния (меньше трафика/ре-рендеров)."""
        h = json.dumps(state, sort_keys=True, default=str)
        if self._last_hash.get(session_id) == h:
            return
        self._last_hash[session_id] = h
        await self.send_state(session_id, state)


ws_manager = GameConnectionManager()


async def game_ws_ticker(interval: float = 0.5) -> None:
    """Фоновый цикл: двигает прогресс и пушит состояние подключённым сессиям."""
    # Ленивый импорт — чтобы не словить цикл импортов на старте модулей
    from .game_sessions_manager import game_sessions_manager as gm

    while True:
        await asyncio.sleep(interval)
        try:
            for sid in ws_manager.session_ids():
                # Отвалы по таймауту heartbeat (в лобби: хост -> отмена, игрок -> выход).
                # Раньше это дёргал GET-поллинг; теперь — тикер.
                gm.check_disconnects(sid)
                gm.sync_progress(sid)
                state = gm.get_session_state(sid)
                if state is None:
                    # сессия исчезла (TTL/finished) — закрывать не обязательно,
                    # клиент сам отреагирует на is_finished/cancelled
                    continue
                await ws_manager.broadcast_if_changed(sid, state)
        except Exception:
            # тикер не должен падать — единичные ошибки игнорируем
            pass
